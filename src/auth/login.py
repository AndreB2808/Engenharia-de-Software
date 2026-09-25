import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_USERS = os.path.join(BASE_DIR, "data", "usuarios.json")


def carregar_usuarios():
    os.makedirs(os.path.dirname(ARQUIVO_USERS), exist_ok=True)

    if not os.path.exists(ARQUIVO_USERS):
        with open(ARQUIVO_USERS, "w", encoding="utf-8") as f:
            json.dump({"usuarios": []}, f, indent=4, ensure_ascii=False)

    try:
        with open(ARQUIVO_USERS, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError:
        dados = {"usuarios": []}

    if "usuarios" not in dados or not isinstance(dados["usuarios"], list):
        return {"usuarios": []}

    return dados


def autenticar_usuario(nome, senha):
    nome = str(nome).strip()
    senha = str(senha).strip()
    dados = carregar_usuarios()

    for usuario in dados["usuarios"]:
        nome_salvo = str(usuario.get("nome", "")).strip()
        senha_salva = str(usuario.get("senha", "")).strip()

        if nome_salvo.casefold() == nome.casefold() and senha_salva == senha:
            return nome_salvo

    return None
