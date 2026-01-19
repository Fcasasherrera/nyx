import requests, time, sys, random
from colorama import Fore, Style, init

init()



# Lista de alias hacker para el AI
AI_ALIASES = [
    "N3m3s1s",
    "Gh0stPr0t0c0l",
    "R3dSh4d0w",
    "Bl4ckPh4nt0m",
    "Cyb3rW4rl0ck",
    "0verl0rd",
    "HexRunn3r",
    "N1ghtF4ll"
]

# Elegir un alias aleatorio al inicio de la sesión
AI_NAME = random.choice(AI_ALIASES)

def type_out(text: str, delay: float = 0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def ask_ai(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data: dict[str, str | list[dict[str, str]]] = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(API_URL, headers=headers, json=data)

    # Log completo de la respuesta
    try:
        resp_json = response.json()
        print(Fore.YELLOW + "[DEBUG RESPONSE]" + Style.RESET_ALL, resp_json)
    except Exception as e:
        print(Fore.RED + "[ERROR PARSING RESPONSE]" + Style.RESET_ALL, e)
        return "Error: no se pudo parsear la respuesta."

    # Verificar si existe 'choices'
    if "choices" in resp_json:
        return resp_json["choices"][0]["message"]["content"]
    else:
        return Fore.RED + "[ACCESS DENIED] " + Style.RESET_ALL + str(resp_json["error"]["message"])

print(Fore.GREEN + "[ACCESS GRANTED]" + Style.RESET_ALL)
print(Fore.GREEN + "[CONNECTION TO AI NODE ESTABLISHED]" + Style.RESET_ALL)
print(Fore.GREEN + f"[AI HANDLE: {AI_NAME}]" + Style.RESET_ALL)

while True:
    user_input = input(Fore.CYAN + "S4vit4r> " + Style.RESET_ALL)
    if user_input.lower() in ["exit", "quit"]:
        print(Fore.RED + "[SESSION TERMINATED]" + Style.RESET_ALL)
        break
    reply = ask_ai(user_input)
    type_out(Fore.GREEN + f"{AI_NAME}> " + reply + Style.RESET_ALL, delay=0.01)
