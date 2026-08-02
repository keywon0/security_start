# 🛡️ security_start

<img width="406" height="228" alt="image" src="https://github.com/user-attachments/assets/7f7a6411-a6f1-4db1-9366-99c1dd4bda98" />


[Русский](#русский) | [English](#english)

---

## Русский

Это простая программа написанная ИИ для безопасного запуска браузера в изолированной «песочнице». Когда вы запускаете браузер через неё, он полностью отрезан от ваших личных файлов на компьютере, поэтому подхватить вирус или скрытый скрипт из сети становится невозможно. Писал для себя но буду рад критике если кого нибудь заинтересует мое "чудо"

### Как установить и запустить

```bash
git clone https://github.com/keywon0/security_start.git
cd security_start
chmod +x install.sh
./install.sh
```
*Скрипт установит `bubblewrap`, если его нет.* Запуск: через меню приложений (Security Start) или командой `security_start`.

### Технологии
* **Python 3 / Tkinter**: GUI и логика.
* **Bubblewrap (bwrap)**: изоляция (Linux).

---

## English

This is a simple AI-written program for running your browser safely inside an isolated "sandbox." When you launch the browser through it, it is completely cut off from your personal files on the computer, making it impossible to catch a virus or a hidden script from the web. I originally made this for myself, but I'd appreciate any feedback if anyone gets interested in my little "miracle". 

### Installation & Launch

```bash
git clone https://github.com/keywon0/security_start.git
cd security_start
chmod +x install.sh
./install.sh
```
*Script installs `bubblewrap` if needed.* Run via Applications menu (Security Start) or terminal command: `security_start`.

### Built With
* **Python 3 / Tkinter**: GUI and logic.
* **Bubblewrap (bwrap)**: Linux isolation.
