import requests, time, sys, random, json, os
from colorama import Fore, Style, init
from dotenv import load_dotenv
from datetime import datetime
from pyfiglet import Figlet
from typing import Any

init()
load_dotenv()

API_URL: str = os.getenv("API_URL", "http://localhost:11434/api/chat")  # default Ollama

# Lista de alias hacker para el AI
AI_ALIASES: list[str] = [
    "N3m3s1s",
    "Gh0stPr0t0c0l",
    "R3dSh4d0w",
    "Bl4ckPh4nt0m",
    "Cyb3rW4rl0ck",
    "0verl0rd",
    "HexRunn3r",
    "N1ghtF4ll"
]

current_ai_name: str = random.choice(AI_ALIASES)
MODEL_NAME: str = "gemma:2b"  # modelo inicial
conversation: list[dict[str, str]] = []  # historial

# Crear carpeta de logs
os.makedirs("logs", exist_ok=True)
log_file: str = f"logs/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# Mensajes MOTD estilo hacker
MOTD: list[str] = [
    ">>> Welcome to ShadowNet. Unauthorized access will be traced...",
    ">>> Node secured. Awaiting encrypted transmission...",
    ">>> AI core online. Ghost Protocol engaged...",
    ">>> Transmission channel established. Hack the planet...",
    ">>> [SYS-ALERT] Surveillance bypassed. Secure channel open..."
]

def log_message(role: str, content: str) -> None:
    """Guardar mensajes en archivo de log con timestamp"""
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{role.upper()}] {content}\n")

def type_out(text: str, delay: float = 0.02) -> None:
    """Imprimir texto con efecto máquina de escribir"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def ask_ai(prompt: str) -> str:
    """Enviar prompt al modelo Ollama y devolver respuesta"""
    conversation.append({"role": "user", "content": prompt})
    data: dict[str, str | list[dict[str, str]]] = {
        "model": MODEL_NAME,
        "messages": conversation
    }

    try:
        response = requests.post(API_URL, json=data, stream=True)
    except Exception as e:
        print(Fore.RED + "[ERROR CONNECTION]" + Style.RESET_ALL, e)
        return "Error: no se pudo conectar con Ollama."

    reply: str = ""
    try:
        for line in response.iter_lines():
            if line:
                try:
                    parsed: dict[str, Any] = json.loads(line.decode("utf-8"))
                    if "message" in parsed and "content" in parsed["message"]:
                        reply += parsed["message"]["content"]
                except Exception as e:
                    print(Fore.RED + "[ERROR PARSING CHUNK]" + Style.RESET_ALL, e)
    except Exception as e:
        print(Fore.RED + "[ERROR STREAM]" + Style.RESET_ALL, e)
        return "Error: fallo al procesar la respuesta."

    if reply.strip() == "":
        return Fore.RED + "[ACCESS DENIED]" + Style.RESET_ALL + " No se recibió contenido."

    conversation.append({"role": "assistant", "content": reply})
    log_message("assistant", reply)
    return reply

# Banner ASCII + MOTD
f: Figlet = Figlet(font="slant")
print(Fore.GREEN + f.renderText(current_ai_name) + Style.RESET_ALL)
print(Fore.MAGENTA + random.choice(MOTD) + Style.RESET_ALL)
print(Fore.GREEN + "[ACCESS GRANTED]" + Style.RESET_ALL)
print(Fore.GREEN + "[CONNECTION TO AI NODE ESTABLISHED]" + Style.RESET_ALL)
print(Fore.GREEN + f"[AI HANDLE: {current_ai_name} | MODEL: {MODEL_NAME}]" + Style.RESET_ALL)

# Loop principal
while True:
    user_input: str = input(Fore.CYAN + "S4vit4r> " + Style.RESET_ALL)
    log_message("user", user_input)

    if user_input.lower() in ["exit", "quit"]:
        print(Fore.RED + "[SESSION TERMINATED]" + Style.RESET_ALL)
        break

    # Comandos internos
    if user_input.startswith(":"):
        cmd: str = user_input[1:].lower()
        if cmd == "clear":
            conversation.clear()
            print(Fore.YELLOW + "[CONTEXT CLEARED]" + Style.RESET_ALL)
            continue
        elif cmd == "alias":
            current_ai_name = random.choice(AI_ALIASES)
            print(Fore.YELLOW + f"[ALIAS CHANGED TO: {current_ai_name}]" + Style.RESET_ALL)
            continue
        elif cmd.startswith("model"):
            parts: list[str] = cmd.split()
            if len(parts) > 1:
                MODEL_NAME: str = parts[1]
                print(Fore.YELLOW + f"[MODEL CHANGED TO: {MODEL_NAME}]" + Style.RESET_ALL)
            else:
                print(Fore.RED + "[USAGE: :model <name>]" + Style.RESET_ALL)
            continue
        elif cmd == "debug":
            print(Fore.YELLOW + "[DEBUG CONVERSATION]" + Style.RESET_ALL, conversation)
            continue
        else:
            print(Fore.RED + "[UNKNOWN COMMAND]" + Style.RESET_ALL)
            continue

    reply: str = ask_ai(user_input)
    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    type_out(Fore.GREEN + f"[{timestamp}] [{current_ai_name}]> " + reply + Style.RESET_ALL, delay=0.01)
