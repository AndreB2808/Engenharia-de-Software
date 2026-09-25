import json
import os
from datetime import date, datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_FINANCEIRO = os.path.join(BASE_DIR, "data", "financeiro.json")
LIMITE_PATRIMONIO = 1_000_000.00


def garantir_arquivo():
    os.makedirs(os.path.dirname(ARQUIVO_FINANCEIRO), exist_ok=True)

    if not os.path.exists(ARQUIVO_FINANCEIRO):
        with open(ARQUIVO_FINANCEIRO, "w", encoding="utf-8") as f:
            json.dump({"usuarios": {}}, f, indent=4, ensure_ascii=False)

    try:
        with open(ARQUIVO_FINANCEIRO, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError:
        dados = {"usuarios": {}}

    if "usuarios" not in dados or not isinstance(dados["usuarios"], dict):
        dados = {"usuarios": {}}

    return dados


def salvar_dados(dados):
    with open(ARQUIVO_FINANCEIRO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def garantir_usuario(dados, usuario):
    if usuario not in dados["usuarios"]:
        dados["usuarios"][usuario] = {
            "patrimonio": 0.0,
            "metas": []
        }

    perfil = dados["usuarios"][usuario]
    perfil.setdefault("patrimonio", 0.0)
    perfil.setdefault("metas", [])

    # Compatibilidade com metas criadas em versões anteriores do protótipo.
    for meta in perfil["metas"]:
        meta.setdefault("reservado", 0.0)
        meta.setdefault("observacao", "")

    return perfil


def obter_patrimonio(usuario):
    dados = garantir_arquivo()
    perfil = garantir_usuario(dados, usuario)
    salvar_dados(dados)
    return round(float(perfil["patrimonio"]), 2)


def obter_fundos_nao_alocados(usuario):
    dados = garantir_arquivo()
    perfil = garantir_usuario(dados, usuario)

    patrimonio = round(float(perfil["patrimonio"]), 2)
    total_reservado = round(
        sum(float(meta.get("reservado", 0.0)) for meta in perfil["metas"]),
        2
    )

    fundos_livres = round(patrimonio - total_reservado, 2)
    salvar_dados(dados)
    return max(fundos_livres, 0.0)


def adicionar_saldo(usuario, valor):
    try:
        valor = round(float(valor), 2)
    except (TypeError, ValueError):
        return False, "Valor inválido."

    if valor <= 0:
        return False, "Digite um valor maior que zero."

    if valor > LIMITE_PATRIMONIO:
        return False, "O valor máximo permitido é R$ 1.000.000,00."

    dados = garantir_arquivo()
    perfil = garantir_usuario(dados, usuario)
    novo_total = round(float(perfil["patrimonio"]) + valor, 2)

    if novo_total > LIMITE_PATRIMONIO:
        return False, "O patrimônio total não pode ultrapassar R$ 1.000.000,00."

    perfil["patrimonio"] = novo_total
    salvar_dados(dados)
    return True, "Saldo adicionado ao patrimônio."


def carregar_metas(usuario):
    dados = garantir_arquivo()
    perfil = garantir_usuario(dados, usuario)
    salvar_dados(dados)
    return perfil["metas"]


def criar_meta(usuario, nome, valor, emoji, data_limite, observacao=""):
    nome = str(nome).strip()
    observacao = str(observacao).strip()

    if not nome:
        return False, "Digite um nome para a meta."

    if len(nome) > 25:
        return False, "O nome da meta deve ter no máximo 25 caracteres."

    if len(observacao) > 50:
        return False, "A observação deve ter no máximo 30 caracteres."

    try:
        valor = round(float(valor), 2)
    except (TypeError, ValueError):
        return False, "Valor da meta inválido."

    if valor <= 0:
        return False, "O valor da meta deve ser maior que zero."

    if valor > LIMITE_PATRIMONIO:
        return False, "O valor da meta não pode ultrapassar R$ 1.000.000,00."

    try:
        data_meta = datetime.strptime(str(data_limite), "%Y-%m-%d").date()
    except ValueError:
        return False, "Data limite inválida."

    if data_meta <= date.today():
        return False, "A data limite deve ser posterior ao dia atual."

    dados = garantir_arquivo()
    perfil = garantir_usuario(dados, usuario)
    metas = perfil["metas"]
    novo_id = max((int(meta.get("id", 0)) for meta in metas), default=0) + 1

    metas.append({
        "id": novo_id,
        "nome": nome,
        "valor": valor,
        "emoji": str(emoji),
        "data_limite": data_meta.isoformat(),
        "observacao": observacao,
        "reservado": 0.0
    })

    salvar_dados(dados)
    return True, "Meta criada com sucesso."


def obter_status_meta(meta):
    valor_meta = round(float(meta.get("valor", 0.0)), 2)
    reservado = round(float(meta.get("reservado", 0.0)), 2)

    if valor_meta > 0 and reservado >= valor_meta:
        return "concluida"

    try:
        data_limite = datetime.strptime(str(meta.get("data_limite", "")), "%Y-%m-%d").date()
    except ValueError:
        return "em_andamento"

    if date.today() > data_limite:
        return "fracassada"

    return "em_andamento"


def reservar_fundos(usuario, meta_id, valor):
    try:
        valor = round(float(valor), 2)
    except (TypeError, ValueError):
        return False, "Valor inválido."

    if valor <= 0:
        return False, "Digite um valor maior que zero."

    dados = garantir_arquivo()
    perfil = garantir_usuario(dados, usuario)
    metas = perfil["metas"]

    meta = next((m for m in metas if int(m.get("id", -1)) == int(meta_id)), None)
    if not meta:
        return False, "Meta não encontrada."

    status = obter_status_meta(meta)
    if status == "concluida":
        return False, "Essa meta já foi concluída."
    if status == "fracassada":
        return False, "O prazo dessa meta já terminou."

    patrimonio = round(float(perfil["patrimonio"]), 2)
    total_reservado = round(
        sum(float(m.get("reservado", 0.0)) for m in metas),
        2
    )
    fundos_livres = round(patrimonio - total_reservado, 2)

    if valor > fundos_livres:
        return False, "Você não possui fundos não-alocados suficientes."

    reservado_atual = round(float(meta.get("reservado", 0.0)), 2)
    falta_para_meta = round(float(meta["valor"]) - reservado_atual, 2)

    if valor > falta_para_meta:
        return False, "O valor reservado não pode ultrapassar o objetivo da meta."

    meta["reservado"] = round(reservado_atual + valor, 2)
    salvar_dados(dados)

    if meta["reservado"] >= float(meta["valor"]):
        return True, "Fundos reservados. Meta concluída!"

    return True, "Fundos reservados para a meta."


def excluir_meta(usuario, meta_id):
    dados = garantir_arquivo()
    perfil = garantir_usuario(dados, usuario)
    metas = perfil["metas"]

    meta = next((m for m in metas if int(m.get("id", -1)) == int(meta_id)), None)

    if not meta:
        return False, "Meta não encontrada."

    metas.remove(meta)
    salvar_dados(dados)
    return True, "Meta excluída. Os fundos reservados voltaram a ficar disponíveis."
