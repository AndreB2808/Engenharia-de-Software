from datetime import date, timedelta
import base64
import html
import os

import streamlit as st
import streamlit.components.v1 as components

from auth.cadastro import cadastrar_usuario
from auth.login import autenticar_usuario
from models.financeiro_model import (
    adicionar_saldo,
    carregar_metas,
    criar_meta,
    excluir_meta,
    obter_fundos_nao_alocados,
    obter_patrimonio,
    obter_status_meta,
    reservar_fundos,
)
from views.interface_view import aplicar_tema, formatar_data, formatar_reais, render_box


st.set_page_config(page_title="Servatio", page_icon="💰", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_LOGO = os.path.join(BASE_DIR, "assets", "logo.png")

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"

if "flash" not in st.session_state:
    st.session_state.flash = None


def set_flash(tipo, mensagem, auto_hide=True):
    st.session_state.flash = (tipo, mensagem, auto_hide)


def mostrar_flash():
    if st.session_state.flash:
        flash = st.session_state.flash

        # Aceita também o formato antigo de duas posições caso a sessão já
        # estivesse aberta antes desta atualização.
        if len(flash) == 2:
            tipo, mensagem = flash
            auto_hide = True
        else:
            tipo, mensagem, auto_hide = flash

        render_box(mensagem, tipo, auto_hide=auto_hide)
        st.session_state.flash = None


def carregar_logo_base64():
    with open(CAMINHO_LOGO, "rb") as arquivo:
        return base64.b64encode(arquivo.read()).decode("utf-8")


def rolar_para_elemento(elemento_id):
    # Mantém o usuário na região em que a ação aconteceu, em vez de
    # fazê-lo voltar ao topo da página para ver uma mensagem de erro.
    components.html(
        f"""
        <script>
        setTimeout(function() {{
            const elemento = window.parent.document.getElementById("{elemento_id}");
            if (elemento) {{
                elemento.scrollIntoView({{behavior: "smooth", block: "center"}});
            }}
        }}, 80);
        </script>
        """,
        height=0,
        width=0
    )


aplicar_tema()

logo_base64 = carregar_logo_base64()
st.markdown(
    f"""
    <div class="brand-header">
        <img class="brand-logo" src="data:image/png;base64,{logo_base64}" alt="Logo Servatio">
        <div class="brand-title">Servatio</div>
    </div>
    <div class="brand-subtitle">
        <span class="subtitle-main">Seu dinheiro com propósito.</span>
        <span class="subtitle-detail">Organize suas metas hoje e acompanhe o caminho até elas.</span>
    </div>
    """,
    unsafe_allow_html=True
)
mostrar_flash()


if st.session_state.usuario is None:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login", use_container_width=True):
            st.session_state.auth_mode = "Login"
            st.rerun()

    with col2:
        if st.button("Cadastro", use_container_width=True):
            st.session_state.auth_mode = "Cadastro"
            st.rerun()

    st.markdown("---")

    if st.session_state.auth_mode == "Login":
        st.subheader("Entrar")
        nome = st.text_input("Nome")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar no Servatio", use_container_width=True):
            usuario = autenticar_usuario(nome, senha)

            if usuario:
                st.session_state.usuario = usuario
                st.rerun()
            else:
                set_flash("error", "Nome ou senha inválidos.")
                st.rerun()

    else:
        st.subheader("Criar conta")
        nome = st.text_input("Nome")
        senha = st.text_input("Senha", type="password")

        if st.button("Cadastrar", use_container_width=True):
            ok, msg = cadastrar_usuario(nome, senha)

            if ok:
                st.session_state.auth_mode = "Login"
                set_flash("success", msg)
                st.rerun()
            else:
                set_flash("error", msg)
                st.rerun()

else:
    # Navegação visual do protótipo. Apenas "Metas financeiras" representa
    # uma área implementada; as demais ficam propositalmente desabilitadas.
    st.markdown(
        """
        <div class="prototype-nav">
            <button class="prototype-nav-button prototype-nav-active" type="button">🎯 Metas financeiras</button>
            <button class="prototype-nav-button prototype-nav-disabled" type="button" disabled>📈 Investimentos</button>
            <button class="prototype-nav-button prototype-nav-disabled" type="button" disabled>🔗 Serviços conectados</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    top1, top2 = st.columns([4, 1])

    with top1:
        usuario_seguro = html.escape(str(st.session_state.usuario))
        st.markdown(f"### Olá, {usuario_seguro}!")

    with top2:
        if st.button("Sair", use_container_width=True):
            st.session_state.usuario = None
            st.rerun()

    patrimonio = obter_patrimonio(st.session_state.usuario)
    fundos_livres = obter_fundos_nao_alocados(st.session_state.usuario)

    st.markdown(
        f"""
        <div class="servatio-card">
            <div class="patrimonio-label">Patrimônio total simulado</div>
            <div class="patrimonio-valor">{formatar_reais(patrimonio)}</div>
            <div class="fundos-label">Fundos não-alocados</div>
            <div class="fundos-valor">{formatar_reais(fundos_livres)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("➕ Adicionar saldo para testes"):
        valor_saldo = st.number_input(
            "Valor a adicionar",
            min_value=0.01,
            max_value=1_000_000.00,
            value=100.00,
            step=10.00,
            format="%.2f"
        )

        if st.button("Adicionar ao patrimônio", use_container_width=True):
            ok, msg = adicionar_saldo(st.session_state.usuario, valor_saldo)
            set_flash("success" if ok else "error", msg)
            st.rerun()

    st.markdown("---")

    # Mensagens da criação de metas ficam nesta posição, imediatamente acima
    # do título da seção, em vez de serem enviadas ao aviso global do topo.
    flash_meta_area = st.empty()
    if "flash_meta_criacao" in st.session_state:
        tipo_meta, mensagem_meta = st.session_state.pop("flash_meta_criacao")
        with flash_meta_area.container():
            render_box(
                mensagem_meta,
                tipo_meta,
                auto_hide=True,
                element_id="mensagem-criacao-meta"
            )

    st.subheader("🎯 Metas financeiras")

    amanha = date.today() + timedelta(days=1)

    # Os widgets da criação usam chaves próprias para que possam ser
    # realmente limpos depois que uma meta for criada com sucesso.
    if st.session_state.pop("resetar_form_meta", False):
        st.session_state.meta_emoji = "🎯"
        st.session_state.meta_nome = ""
        st.session_state.meta_valor = 1000.00
        st.session_state.meta_data = amanha
        st.session_state.meta_observacao = ""

    if "meta_emoji" not in st.session_state:
        st.session_state.meta_emoji = "🎯"
    if "meta_nome" not in st.session_state:
        st.session_state.meta_nome = ""
    if "meta_valor" not in st.session_state:
        st.session_state.meta_valor = 1000.00
    if "meta_data" not in st.session_state or st.session_state.meta_data < amanha:
        st.session_state.meta_data = amanha
    if "meta_observacao" not in st.session_state:
        st.session_state.meta_observacao = ""

    with st.expander("Criar nova meta", expanded=True):
        coluna_emoji, coluna_nome = st.columns([1, 9], gap="small")

        with coluna_emoji:
            emoji = st.selectbox(
                "Emoji",
                ["🎯", "💵", "💸", "🪙", "💲", "🌱", "💳", "💻", "🚗", "🏠", "✈️", "🎂", "📱", "💰", "🎮", "🎁", "🏆"],
                key="meta_emoji"
            )

        with coluna_nome:
            nome_meta = st.text_input(
                "Nome da meta",
                placeholder="Ex.: Notebook novo",
                max_chars=25,
                key="meta_nome"
            )

        valor_meta = st.number_input(
            "Valor da meta",
            min_value=0.01,
            max_value=1_000_000.00,
            step=50.00,
            format="%.2f",
            key="meta_valor"
        )
        data_limite = st.date_input(
            "Data limite",
            min_value=amanha,
            key="meta_data"
        )
        observacao = st.text_input(
            "Observação",
            placeholder="Ex.: Comprar na RiHappy",
            max_chars=50,
            key="meta_observacao"
        )

        if st.button("Criar meta", use_container_width=True):
            ok, msg = criar_meta(
                st.session_state.usuario,
                nome_meta,
                valor_meta,
                emoji,
                data_limite.isoformat(),
                observacao
            )

            if ok:
                st.session_state.flash_meta_criacao = ("success", msg)
                st.session_state.resetar_form_meta = True
                st.rerun()
            else:
                # O erro é desenhado no placeholder que já foi criado acima do
                # título "Metas financeiras", sem rerun e sem levar a página ao topo.
                with flash_meta_area.container():
                    render_box(
                        msg,
                        "error",
                        auto_hide=True,
                        element_id="mensagem-criacao-meta"
                    )

    metas = carregar_metas(st.session_state.usuario)

    if not metas:
        render_box("Você ainda não possui metas financeiras.", "info")
    else:
        for meta in metas:
            status = obter_status_meta(meta)
            reservado = round(float(meta.get("reservado", 0.0)), 2)
            valor_objetivo = round(float(meta["valor"]), 2)
            falta = max(round(valor_objetivo - reservado, 2), 0.0)
            progresso = 100.0 if valor_objetivo <= 0 else min((reservado / valor_objetivo) * 100, 100.0)

            if status == "concluida":
                status_texto = "✅ Meta concluída"
                status_classe = "status-concluida"
            elif status == "fracassada":
                status_texto = "❌ Meta fracassada"
                status_classe = "status-fracassada"
            else:
                status_texto = "⏳ Em andamento"
                status_classe = "status-andamento"

            nome_seguro = html.escape(str(meta["nome"]))
            emoji_seguro = html.escape(str(meta["emoji"]))
            observacao_segura = html.escape(str(meta.get("observacao", "")).strip()) or "—"

            # O card da meta ocupa menos largura e permanece alinhado à esquerda.
            # A coluna da direita concentra a reserva de fundos e a exclusão.
            coluna_meta, coluna_acoes = st.columns([3.8, 1.5], gap="medium")

            with coluna_meta:
                st.markdown(
                    f"""
                    <div class="servatio-card meta-created-card">
                        <h3>{emoji_seguro} {nome_seguro}</h3>
                        <div class="meta-status {status_classe}">{status_texto}</div>
                        <p><b>Objetivo:</b> {formatar_reais(valor_objetivo)}</p>
                        <p><b>Fundos reservados:</b> {formatar_reais(reservado)}</p>
                        <p><b>Falta reservar:</b> {formatar_reais(falta)}</p>
                        <p><b>Data limite:</b> {formatar_data(meta['data_limite'])}</p>
                        <p><b>Observação:</b> {observacao_segura}</p>
                        <div class="meta-progress-track">
                            <div class="meta-progress-fill" style="width: {progresso:.2f}%;"></div>
                        </div>
                        <div class="meta-progress-text">{progresso:.0f}% da meta reservada</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            mensagem_reserva = None
            chave_flash_reserva = f"flash_reserva_{meta['id']}"

            with coluna_acoes:
                # O container tem altura fixa: abrir/fechar a reserva não move
                # o botão de excluir, que permanece preso à parte inferior.
                with st.container(key=f"meta_actions_{meta['id']}"):
                    if status == "em_andamento":
                        fundos_livres = obter_fundos_nao_alocados(st.session_state.usuario)
                        maximo_reserva = round(min(fundos_livres, falta), 2)

                        with st.expander("💰 Reservar fundos"):
                            if maximo_reserva >= 0.01:
                                valor_padrao = min(100.00, maximo_reserva)
                                chave_valor_reserva = f"reservar_valor_{meta['id']}"

                                if chave_valor_reserva not in st.session_state:
                                    st.session_state[chave_valor_reserva] = valor_padrao

                                valor_reserva = st.number_input(
                                    "Valor a reservar",
                                    min_value=0.01,
                                    # O limite real continua sendo validado no model,
                                    # evitando que um valor inválido vire R$ 100,00.
                                    max_value=1_000_000.00,
                                    step=10.00,
                                    format="%.2f",
                                    key=chave_valor_reserva
                                )

                                st.caption(
                                    f"Disponível: {formatar_reais(fundos_livres)}"
                                )

                                if st.button(
                                    "Reservar",
                                    use_container_width=True,
                                    key=f"reservar_botao_{meta['id']}"
                                ):
                                    ok, msg = reservar_fundos(
                                        st.session_state.usuario,
                                        meta["id"],
                                        valor_reserva
                                    )

                                    if ok:
                                        st.session_state[chave_flash_reserva] = ("success", msg)
                                        st.rerun()
                                    else:
                                        mensagem_reserva = ("error", msg)
                            else:
                                st.caption("Sem fundos não-alocados disponíveis.")
                    else:
                        st.markdown(
                            '<div class="reserve-closed">💰 Reserva encerrada</div>',
                            unsafe_allow_html=True
                        )

                    with st.container(key=f"meta_delete_{meta['id']}"):
                        if st.button(
                            "🗑️ Excluir meta",
                            use_container_width=True,
                            key=f"excluir_{meta['id']}"
                        ):
                            ok, msg = excluir_meta(st.session_state.usuario, meta["id"])
                            set_flash("success" if ok else "error", msg)
                            st.rerun()

            # Os alertas de reserva continuam abaixo da área da meta, com a
            # mesma largura e posição usadas na versão anterior.
            if chave_flash_reserva in st.session_state:
                mensagem_reserva = st.session_state.pop(chave_flash_reserva)

            if mensagem_reserva:
                tipo_mensagem, texto_mensagem = mensagem_reserva
                id_mensagem = f"mensagem-reserva-{meta['id']}"
                render_box(
                    texto_mensagem,
                    tipo_mensagem,
                    auto_hide=True,
                    element_id=id_mensagem
                )
                rolar_para_elemento(id_mensagem)
