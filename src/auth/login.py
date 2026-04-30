import json
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_USERS = os.path.join(BASE_DIR, "data", "usuarios.json")

def carregar_usuarios():
    os.makedirs(os.path.dirname(ARQUIVO_USERS), exist_ok=True)

    if not os.path.exists(ARQUIVO_USERS):
        with open(ARQUIVO_USERS, "w") as f:
            json.dump({"usuarios": []}, f, indent=4)

    with open(ARQUIVO_USERS, "r") as f:
        return json.load(f)

def login():
    dados = carregar_usuarios()

    rm = input("RM: ")
    senha = input("Senha: ")

    for u in dados["usuarios"]:
        if u["rm"] == rm and u["senha"] == senha:
            print(f"✔ Bem vindo, {u['nome']}!")
            return u["nome"] 

    print("✗ RM ou senha incorretos!")
    return None