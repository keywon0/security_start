#!/bin/bash

# Цвета для красивого вывода в терминал
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0;m' # Без цвета

echo -e "${BLUE}=============================================${NC}"
echo -e "${BLUE}🛡️ Установка приложения security_start...${NC}"
echo -e "${BLUE}=============================================${NC}"

# 🔥 Проверка и автоматическая установка системной утилиты bubblewrap
echo -e "${BLUE}[1/5] Проверка системных зависимостей...${NC}"

if command -v bwrap &> /dev/null; then
    echo -e "${GREEN}  ✓ Утилита bubblewrap уже установлена в системе.${NC}"
else
    echo -e "${YELLOW}  ⚠ Утилита bubblewrap не найдена. Начинаем установку...${NC}"
    echo -e "${YELLOW}  💡 Для установки системных компонентов требуется пароль sudo.${NC}"

    # Определяем пакетный менеджер дистрибутива (Ubuntu/Arch/Fedora)
    if [ -x "$(command -v apt)" ]; then
        sudo apt update && sudo apt install -y bubblewrap
    elif [ -x "$(command -v pacman)" ]; then
        sudo pacman -Sy --noconfirm bubblewrap
    elif [ -x "$(command -v dnf)" ]; then
        sudo dnf install -y bubblewrap
    else
        echo -e "${RED}❌ Ошибка: Не удалось определить ваш менеджер пакетов.${NC}"
        echo -e "${RED}   Пожалуйста, установите 'bubblewrap' вручную через ваш терминал.${NC}"
        exit 1
    fi

    # Проверка, что установка прошла успешно
    if ! command -v bwrap &> /dev/null; then
        echo -e "${RED}❌ Ошибка: Не удалось установить bubblewrap. Установка прервана.${NC}"
        exit 1
    fi
    echo -e "${GREEN}  ✓ bubblewrap успешно установлен!${NC}"
fi

# Подготовка системных папок пользователя
echo -e "${BLUE}[2/5] Подготовка системных папок...${NC}"
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/share/security_start

# Копирование файлов проекта
echo -e "${BLUE}[3/5] Копирование файлов проекта...${NC}"
cp -r src/ ~/.local/share/security_start/

# Создание исполняемого скрипта запуска в ~/.local/bin
echo -e "${BLUE}[4/5] Создание исполняемого скрипта запуска...${NC}"
cat << 'EOF' > ~/.local/bin/security_start
#!/bin/bash
if command -v python3w &> /dev/null; then
    python3w ~/.local/share/security_start/src/main.pyw &> /dev/null &
else
    python3 ~/.local/share/security_start/src/main.pyw &> /dev/null &
fi
EOF


# Делаем файл запуска исполняемым
chmod +x ~/.local/bin/security_start

# Создание системного ярлыка (.desktop файл) для меню приложений
echo -e "${BLUE}[5/5] Создание системного ярлыка для меню приложений...${NC}"
cat << EOF > ~/.local/share/applications/security_start.desktop
[Desktop Entry]
Version=1.0
Type=Application
Name=Security Start
Comment=Помощник безопасного запуска приложений в песочнице
Exec=$HOME/.local/bin/security_start
Terminal=false
Icon=security-high
Categories=Utility;Security;
EOF

# Обновляем базу данных ярлыков Linux
update-desktop-database ~/.local/share/applications &> /dev/null

echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}✅ Установка успешно завершена!${NC}"
echo -e "${GREEN}💡 Теперь вы можете найти 'Security Start' в меню ваших приложений${NC}"
echo -e "${GREEN}   или запустить командой 'security_start' в терминале.${NC}"
echo -e "${GREEN}=============================================${NC}"
