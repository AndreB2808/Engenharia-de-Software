import streamlit as st
import json
import os
import csv
import io
import html

st.set_page_config(page_title="GetLab", page_icon="🏫", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_USUARIOS = os.path.join(BASE_DIR, "data", "usuarios.json")
ARQUIVO_RESERVAS = os.path.join(BASE_DIR, "data", "reservas.json")

SALAS = [
    1501, 1502, 1504, 1508, 1701, 1703, 1704,
    1706, 1710, 2201, 2202, 2203, 2204, 2301,
    2302, 2303, 2304, 2501, 2502, 2503, 2603,
    2701, 2702, 2703, 2704, 2801, 2802, 2803,
    2804, 2901, 2902, 2903
]

if "tema" not in st.session_state:
    st.session_state.tema = "light"

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"

if "menu_secao" not in st.session_state:
    st.session_state.menu_secao = "Listar salas"

if "flash" not in st.session_state:
    st.session_state.flash = None


def set_flash(tipo, mensagem):
    st.session_state.flash = (tipo, mensagem)


def render_box(texto, tipo="info"):
    texto = html.escape(str(texto))
    st.markdown(
        f'<div class="msg-box msg-{tipo}">{texto}</div>',
        unsafe_allow_html=True
    )


def mostrar_flash():
    if st.session_state.flash:
        tipo, mensagem = st.session_state.flash
        render_box(mensagem, tipo)
        st.session_state.flash = None


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


def carregar_usuarios():
    dados = garantir_arquivo(ARQUIVO_USUARIOS, {"usuarios": []})
    if "usuarios" not in dados or not isinstance(dados["usuarios"], list):
        dados["usuarios"] = []
        salvar_usuarios(dados)
    return dados


def salvar_usuarios(dados):
    os.makedirs(os.path.dirname(ARQUIVO_USUARIOS), exist_ok=True)
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


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


def login_streamlit(rm, senha):
    dados = carregar_usuarios()
    rm = str(rm).strip()
    senha = str(senha).strip()

    for usuario in dados["usuarios"]:
        if str(usuario.get("rm", "")).strip() == rm and str(usuario.get("senha", "")).strip() == senha:
            return usuario.get("nome", "")
    return None


def cadastrar_streamlit(nome, rm, senha):
    nome = str(nome).strip()
    rm = str(rm).strip()
    senha = str(senha).strip()

    if not nome or not rm or not senha:
        return False, "Preencha todos os campos."

    if not rm.isdigit():
        return False, "RM inválido. Use apenas números."

    dados = carregar_usuarios()

    if any(str(u.get("rm", "")).strip() == rm for u in dados["usuarios"]):
        return False, "RM já cadastrado."

    dados["usuarios"].append({
        "nome": nome,
        "rm": rm,
        "senha": senha
    })
    salvar_usuarios(dados)
    return True, "Cadastro realizado com sucesso."


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


def aplicar_tema():
    if st.session_state.tema == "dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
        }

        body, .stApp, .stApp p, .stApp label, .stApp span, .stApp div, .stApp li, .stApp h1, .stApp h2, .stApp h3 {
            color: white !important;
            font-weight: bold !important;
        }

        div[data-testid="stTextInput"] > div,
        div[data-baseweb="select"] > div {
            border: 2px solid white;
            border-radius: 6px;
            background-color: white;
        }

        div[data-testid="stTextInput"] input,
        div[data-baseweb="select"] * {
            color: black !important;
        }

        div[data-baseweb="select"] {
            background-color: white !important;
        }

        div[data-testid="stTextInput"] input {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        div[data-testid="stTextInput"]:focus-within > div,
        div[data-baseweb="select"]:focus-within > div {
            border: 2px solid #ed145b;
            box-shadow: 0 0 6px #ed145b;
        }

        .stButton > button,
        .stDownloadButton > button {
            background-color: #262730;
            color: white;
            border: 2px solid white;
            border-radius: 6px;
            font-weight: bold;
            white-space: nowrap;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border: 2px solid #ed145b;
            color: #ed145b;
        }

        div[data-testid="stTextInput"] button {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
            filter: invert(1);
        }

        div[data-testid="stTextInput"] svg {
            fill: white !important;
        }

        div[data-testid="InputInstructions"] {
            display: none !important;
        }

        .msg-box {
            width: 100%;
            max-width: 620px;
            margin: 0 auto 16px auto;
            padding: 12px 14px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            border: 2px solid transparent;
        }

        .msg-success { background-color: #1f3b2c; color: #d7ffe4 !important; border-color: #55b07a; }
        .msg-error { background-color: #3a1f24; color: #ffd7dc !important; border-color: #d66b7b; }
        .msg-warning { background-color: #3a331a; color: #fff4c2 !important; border-color: #d6bf57; }
        .msg-info { background-color: #1f2f3a; color: #d9f0ff !important; border-color: #5e97c7; }

        .sala-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            color: white;
        }

        .sala-table th,
        .sala-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #444;
        }

        .sala-table th {
            background: #1b1f27;
            color: white;
        }

        .sala-table td {
            background: #11151c;
            color: white;
        }

        .sala-table .col-sala {
            text-align: right;
            width: 45%;
        }

        .sala-table .col-status {
            text-align: center;
            width: 55%;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background-color: #F0F2F6;
        }

        body, .stApp, .stApp p, .stApp label, .stApp span, .stApp div, .stApp li, .stApp h1, .stApp h2, .stApp h3 {
            color: black !important;
            font-weight: bold !important;
        }

        div[data-testid="stTextInput"] > div,
        div[data-baseweb="select"] > div {
            border: 2px solid black;
            border-radius: 6px;
            background-color: white;
        }

        div[data-testid="stTextInput"] input,
        div[data-baseweb="select"] * {
            color: black !important;
        }

        div[data-baseweb="select"] {
            background-color: white !important;
        }

        div[data-testid="stTextInput"] input {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        div[data-testid="stTextInput"]:focus-within > div,
        div[data-baseweb="select"]:focus-within > div {
            border: 2px solid #ed145b;
            box-shadow: 0 0 6px #ed145b;
        }

        .stButton > button,
        .stDownloadButton > button {
            background-color: #e0e0e0;
            color: black;
            border: 2px solid black;
            border-radius: 6px;
            font-weight: bold;
            white-space: nowrap;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border: 2px solid #ed145b;
            color: #ed145b;
        }

        div[data-testid="stTextInput"] button {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
        }

        div[data-testid="InputInstructions"] {
            display: none !important;
        }

        .msg-box {
            width: 100%;
            max-width: 620px;
            margin: 0 auto 16px auto;
            padding: 12px 14px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            border: 2px solid transparent;
        }

        .msg-success { background-color: #dff3e5; color: #125a30 !important; border-color: #55b07a; }
        .msg-error { background-color: #f9dfe3; color: #8c1f2f !important; border-color: #d66b7b; }
        .msg-warning { background-color: #fff4cf; color: #826500 !important; border-color: #d6bf57; }
        .msg-info { background-color: #dcecff; color: #124d79 !important; border-color: #5e97c7; }

        .sala-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            color: black;
        }

        .sala-table th,
        .sala-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #c8c8c8;
        }

        .sala-table th {
            background: #e9edf3;
            color: black;
        }

        .sala-table td {
            background: #ffffff;
            color: black;
        }

        .sala-table .col-sala {
            text-align: right;
            width: 45%;
        }

        .sala-table .col-status {
            text-align: center;
            width: 55%;
        }
        </style>
        """, unsafe_allow_html=True)

aplicar_tema()

top1, top2, top3 = st.columns([1, 2, 8])

with top1:
    if st.button("🌓", use_container_width=True):
        st.session_state.tema = "dark" if st.session_state.tema == "light" else "light"
        st.rerun()

with top2:
    if st.session_state.usuario is not None:
        if st.button("Logout", use_container_width=True):
            st.session_state.usuario = None
            st.session_state.menu_secao = "Listar salas"
            st.rerun()

st.markdown("<h1 style='text-align:center;'>🏫 GetLab</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Sistema de reserva de laboratórios</p>", unsafe_allow_html=True)
mostrar_flash()

if st.session_state.usuario is None:
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        op1, op2 = st.columns(2)
        with op1:
            if st.button("Login", use_container_width=True):
                st.session_state.auth_mode = "Login"
                st.rerun()
        with op2:
            if st.button("Cadastro", use_container_width=True):
                st.session_state.auth_mode = "Cadastro"
                st.rerun()

    if st.session_state.auth_mode == "Login":
        col1, col2 = st.columns(2)

        with col1:
            rm = st.text_input("RM")

        with col2:
            senha = st.text_input("Senha", type="password")

        if st.button("Entrar", use_container_width=True):
            usuario = login_streamlit(rm, senha)
            if usuario:
                st.session_state.usuario = usuario
                st.session_state.menu_secao = "Listar salas"
                st.rerun()
            else:
                set_flash("error", "RM ou senha inválidos.")
                st.rerun()

    else:
        nome = st.text_input("Nome")
        rm = st.text_input("RM")
        senha = st.text_input("Senha", type="password")

        if st.button("Cadastrar", use_container_width=True):
            ok, msg = cadastrar_streamlit(nome, rm, senha)
            if ok:
                set_flash("success", msg)
                st.rerun()
            else:
                set_flash("error", msg)
                st.rerun()

else:
    st.markdown(
        f"<h3 style='text-align:center;'>Bem vindo, {st.session_state.usuario}!</h3>",
        unsafe_allow_html=True
    )

    if "menu_secao" not in st.session_state:
        st.session_state.menu_secao = "Listar salas"

    linha1 = st.columns(3)
    with linha1[0]:
        if st.button("Listar salas", use_container_width=True):
            st.session_state.menu_secao = "Listar salas"
            st.rerun()
    with linha1[1]:
        if st.button("Reservar uma sala", use_container_width=True):
            st.session_state.menu_secao = "Reservar uma sala"
            st.rerun()
    with linha1[2]:
        if st.button("Consultar reserva ativa", use_container_width=True):
            st.session_state.menu_secao = "Consultar reserva ativa"
            st.rerun()

    linha2 = st.columns([1, 2, 2, 1])
    with linha2[1]:
        if st.button("Cancelar reserva ativa", use_container_width=True):
            st.session_state.menu_secao = "Cancelar reserva ativa"
            st.rerun()
    with linha2[2]:
        if st.button("Exportar reservas CSV", use_container_width=True):
            st.session_state.menu_secao = "Exportar reservas CSV"
            st.rerun()

    st.markdown("---")

    menu = st.session_state.menu_secao

    if menu == "Listar salas":

        st.markdown("<h3 style='text-align:center;'>Salas disponíveis</h3>", unsafe_allow_html=True)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(BASE_DIR, "data", "reservas.json")

        if not os.path.exists(caminho):
            dados = {"reservas": []}
        else:
            with open(caminho, "r") as f:
                dados = json.load(f)

        reservas = dados.get("reservas", [])

        salas = [
            1501,1502,1504,1508,1701,1703,1704,
            1706,1710,2201,2202,2203,2204,2301,
            2302,2303,2304,2501,2502,2503,2603,
            2701,2702,2703,2704,2801,2802,2803,
            2804,2901,2902,2903
        ]

        # Cabeçalho
        st.markdown(
            "<div style='display:flex; justify-content:center; gap:120px;'>"
            "<b>SALA</b><b>STATUS</b>"
            "</div>",
            unsafe_allow_html=True
        )

        # Linhas
        for s in salas:
            status = "RESERVADA" if any(r["sala"] == s for r in reservas) else "DISPONÍVEL"

            cor = "#ed145b" if status == "RESERVADA" else "green"

            st.markdown(
                f"<div style='display:flex; justify-content:center; gap:120px;'>"
                f"<span>{s}</span>"
                f"<span style='color:{cor}'>{status}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

    elif menu == "Reservar uma sala":
        sala = st.selectbox("Escolha a sala", SALAS)

        if st.button("Reservar", use_container_width=True):
            ok, msg = reservar_sala(st.session_state.usuario, sala)
            if ok:
                set_flash("success", msg)
                st.rerun()
            else:
                set_flash("error", msg)
                st.rerun()

    elif menu == "Consultar reserva ativa":
        reserva = usuario_tem_reserva(st.session_state.usuario)

        if reserva:
            render_box(f"Sua reserva ativa é a sala {reserva['sala']}.", "info")
        else:
            render_box("Você não possui reserva ativa.", "warning")

    elif menu == "Cancelar reserva ativa":
        reserva = usuario_tem_reserva(st.session_state.usuario)

        if reserva:
            render_box(f"Reserva encontrada para a sala {reserva['sala']}.", "info")
            if st.button("Cancelar reserva", use_container_width=True):
                ok, msg = cancelar_reserva(st.session_state.usuario)
                if ok:
                    set_flash("success", msg)
                    st.rerun()
                else:
                    set_flash("error", msg)
                    st.rerun()
        else:
            render_box("Você não possui reserva ativa.", "warning")

    elif menu == "Exportar reservas CSV":
        csv_data = exportar_reservas_csv()
        st.download_button(
            "Baixar CSV das reservas",
            data=csv_data,
            file_name="reservas_getlab.csv",
            mime="text/csv",
            use_container_width=True
        )