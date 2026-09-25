import html
import streamlit as st


def render_box(texto, tipo="info", auto_hide=False, element_id=None):
    texto = html.escape(str(texto))
    classe_auto_hide = " msg-auto-hide" if auto_hide else ""
    atributo_id = f' id="{html.escape(str(element_id), quote=True)}"' if element_id else ""
    st.markdown(
        f'<div{atributo_id} class="msg-box msg-{tipo}{classe_auto_hide}">{texto}</div>',
        unsafe_allow_html=True
    )


def formatar_reais(valor):
    valor_formatado = f"{float(valor):,.2f}"
    valor_formatado = valor_formatado.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {valor_formatado}"


def formatar_data(data_iso):
    partes = str(data_iso).split("-")
    if len(partes) == 3:
        return f"{partes[2]}/{partes[1]}/{partes[0]}"
    return str(data_iso)


def aplicar_tema():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root,
    html,
    body,
    .stApp {
        color-scheme: light !important;
    }

    .stApp {
        background: linear-gradient(135deg, #FEA362 0%, #FE834D 100%);
        font-family: "Plus Jakarta Sans", "Segoe UI", sans-serif;
    }

    /* Espaço extra para o cabeçalho não ficar sob a barra superior do Streamlit. */
    .block-container {
        max-width: 900px;
        padding-top: 5.25rem !important;
        padding-bottom: 3rem;
    }

    /* Não aplicar fonte em todos os spans/divs: isso quebrava os ícones do Streamlit. */
    .stApp p,
    .stApp label,
    .stApp li,
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp input,
    .stApp textarea,
    .stApp button {
        font-family: "Plus Jakarta Sans", "Segoe UI", sans-serif;
    }

    .stApp p,
    .stApp label,
    .stApp li,
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4 {
        color: #FFFFFF;
    }

    /* Preserva a fonte de ícones usada pelo Streamlit nas setas e no botão de senha. */
    span[data-testid="stIconMaterial"],
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
        font-weight: normal !important;
        font-style: normal !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        font-feature-settings: "liga" !important;
        -webkit-font-feature-settings: "liga" !important;
        -webkit-font-smoothing: antialiased !important;
    }

    /* Mantém todos os campos sempre claros. */
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input,
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #FFFFFF !important;
        color: #3A2A24 !important;
        border-radius: 12px !important;
        -webkit-text-fill-color: #3A2A24 !important;
    }

    div[data-testid="stTextInput"] > div,
    div[data-testid="stNumberInput"] > div,
    div[data-testid="stDateInput"] > div,
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] span,
    div[data-testid="stNumberInput"] button,
    div[data-testid="stDateInput"] button {
        color: #3A2A24 !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    div[role="dialog"] {
        color-scheme: light !important;
    }

    ul[role="listbox"],
    li[role="option"],
    div[role="dialog"] {
        background-color: #FFFFFF !important;
        color: #3A2A24 !important;
    }

    li[role="option"] span,
    div[role="dialog"] span,
    div[role="dialog"] button,
    div[role="dialog"] div {
        color: #3A2A24 !important;
    }

    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.13);
        border: 1px solid rgba(255, 255, 255, 0.35);
        border-radius: 16px;
    }

    .stButton > button {
        background-color: #FE834D;
        color: #FFFFFF;
        border: 2px solid #FFDAE2;
        border-radius: 12px;
        font-weight: 700;
    }

    .stButton > button:hover {
        background-color: #FFFFFF;
        color: #FE834D;
        border-color: #FFFFFF;
    }

    .servatio-card {
        background: rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.35);
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        backdrop-filter: blur(8px);
    }

    .brand-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        margin-bottom: 8px;
    }

    .brand-logo {
        width: 82px;
        height: 82px;
        object-fit: contain;
        filter: drop-shadow(0 6px 12px rgba(120, 52, 29, 0.18));
    }

    .brand-title {
        color: #FFDAE2 !important;
        font-size: 3.2rem;
        line-height: 1;
        font-weight: 800;
        letter-spacing: -1.5px;
    }

    .brand-subtitle {
        max-width: 650px;
        margin: 6px auto 28px auto;
        padding: 15px 22px 17px 22px;
        text-align: center;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(124, 53, 30, 0.08);
        backdrop-filter: blur(6px);
    }

    .subtitle-main {
        display: block;
        color: #FFFFFF !important;
        font-size: 1.18rem;
        font-weight: 800;
        letter-spacing: -0.2px;
        margin-bottom: 4px;
    }

    .subtitle-detail {
        display: block;
        color: #FFF4F7 !important;
        font-size: 0.94rem;
        font-weight: 500;
        line-height: 1.45;
        opacity: 0.95;
    }

    .prototype-nav {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        margin: 2px auto 24px auto;
    }

    .prototype-nav-button {
        font-family: "Plus Jakarta Sans", "Segoe UI", sans-serif;
        border-radius: 999px;
        padding: 9px 16px;
        font-size: 0.88rem;
        font-weight: 700;
        border: 1px solid rgba(255, 255, 255, 0.55);
        box-shadow: 0 5px 14px rgba(101, 43, 24, 0.08);
    }

    .prototype-nav-active {
        background: #FFFFFF;
        color: #FE834D;
        border-color: #FFFFFF;
    }

    .prototype-nav-disabled {
        background: rgba(105, 94, 90, 0.28);
        color: rgba(255, 255, 255, 0.58);
        border-color: rgba(255, 255, 255, 0.22);
        cursor: not-allowed;
        opacity: 0.72;
    }

    .patrimonio-label {
        font-size: 1rem;
        opacity: 0.9;
        margin-bottom: 4px;
        color: #FFFFFF !important;
    }

    .patrimonio-valor {
        font-size: 2.1rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 14px;
    }

    .fundos-label {
        font-size: 0.9rem;
        color: #FFF4F7 !important;
        opacity: 0.92;
        margin-bottom: 2px;
    }

    .fundos-valor {
        font-size: 1.3rem;
        font-weight: 800;
        color: #FFFFFF !important;
    }

    /* Cards de metas ficam um pouco mais compactos horizontalmente;
       a altura fixa serve de referência para a coluna de ações ao lado. */
    .meta-created-card {
        min-height: 350px;
        margin-bottom: 0;
    }

    .meta-created-card .meta-progress-track {
        width: 92%;
        max-width: 100%;
    }

    /* Ações laterais de cada meta: reserva no topo e exclusão sempre embaixo. */
    div[class*="st-key-meta_actions_"] {
        position: relative !important;
        height: 350px !important;
        min-height: 350px !important;
        overflow: visible !important;
    }

    div[class*="st-key-meta_actions_"] div[data-testid="stExpander"] {
        max-height: 280px;
        overflow-y: auto;
        overflow-x: hidden;
        background: rgba(255, 255, 255, 0.13);
    }

    div[class*="st-key-meta_actions_"] div[data-testid="stExpander"] details {
        max-height: 278px;
    }

    div[class*="st-key-meta_delete_"] {
        position: absolute !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100% !important;
        z-index: 5;
    }

    .reserve-closed {
        width: 100%;
        padding: 10px 12px;
        border-radius: 14px;
        text-align: center;
        font-size: 0.82rem;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.82) !important;
        background: rgba(255, 255, 255, 0.10);
        border: 1px solid rgba(255, 255, 255, 0.28);
    }

    .meta-status {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 800;
        margin: 2px 0 10px 0;
    }

    .status-andamento {
        background: rgba(255, 244, 207, 0.92);
        color: #765B00 !important;
    }

    .status-concluida {
        background: rgba(220, 247, 228, 0.95);
        color: #1D6A3B !important;
    }

    .status-fracassada {
        background: rgba(249, 223, 227, 0.95);
        color: #8C1F2F !important;
    }

    .meta-progress-track {
        width: 100%;
        height: 11px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.28);
        overflow: hidden;
        margin: 8px 0 4px 0;
    }

    .meta-progress-fill {
        height: 100%;
        border-radius: 999px;
        background: #FFDAE2;
    }

    .meta-progress-text {
        color: #FFFFFF !important;
        font-size: 0.84rem;
        font-weight: 700;
        opacity: 0.95;
    }

    .msg-box {
        width: 100%;
        margin: 0 auto 16px auto;
        padding: 12px 14px;
        border-radius: 12px;
        text-align: center;
        font-weight: 700;
        border: 1px solid rgba(255,255,255,0.55);
        color: #FFFFFF !important;
    }

    .msg-success { background-color: rgba(31, 107, 65, 0.78); }
    .msg-error { background-color: rgba(145, 40, 55, 0.82); }
    .msg-warning { background-color: rgba(135, 101, 0, 0.82); }
    .msg-info { background-color: rgba(44, 85, 120, 0.80); }

    /* Mensagens temporárias, como a confirmação ao reservar fundos. */
    .msg-auto-hide {
        animation: servatioHideMessage 0.30s ease 2.70s forwards;
        overflow: hidden;
    }

    @keyframes servatioHideMessage {
        to {
            opacity: 0;
            visibility: hidden;
            max-height: 0;
            margin-top: 0;
            margin-bottom: 0;
            padding-top: 0;
            padding-bottom: 0;
            border-width: 0;
        }
    }

    @media (max-width: 640px) {
        .block-container {
            padding-top: 5rem !important;
        }

        .brand-logo {
            width: 68px;
            height: 68px;
        }

        .brand-title {
            font-size: 2.55rem;
        }

        .brand-subtitle {
            padding-left: 14px;
            padding-right: 14px;
        }

        .prototype-nav {
            gap: 7px;
        }

        .prototype-nav-button {
            padding: 8px 11px;
            font-size: 0.78rem;
        }

        .meta-created-card {
            min-height: auto;
        }

        div[class*="st-key-meta_actions_"] {
            height: auto !important;
            min-height: 0 !important;
        }

        div[class*="st-key-meta_delete_"] {
            position: static !important;
            margin-top: 10px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
