import tkinter as tk
from tkinter import messagebox
import os
from core.config import ConfigManager
from core.sandbox import SandboxLauncher

class SecurityAppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🛡️ security_start — Панель Управления")
        self.root.geometry("400x200")
        
        self.config = ConfigManager()

        # ========== ИНТЕРФЕЙС ==========
        tk.Label(self.root, text="🛡️ Панель Управления Защитой", font=("Arial", 14, "bold"), pady=15).pack()

        self.btn_browser = tk.Button(
            self.root, text="🌐 Запустить Безопасный Браузер", font=("Arial", 11, "bold"),
            width=30, height=2, bg="#2ecc71", fg="white",
            command=self.launch_browser
        )
        self.btn_browser.pack(pady=10)

        tk.Label(self.root, text="📁 Файлы сохраняются в обычную папку Загрузки", font=("Arial", 10), fg="gray").pack()

        tk.Button(
            self.root, text="❌ Закрыть программу", font=("Arial", 11),
            width=30, height=1, bg="#e74c3c", fg="white",
            command=self.root.quit
        ).pack(pady=15)

    def launch_browser(self):
        profile_data = self.config.profiles["browser"]
        # Передаём только ОДИН аргумент (profile_data)
        launcher = SandboxLauncher(profile_data)
        if launcher.launch():
            messagebox.showinfo("Успех", "✅ Безопасный Firefox запущен!")

    def run(self):
        self.root.mainloop()
