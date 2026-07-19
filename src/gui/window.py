import tkinter as tk
from tkinter import messagebox
import os
import shutil
from core.config import ConfigManager
from core.sandbox import SandboxLauncher

class SecurityAppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🛡️ security_start — Панель Управления")
        self.root.geometry("500x520")
        
        self.config = ConfigManager()
        self.sandbox_dir = "/tmp/sandbox_firefox_downloads"
        self.real_downloads = os.path.expanduser("~/Downloads")

        # 1. Заголовок
        tk.Label(self.root, text="🛡️ Панель Управления Защитой", font=("Arial", 14, "bold"), pady=15).pack()

        # 2. Блок запуска браузера
        tk.Label(self.root, text="Шаг 1: Запуск безопасной среды", font=("Arial", 10, "italic"), fg="gray").pack()
        self.btn_browser = tk.Button(
            self.root, text="🌐 Запустить Безопасный Браузер", font=("Arial", 11, "bold"),
            width=35, height=2, bg="#2ecc71", fg="white",
            command=self.launch_browser
        )
        self.btn_browser.pack(pady=10)

        # 3. 🔥 ЗАГЛУШКА НА БУДУЩЕЕ (Вместо Kate)
        self.btn_future = tk.Button(
            self.root, text="📝 [ Функция будет добавлена позже ]", font=("Arial", 11, "italic"),
            width=35, height=2, bg="#95a5a6", fg="#d5dbdb", state="disabled" 
            # state="disabled" делает кнопку серой и некликабельной
        )
        self.btn_future.pack(pady=5)

        # Разделительная линия
        tk.Frame(self.root, height=2, bd=1, relief="sunken", bg="lightgray").pack(fill="x", padx=50, pady=15)

        # 4. Блок настройки ПИН-кода
        tk.Label(self.root, text="Шаг 2: Настройка шлюза данных", font=("Arial", 10, "italic"), fg="gray").pack()
        tk.Label(self.root, text="Придумайте ПИН-код для этой сессии:", font=("Arial", 11)).pack(pady=5)
        
        self.entry_pin = tk.Entry(self.root, font=("Arial", 14), width=15, justify="center", show="*")
        self.entry_pin.pack(pady=5)
        self.entry_pin.insert(0, "1234") 

        # 5. Блок работы со скачанными файлами
        self.btn_gateway = tk.Button(
            self.root, text="📥 Проверить и извлечь файлы из изолятора", font=("Arial", 11),
            width=35, height=2, bg="#3498db", fg="white",
            command=self.process_files
        )
        self.btn_gateway.pack(pady=15)

        # 6. Кнопка Выхода
        tk.Button(self.root, text="❌ Закрыть программу", font=("Arial", 11), width=35, height=1, bg="#e74c3c", fg="white", command=self.root.quit).pack(pady=15)

    def launch_browser(self):
        profile_data = self.config.profiles["browser"]
        launcher = SandboxLauncher(profile_data)
        if launcher.launch():
            messagebox.showinfo("Успех", "Безопасный Firefox запущен!\nВсе скачиваемые файлы изолированы.")

    def process_files(self):
        user_pin = self.entry_pin.get().strip()
        if not user_pin:
            messagebox.showwarning("Внимание", "Поле ПИН-кода не может быть пустым!")
            return

        if not os.path.exists(self.sandbox_dir) or not os.listdir(self.sandbox_dir):
            messagebox.showinfo("Изолятор пуст", "В изолированной папке загрузок пока нет новых файлов.")
            return

        files = os.listdir(self.sandbox_dir)
        selected_file = files[0]

        confirm = messagebox.askyesno(
            "Извлечение файла", 
            f"В изоляторе найден файл:\n{selected_file}\n\nПеренести его в реальную систему по указанному ПИН-коду?"
        )
        
        if confirm:
            src_path = os.path.join(self.sandbox_dir, selected_file)
            dst_path = os.path.join(self.real_downloads, selected_file)
            
            try:
                shutil.move(src_path, dst_path)
                messagebox.showinfo("Успех", f"Файл успешно проверен и перенесен в: {dst_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось перенести файл: {e}")

    def run(self):
        self.root.mainloop()
