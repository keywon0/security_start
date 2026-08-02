import subprocess
import os
import shutil
from core.config import ConfigManager

class SandboxLauncher:
    def __init__(self, profile_data: dict):
        self.app_name = profile_data["app_name"]
        self.network_allowed = profile_data["network"]

    def generate_bwrap_command(self) -> list:
        cmd = [
            "bwrap",
            "--ro-bind", "/usr", "/usr",
            "--ro-bind", "/lib", "/lib",
            "--ro-bind", "/lib64", "/lib64",
            "--ro-bind", "/bin", "/bin",
            "--proc", "/proc",
            "--dev", "/dev",
            "--as-pid-1",
            "--unshare-pid"
        ]

        # Графика
        display = os.environ.get("DISPLAY")
        if display:
            cmd.extend(["--setenv", "DISPLAY", display])
            if os.path.exists("/tmp/.X11-unix"):
                cmd.extend(["--ro-bind", "/tmp/.X11-unix", "/tmp/.X11-unix"])

        xauthority = os.environ.get("XAUTHORITY")
        if xauthority and os.path.exists(xauthority):
            cmd.extend(["--ro-bind", xauthority, xauthority])

        # Wayland
        wayland_display = os.environ.get("WAYLAND_DISPLAY")
        runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
        if wayland_display and runtime_dir:
            wayland_socket = os.path.join(runtime_dir, wayland_display)
            if os.path.exists(wayland_socket):
                cmd.extend(["--ro-bind", wayland_socket, wayland_socket])
                cmd.extend(["--setenv", "WAYLAND_DISPLAY", wayland_display])
                cmd.extend(["--setenv", "XDG_RUNTIME_DIR", runtime_dir])

        # Шрифты и темы
        for font_dir in ["/usr/share/fonts", "/usr/share/themes", "/usr/share/icons"]:
            if os.path.exists(font_dir):
                cmd.extend(["--ro-bind", font_dir, font_dir])

        # D-Bus
        dbus_pointer = os.environ.get("DBUS_SESSION_BUS_ADDRESS")
        if dbus_pointer and "path=" in dbus_pointer:
            try:
                dbus_path = dbus_pointer.split("path=")[1].split(",")[0]
                if os.path.exists(dbus_path):
                    cmd.extend(["--bind", dbus_path, dbus_path])
            except Exception:
                pass

        # Сеть
        if self.network_allowed:
            cmd.extend(["--share-net"])
            dns_file_path = "/tmp/sandbox_dns.conf"
            with open(dns_file_path, "w") as f:
                f.write("nameserver 8.8.8.8\nnameserver 1.1.1.1\n")
            cmd.extend(["--ro-bind", dns_file_path, "/etc/resolv.conf"])
        else:
            cmd.append("--unshare-net")

        # ===== ПОЛНАЯ ИЗОЛЯЦИЯ ДОМАШНЕЙ ПАПКИ =====
        # Создаём временную папку (tmpfs) — она исчезнет после закрытия
        fake_home = "/tmp/sandbox_firefox_home"
        
        # Удаляем старую, если есть
        if os.path.exists(fake_home):
            shutil.rmtree(fake_home, ignore_errors=True)
        
        # Создаём новую
        os.makedirs(fake_home)
        
        # Создаём минимальные папки внутри fake_home
        for subdir in [".mozilla", ".cache", ".config", ".local"]:
            os.makedirs(os.path.join(fake_home, subdir), exist_ok=True)
        
        # ===== ПРИВЯЗЫВАЕМ fake_home как ~ (НО НЕ РЕАЛЬНУЮ) =====
        cmd.extend(["--bind", fake_home, os.path.expanduser("~")])
        
        # ===== ПРИВЯЗЫВАЕМ ТОЛЬКО ПАПКУ ЗАГРУЗОК (если хочешь сохранять файлы) =====
        # Это единственная папка, которая будет видна из реальной системы
        downloads = os.path.expanduser("~/Загрузки")
        if os.path.exists(downloads):
            cmd.extend(["--bind", downloads, downloads])
        
        downloads_en = os.path.expanduser("~/Downloads")
        if os.path.exists(downloads_en):
            cmd.extend(["--bind", downloads_en, downloads_en])
        
        # Устанавливаем HOME внутри песочницы
        cmd.extend(["--setenv", "HOME", os.path.expanduser("~")])

        # ===== ЗАПУСК FIREFOX =====
        cmd.append(self.app_name)
        cmd.append("--no-remote")
        cmd.append("--new-instance")
        
        return cmd

    def launch(self) -> bool:
        if not ConfigManager.check_system_dependency("bwrap"):
            print("\n❌ Ошибка: bubblewrap не установлен!")
            return False

        if not ConfigManager.check_system_dependency(self.app_name):
            print(f"\n❌ Ошибка: {self.app_name} не найден!")
            return False

        command = self.generate_bwrap_command()
        print(f"\n🛡️ Запуск {self.app_name}...")
        
        try:
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            return True
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return False
