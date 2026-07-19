from core.config import ConfigManager
from core.sandbox import SandboxLauncher
import sys

def main():
    print("=============================================")
    print("🛡️  security_start — Помощник Безопасности Linux")
    print("=============================================")
    
    # Инициализируем менеджер конфигурации
    config = ConfigManager()

    while True:
        print("\nДоступные режимы безопасности:")
        
        # Автоматически выводим меню на основе профилей из JSON
        # Метод items() возвращает пары (ключ, значение) из словаря
        available_keys = []
        for index, (profile_id, data) in enumerate(config.profiles.items(), 1):
            print(f"{index}. {data['desc']}")
            available_keys.append(profile_id)
            
        print(f"{len(available_keys) + 1}. Выход из программы")
        
        choice = input("\nВведите номер режима: ").strip()
        
        # Проверяем, нажал ли пользователь выход
        if choice == str(len(available_keys) + 1):
            print("🔒 Система безопасности закрыта. До свидания!")
            sys.exit(0)
            
        # Проверяем корректность ввода
        # try-except здесь переводит введенный текст в число
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_keys):
                # Получаем имя выбранного профиля (например, 'browser')
                selected_profile = available_keys[choice_idx]
                profile_data = config.profiles[selected_profile]
                
                # Передаем данные профиля в песочницу и запускаем
                launcher = SandboxLauncher(profile_data)
                if launcher.launch():
                    print(f"🚀 Приложение успешно запущено в песочнице!")
                    print(f"📂 Изолированная папка загрузок: {launcher.sandbox_download_dir}")
            else:
                print("❌ Ошибка: Выберите номер из списка!")
        except ValueError:
            print("❌ Ошибка: Введите корректное число!")

if __name__ == "__main__":
    main()
