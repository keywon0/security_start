import json
import os
import shutil

class ConfigManager:
    def __init__(self):
        # Определяем путь к папке пользователя (~/.config/security_start)
        self.config_dir = os.path.expanduser("~/.config/security_start")
        self.config_file = os.path.join(self.config_dir, "profiles.json")
        
        # Если папки нет, создаем её
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            
        # Загружаем или создаем стандартные профили
        self.profiles = self.load_profiles()

    def load_profiles(self) -> dict:
        """Загружает профили из JSON файла. Если файла нет — создает дефолтные."""
        if not os.path.exists(self.config_file):
            # Начальные настройки (Словарь в Python)
            default_profiles = {
                "browser": {
                    "app_name": "firefox",
                    "network": True,
                    "desc": "Безопасный серфинг (Изоляция файлов + Интернет)"
                },
                "office": {
                    "app_name": "Kate",
                    "network": False,
                    "desc": "Изолированный редактор (Интернет полностью ЗАБЛОКИРОВАН)"
                }
            }
            # Записываем словарь в файл в формате JSON
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_profiles, f, indent=4, ensure_ascii=False)
            return default_profiles
        
        # Если файл есть, просто читаем его
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def check_system_dependency(program_name: str) -> bool:
        """Проверяет, установлена ли программа в Linux системе"""
        # shutil.which ищет путь к программе (например, /usr/bin/bwrap). 
        # Если не находит, возвращает None
        return shutil.which(program_name) is not None
