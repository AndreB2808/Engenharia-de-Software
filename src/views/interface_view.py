import streamlit as st
import html

def render_box(texto, tipo="info"):
    texto = html.escape(str(texto))
    st.markdown(
        f'<div class="msg-box msg-{tipo}">{texto}</div>',
        unsafe_allow_html=True
    )


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
            background-color: white !important;
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
            background: black !important;
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
            background-color: white !important;
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
            background: white !important;
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
        </style>
        """, unsafe_allow_html=True)
