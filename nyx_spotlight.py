import tkinter as tk
import subprocess
import os
import keyboard  # pip install keyboard

# Configuración de rutas y comandos
COMMANDS = {
    "fajillassap": r'C:\Users\fecasas\AppData\Local\Programs\Microsoft VS Code\Code.exe "C:\Users\fecasas\code\fajillassap"',
    "fastapi": r'C:\Users\fecasas\AppData\Local\Programs\Microsoft VS Code\Code.exe "C:\Users\fecasas\code\FASTAPI"',
    "chrome": r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    "copilot": r'C:\Program Files\Google\Chrome\Application\chrome.exe https://copilot.microsoft.com'
}

# Función para ejecutar comandos
def run_command(cmd):
    try:
        subprocess.Popen(cmd, shell=True)
    except Exception as e:
        print(f"Error ejecutando {cmd}: {e}")

# Función para procesar entrada
def process_input(event=None):
    query = entry.get().strip().lower()
    if query in COMMANDS:
        run_command(COMMANDS[query])
    else:
        try:
            # Calculadora básica
            result = eval(query)
            output_label.config(text=f"Resultado: {result}")
        except:
            output_label.config(text="Comando no reconocido")
    entry.delete(0, tk.END)

# Crear ventana Spotlight
def create_window():
    global entry, output_label
    win = tk.Tk()
    win.title("Nyx Spotlight")
    win.geometry("500x100+500+300")
    win.configure(bg="#0f0f17")

    entry = tk.Entry(win, font=("Segoe UI", 14))
    entry.pack(fill="x", padx=10, pady=10)
    entry.bind("<Return>", process_input)

    output_label = tk.Label(win, text="", font=("Segoe UI", 12), fg="white", bg="#0f0f17")
    output_label.pack()

    win.mainloop()

# Hotkey global para abrir Spotlight
def hotkey_listener():
    keyboard.add_hotkey("ctrl+space", create_window)
    print("Nyx Spotlight activo. Presiona Ctrl+Space para abrir.")
    keyboard.wait()

if __name__ == "__main__":
    hotkey_listener()
