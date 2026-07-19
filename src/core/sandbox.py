import subprocess
import os
from core.config import ConfigManager

class SandboxLauncher:
    def __init__(self, profile_data: dict):
        self.app_name = profile_data["app_name"]
        self.network_allowed = profile_data["network"]
        self.sandbox_download_dir = f"/tmp/sandbox_{self.app_name}_downloads"
        
        if not os.path.exists(self.sandbox_download_dir):
            os.makedirs(self.sandbox_download_dir)

    def generate_bwrap_command(self) -> list:
        """Генерирует безопасную команду для запуска GUI/Wayland приложений через bubblewrap"""
        cmd = [
            "bwrap",
            "--ro-bind", "/usr", "/usr",
            "--ro-bind", "/lib", "/lib",
            "--ro-bind", "/lib64", "/lib64",
            "--ro-bind", "/bin", "/bin",
            "--dir", "/tmp",
            "--proc", "/proc",
            "--dev", "/dev",
            "--as-pid-1",                  
            "--unshare-pid"               
        ]

        # Настройка графики (Wayland / X11)
        wayland_display = os.environ.get("WAYLAND_DISPLAY")
        xauthority = os.environ.get("XAUTHORITY")
        display = os.environ.get("DISPLAY")
        runtime_dir = os.environ.get("XDG_RUNTIME_DIR")

        if wayland_display and runtime_dir:
            wayland_socket = os.path.join(runtime_dir, wayland_display)
            if os.path.exists(wayland_socket):
                cmd.extend(["--ro-bind", wayland_socket, wayland_socket])
                cmd.extend(["--setenv", "WAYLAND_DISPLAY", wayland_display])
                cmd.extend(["--setenv", "XDG_RUNTIME_DIR", runtime_dir])

        if display:
            cmd.extend(["--setenv", "DISPLAY", display])
            if os.path.exists("/tmp/.X11-unix"):
                cmd.extend(["--ro-bind", "/tmp/.X11-unix", "/tmp/.X11-unix"])
        if xauthority and os.path.exists(xauthority):
            cmd.extend(["--ro-bind", xauthority, xauthority])

        for font_dir in ["/usr/share/fonts", "/usr/share/themes", "/usr/share/icons", "/usr/share/KDE"]:
            if os.path.exists(font_dir):
                cmd.extend(["--ro-bind", font_dir, font_dir])

        # Полный список /etc для тяжелых приложений (Kate/KDE требует dbus и темы)
        important_etc_files = [
            "fonts", "passwd", "group", "host.conf", "hosts", 
            "nsswitch.conf", "ssl", "pki", "crypto-policies",
            "dbus-1", "alternatives", "xdg"
        ]
        
        cmd.extend(["--dir", "/etc"])
        for etc_item in important_etc_files:
            system_path = f"/etc/{etc_item}"
            if os.path.exists(system_path):
                cmd.extend(["--ro-bind", system_path, system_path])

        # Проброс сокета D-Bus для Kate
        dbus_pointer = os.environ.get("DBUS_SESSION_BUS_ADDRESS")
        if dbus_pointer and "path=" in dbus_pointer:
            try:
                dbus_path = dbus_pointer.split("path=")[1].split(",")[0]
                if os.path.exists(dbus_path):
                    cmd.extend(["--bind", dbus_path, dbus_path])
            except Exception:
                pass

        # Настройка сети
        if self.network_allowed:
            cmd.extend(["--share-net"])
            dns_file_path = f"/tmp/sandbox_{self.app_name}_dns.conf"
            with open(dns_file_path, "w") as f:
                f.write("nameserver 8.8.8.8\nnameserver 1.1.1.1\n")
            cmd.extend(["--ro-bind", dns_file_path, "/etc/resolv.conf"])
        else:
            cmd.append("--unshare-net")

        # Создаем изолированную домашнюю папку
        fake_home = f"/tmp/sandbox_{self.app_name}_home"
        if not os.path.exists(fake_home):
            os.makedirs(fake_home)
            
        cmd.extend(["--bind", fake_home, os.path.expanduser("~")])
        cmd.extend(["--bind", self.sandbox_download_dir, os.path.expanduser("~/Downloads")])
        cmd.extend(["--setenv", "HOME", os.path.expanduser("~")])

        cmd.append(self.app_name)
        if self.app_name == "firefox":
            cmd.append("--no-remote")
            
        # 🔥 НОВОЕ: Запрещаем Kate искать другие процессы и заставляем открыть НОВОЕ окно
        elif self.app_name == "kate":
            cmd.append("--new-instance")
            
        return cmd

    def launch(self) -> bool:
        """Запуск изолированного процесса"""
        if not ConfigManager.check_system_dependency("bwrap"):
            print("\n❌ КРИТИЧЕСКАЯ ОШИБКА: Утилита 'bubblewrap' не установлена!")
            return False

        if not ConfigManager.check_system_dependency(self.app_name):
            print(f"\n❌ ОШИБКА: Программа '{self.app_name}' не найдена!")
            return False

        fake_home = f"/tmp/sandbox_{self.app_name}_home"
        if os.path.exists(fake_home):
            import shutil
            try:
                shutil.rmtree(fake_home)
            except Exception:
                pass

        command = self.generate_bwrap_command()
        print(f"\n🛡️ [security_start] Запуск {self.app_name}...")
        
        try:
            # Временно меняем Popen на run, чтобы Python ЖДАЛ завершения команды 
            # и принудительно выводил все системные ошибки на экран
            result = subprocess.run(command, capture_output=True, text=True)
            
            # Если bwrap завершился с ошибкой, печатаем её в терминал
            if result.returncode != 0:
                print("\n❌ СИСТЕМНЫЙ СБОЙ ПЕСОЧНИЦЫ:")
                print(result.stderr)
                return False
                
            return True
        except Exception as e:
            print(f"❌ Непредвиденная ошибка при запуске: {e}")
            return False
