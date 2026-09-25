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
        dados = {"usuarios": []}

    return dados


def salvar_usuarios(dados):
    with open(ARQUIVO_USERS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def cadastrar_usuario(nome, senha):
    nome = str(nome).strip()
    senha = str(senha).strip()

    if not nome or not senha:
        return False, "Preencha todos os campos."

    dados = carregar_usuarios()

    if any(str(u.get("nome", "")).strip().casefold() == nome.casefold() for u in dados["usuarios"]):
        return False, "Nome de usuário já cadastrado."

    dados["usuarios"].append({
        "nome": nome,
        "senha": senha
    })

    salvar_usuarios(dados)
    return True, "Cadastro realizado com sucesso."
