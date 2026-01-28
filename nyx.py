import json
import os
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox

# ---------- Utilidades ----------
def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def speak(text, cfg):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        # Voz femenina si está disponible
        if cfg["voice"].get("female_preferred", True):
            for v in engine.getProperty('voices'):
                # Heurística simple: elegir voz con "female" o "woman" en el nombre
                name = (v.name or "").lower()
                if "female" in name or "woman" in name or "zira" in name or "eva" in name:
                    engine.setProperty('voice', v.id)
                    break
        engine.setProperty('rate', cfg["voice"].get("rate", 170))
        engine.setProperty('volume', cfg["voice"].get("volume", 1.0))
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[Nyx] TTS error: {e}")

def open_vscode(vscode_path, project_path):
    subprocess.Popen([vscode_path, project_path], shell=False)

def open_chrome(chrome_path, url=None, extra_flags=None):
    cmd = [chrome_path]
    if extra_flags:
        # dividir flags respetando espacios entre comillas
        from shlex import split
        cmd += split(extra_flags)
    if url:
        cmd.append(url)
    subprocess.Popen(cmd, shell=False)

def delayed(fn, delay=1.0, *args, **kwargs):
    def runner():
        time.sleep(delay)
        fn(*args, **kwargs)
    threading.Thread(target=runner, daemon=True).start()

# ---------- GUI ----------
class NyxApp(tk.Tk):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.title("Nyx — Diosa de la Noche")
        self.geometry("520x360")
        self.configure(bg="#0f0f17" if cfg["ui"].get("theme") == "dark" else "#f5f5f5")

        fg = "#e6e6fa" if cfg["ui"].get("theme") == "dark" else "#222"
        accent = "#7f5af0"

        # Header
        header = tk.Label(self, text="Bienvenido, " + cfg["user"]["title"], font=("Segoe UI", 16, "bold"),
                          bg=self["bg"], fg=fg)
        header.pack(pady=(16, 8))

        sub = tk.Label(self, text="Nyx ha despertado. ¿Qué deseas abrir?",
                       font=("Segoe UI", 11), bg=self["bg"], fg=fg)
        sub.pack(pady=(0, 16))

        # Botones de acciones
        btn_frame = tk.Frame(self, bg=self["bg"])
        btn_frame.pack(pady=8)

        def mkbtn(text, cmd):
            b = tk.Button(btn_frame, text=text, command=cmd,
                          font=("Segoe UI", 10, "bold"),
                          bg=accent, fg="white", activebackground="#5b3bd9",
                          relief="flat", padx=12, pady=8)
            b.pack(fill="x", pady=6)
            return b

        mkbtn("Abrir VS Code — fajillassap", self.open_fajillassap)
        mkbtn("Abrir VS Code — FASTAPI", self.open_fastapi)
        mkbtn("Chrome (flags) → Mavipos", self.open_chrome_mavipos)
        mkbtn("Chrome normal", self.open_chrome_normal)
        mkbtn("Abrir Thunderbird (Correo)", self.open_thunderbird)


        # Footer
        footer = tk.Label(self, text="La diosa Nyx vela por tu código.",
                          font=("Segoe UI", 9, "italic"), bg=self["bg"], fg=fg)
        footer.pack(side="bottom", pady=12)

        # Saludo inicial
        greeting = cfg["voice"]["greeting"].format(title=cfg["user"]["title"])
        if cfg["ui"].get("show_popup", True):
            delayed(lambda: messagebox.showinfo("Nyx", greeting), 0.5)
        if cfg["voice"].get("enabled", True):
            delayed(speak, 0.8, greeting, cfg)

        # Lanzamientos automáticos al abrir (opcional)
        delayed(self.auto_launch, 1.2)

    # Acciones
    def open_fajillassap(self):
        open_vscode(self.cfg["paths"]["vscode"], self.cfg["paths"]["project_fajillassap"])

    def open_fastapi(self):
        open_vscode(self.cfg["paths"]["vscode"], self.cfg["paths"]["project_fastapi"])

    def open_chrome_mavipos(self):
        open_chrome(
            self.cfg["paths"]["chrome"],
            url=self.cfg["web"]["mavipos_url"],
            extra_flags=self.cfg["web"]["chrome_flags_profile"]
        )

    def open_chrome_normal(self):
        open_chrome(self.cfg["paths"]["chrome"])
    def open_thunderbird(self):
        subprocess.Popen([self.cfg["paths"]["thunderbird"]], shell=False)

    def auto_launch(self):
        # Abre todo como en tu init.bat, con pequeños delays para no saturar
        # delayed(self.open_fajillassap, 0.2)
        # delayed(self.open_fastapi, 0.6)
        delayed(self.open_chrome_mavipos, 1.0)
        # delayed(self.open_chrome_normal, 1.4)
        delayed(self.open_thunderbird, 1.8)

def main():
    cfg = load_config()
    app = NyxApp(cfg)
    app.mainloop()

if __name__ == "__main__":
    main()
