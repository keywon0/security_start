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
            "--as-pid-1",                  # Решает ошибку EPERM
            "--unshare-pid"               # Требование безопасности для --as-pid-1
        ]

        # 🖥️ Настройка графики (Wayland / X11)
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

        for font_dir in ["/usr/share/fonts", "/usr/share/themes", "/usr/share/icons"]:
            if os.path.exists(font_dir):
                cmd.extend(["--ro-bind", font_dir, font_dir])

        # 🔥 ИСПРАВЛЕНИЕ СЕТИ И /etc БЕЗ КОНФЛИКТОВ С СЫЛКАМИ
        # Вместо монтирования всего /etc, мы монтируем только те файлы, которые реально нужны для работы GUI и сети
        important_etc_files = [
            "fonts", "passwd", "group", "host.conf", "hosts", 
            "nsswitch.conf", "ssl", "pki", "crypto-policies"
        ]
        
        # Создаем виртуальную пустую папку /etc внутри песочницы
        cmd.extend(["--dir", "/etc"])
        
        # Прокидываем в неё только действительно важные системные файлы, если они существуют
        for etc_item in important_etc_files:
            system_path = f"/etc/{etc_item}"
            if os.path.exists(system_path):
                cmd.extend(["--ro-bind", system_path, system_path])

        if self.network_allowed:
            cmd.extend(["--share-net"])
            
            # Создаем на твоем ПК простой текстовый файл с DNS-серверами Google и Cloudflare
            dns_file_path = f"/tmp/sandbox_{self.app_name}_dns.conf"
            with open(dns_file_path, "w") as f:
                f.write("nameserver 8.8.8.8\nnameserver 1.1.1.1\n")
            
            # Теперь монтируем наш файл прямо в пустую виртуальную точку /etc/resolv.conf без всяких конфликтов!
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
        
        # 🔥 НОВОЕ: Если мы запускаем именно firefox, добавляем флаг --no-remote
        # Это заставит его запустить СВОЙ независимый процесс, проигнорировав открытый в системе браузер
        if self.app_name == "firefox":
            cmd.append("--no-remote")
            
        return cmd

    def launch(self) -> bool:
        """Запуск изолированного процесса"""
        if not ConfigManager.check_system_dependency("bwrap"):
            print("\n❌ КРИТИЧЕСКАЯ ОШИБКА: Утилита 'bubblewrap' не установлена!")
            return False

        # 🔥 НОВОЕ: Полностью стираем старую фейковую домашнюю папку перед запуском,
        # чтобы у браузера не было «памяти» о прошлых сессиях внутри нашей программы.
        fake_home = f"/tmp/sandbox_{self.app_name}_home"
        if os.path.exists(fake_home):
            import shutil
            shutil.rmtree(fake_home) # rmtree полностью удаляет папку со всеми файлами внутри

        command = self.generate_bwrap_command()
        print(f"\n🛡️ [security_start] Запуск {self.app_name}...")
        
        try:
            subprocess.Popen(command)
            return True
        except FileNotFoundError:
            print(f"❌ Ошибка: Приложение '{self.app_name}' не найдено в системе.")
            return False
        except Exception as e:
            print(f"❌ Непредвиденная ошибка при запуске: {e}")
            return False
