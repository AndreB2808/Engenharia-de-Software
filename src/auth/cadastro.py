import json
import os
import time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_USERS = os.path.join(BASE_DIR, "data", "usuarios.json")

def carregar_usuarios():
    os.makedirs(os.path.dirname(ARQUIVO_USERS), exist_ok=True)

    if not os.path.exists(ARQUIVO_USERS):
        with open(ARQUIVO_USERS, "w") as f:
            json.dump({"usuarios": []}, f, indent=4)

    with open(ARQUIVO_USERS, "r") as f:
        return json.load(f)

def salvar_usuarios(dados):
    with open(ARQUIVO_USERS, "w") as f:
        json.dump(dados, f, indent=4)

def cadastrar():
    dados = carregar_usuarios()

    nome = input("Nome: ")
    rm = input("RM: ")
    senha = input("Senha: ")

    if not rm.isdigit():
        print("RM inválido!")
        return

    if any(u["rm"] == rm for u in dados["usuarios"]):
        print("Usuário já existe!")
        return

    dados["usuarios"].append({
        "nome": nome,
        "rm": rm,
        "senha": senha
    })

    salvar_usuarios(dados)

    print("✔ Cadastro realizado!")
    time.sleep(2)