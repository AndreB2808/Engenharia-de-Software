import json
import os
import csv
import io
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_RESERVAS = os.path.join(BASE_DIR, "data", "reservas.json")


SALAS = [
    1501, 1502, 1504, 1508, 1701, 1703, 1704,
    1706, 1710, 2201, 2202, 2203, 2204, 2301,
    2302, 2303, 2304, 2501, 2502, 2503, 2603,
    2701, 2702, 2703, 2704, 2801, 2802, 2803,
    2804, 2901, 2902, 2903
]

def garantir_arquivo(caminho, estrutura_padrao):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    if not os.path.exists(caminho):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(estrutura_padrao, f, indent=4, ensure_ascii=False)
        return estrutura_padrao

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(estrutura_padrao, f, indent=4, ensure_ascii=False)
        return estrutura_padrao

    if not isinstance(dados, dict):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(estrutura_padrao, f, indent=4, ensure_ascii=False)
        return estrutura_padrao

    return dados


def carregar_reservas():
    dados = garantir_arquivo(ARQUIVO_RESERVAS, {"reservas": []})
    if "reservas" not in dados or not isinstance(dados["reservas"], list):
        dados["reservas"] = []
        salvar_reservas(dados)
    return dados


def salvar_reservas(dados):
    os.makedirs(os.path.dirname(ARQUIVO_RESERVAS), exist_ok=True)
    with open(ARQUIVO_RESERVAS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def usuario_tem_reserva(usuario):
    dados = carregar_reservas()
    return next((r for r in dados["reservas"] if r["usuario"] == usuario), None)


def reservar_sala(usuario, sala):
    dados = carregar_reservas()

    if any(r["usuario"] == usuario for r in dados["reservas"]):
        return False, "Você já possui uma reserva ativa."

    if sala not in SALAS:
        return False, "Sala inválida."

    if any(r["sala"] == sala for r in dados["reservas"]):
        return False, "Essa sala já está reservada."

    dados["reservas"].append({
        "usuario": usuario,
        "sala": sala
    })
    salvar_reservas(dados)
    return True, f"Reserva realizada com sucesso para a sala {sala}."


def cancelar_reserva(usuario):
    dados = carregar_reservas()
    reserva = next((r for r in dados["reservas"] if r["usuario"] == usuario), None)

    if not reserva:
        return False, "Você não possui reserva ativa."

    dados["reservas"].remove(reserva)
    salvar_reservas(dados)
    return True, f"Reserva da sala {reserva['sala']} cancelada com sucesso."


def exportar_reservas_csv():
    dados = carregar_reservas()["reservas"]
    saida = io.StringIO()
    escritor = csv.DictWriter(saida, fieldnames=["usuario", "sala"])
    escritor.writeheader()
    escritor.writerows(dados)
    return saida.getvalue()
