import random
import time
import streamlit as st

st.set_page_config(page_title="Test Your Luck", layout="centered")

# --- ESTILOS DE MÁQUINA REAL + DISPLAY CS2 ---
st.markdown("""
<style>

.machine {
    border: 8px solid #8b0000;
    border-radius: 25px;
    padding: 25px;
    background: linear-gradient(to bottom, #3a0000, #0d0000);
    box-shadow: 0px 0px 40px #ff0000aa;
    max-width: 500px;
    margin: auto;
}

.title-bar {
    background: linear-gradient(to right, #66ccff, #99ddff);
    color: #000;
    font-size: 36px;
    font-weight: bold;
    text-align: center;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 25px;
    box-shadow: 0px 0px 15px #66ccff;
}

.screen {
    background: #0a0a0a;
    padding: 25px;
    border-radius: 15px;
    border: 4px solid #444;
    margin-bottom: 20px;
    text-align: center;
}

/* Caja normal (color claro) */
.cs2-box {
    display: inline-block;
    background: linear-gradient(145deg, #d9d9d9, #bfbfbf); /* gris claro */
    border: 3px solid #00eaff;
    border-radius: 10px;
    padding: 15px 25px;
    margin: 5px;
    font-size: 45px;
    box-shadow: 0px 0px 15px #00eaffaa;
}

/* Caja especial para el 7 (más ancha y dorada) */
.cs2-box-seven {
    display: inline-block;
    background: linear-gradient(145deg, #ffd966, #ffcc33); /* dorado */
    border: 4px solid #ffaa00;
    border-radius: 12px;
    padding: 15px 40px; /* más ancha */
    margin: 5px;
    font-size: 50px;
    box-shadow: 0px 0px 20px #ffcc33aa;
}

.button-play {
    background-color: #ffcc00;
    color: black;
    font-size: 28px;
    padding: 15px;
    border-radius: 12px;
    width: 100%;
    border: 4px solid #b38f00;
    cursor: pointer;
}

.button-play:hover {
    background-color: #ffe680;
}

</style>
""", unsafe_allow_html=True)

# --- ESTADO ---
if "creditos" not in st.session_state:
    st.session_state.creditos = 100
if "ultimo_juego" not in st.session_state:
    st.session_state.ultimo_juego = None

simbolos = ["🍒", "🍋", "
