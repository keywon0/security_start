# 🛡️ security_start

<img width="519" height="563" alt="image" src="https://github.com/user-attachments/assets/4cc9cd58-520a-446f-83ac-790d04fc6189" />


[Русский](#русский) | [English](#english)

---

## Русский

Это простая программа написанная ИИ для безопасного запуска браузера в изолированной «песочнице». Когда вы запускаете браузер через неё, он полностью отрезан от ваших личных файлов на компьютере, поэтому подхватить вирус или скрытый скрипт из сети становится невозможно. Писал для себя но буду рад критике если кого нибудь заинтересует мое "чудо".

Все скачанные картинки и документы не попадают сразу на компьютер, а ловятся во временную скрытую папку (изолятор). Чтобы забрать файл в свои реальные загрузки, нужно будет ввести ПИН-код в окне программы."

### Как установить и запустить

```bash
git clone https://github.com/security_start
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

Any downloaded pictures and documents don't land straight on your computer; instead, they are caught in a temporary hidden folder (the isolator). To pull a file into your real downloads, you'll just need to type in a PIN code in the program's window.

### Installation & Launch

```bash
git clone https://github.com/security_start
cd security_start
chmod +x install.sh
./install.sh
```
*Script installs `bubblewrap` if needed.* Run via Applications menu (Security Start) or terminal command: `security_start`.

### Built With
* **Python 3 / Tkinter**: GUI and logic.
* **Bubblewrap (bwrap)**: Linux isolation.
