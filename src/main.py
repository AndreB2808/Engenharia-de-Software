import streamlit as st
import json
import os
import html

from models.reserva_model import (
    carregar_reservas,
    usuario_tem_reserva,
    reservar_sala,
    cancelar_reserva,
    exportar_reservas_csv,
    garantir_arquivo,
    SALAS
)

from views.interface_view import (
    render_box,
    aplicar_tema
)

st.set_page_config(page_title="GetLab", page_icon="🏫", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_USUARIOS = os.path.join(BASE_DIR, "data", "usuarios.json")
ARQUIVO_RESERVAS = os.path.join(BASE_DIR, "data", "reservas.json")

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

def mostrar_flash():
    if st.session_state.flash:
        tipo, mensagem = st.session_state.flash
        render_box(mensagem, tipo)
        st.session_state.flash = None

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

        reservas = carregar_reservas()["reservas"]

        salas = [
            1501,1502,1504,1508,1701,1703,1704,
            1706,1710,2201,2202,2203,2204,2301,
            2302,2303,2304,2501,2502,2503,2603,
            2701,2702,2703,2704,2801,2802,2803,
            2804,2901,2902,2903
        ]

        st.markdown(
            "<div style='display:flex; justify-content:center; gap:120px;'>"
            "<b>SALA</b><b>STATUS</b>"
            "</div>",
            unsafe_allow_html=True
        )

        for s in salas:
            status = "⛔ RESERVADA" if any(r["sala"] == s for r in reservas) else "✅ DISPONÍVEL" 

            st.markdown(
                f"<div style='display:flex; justify-content:center; gap:120px;'>"
                f"<span style='margin-left:52px;'>{s}</span>"
                f"<span>{status}</span>"
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