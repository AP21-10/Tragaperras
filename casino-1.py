import random
import time
import streamlit as st

st.set_page_config(page_title="Test Your Luck", layout="centered")

# --- ESTILOS DE MÁQUINA REAL + DISPLAY CS2 ---
st.markdown("""
<style>

.screen {
    background: #0a0a0a;
    padding: 25px;
    border-radius: 15px;
    border: 4px solid #444;
    margin-bottom: 20px;
    text-align: center;
}

.cs2-box {
    display: inline-block;
    background: linear-gradient(145deg, #1a1a1a, #000000);
    border: 3px solid #00eaff;
    border-radius: 10px;
    padding: 15px 20px;
    margin: 5px;
    font-size: 45px;
    box-shadow: 0px 0px 15px #00eaffaa;
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

simbolos = ["🍒", "🍋", "⭐", "💎", "7"]

# --- MÁQUINA ---
st.markdown('<div class="machine">', unsafe_allow_html=True)

st.title("🎰 TEST YOUR LUCK")

st.subheader(f"Créditos: {st.session_state.creditos}")

# Si no hay créditos → depósito
if st.session_state.creditos <= 0:
    st.error("Sin créditos. Deposita para continuar.")
    deposito = st.text_input("💰 Cantidad a depositar:", placeholder="Ej: 100")
    if st.button("💵 Depositar"):
        if deposito.isdigit() and int(deposito) > 0:
            st.session_state.creditos = int(deposito)
            st.success("Depósito realizado.")
            time.sleep(1)
            st.rerun()
        else:
            st.warning("Introduce un número válido.")
    st.stop()

# Apuesta
apuesta_texto = st.text_input("¿Cuánto quieres apostar?", placeholder="Escribe tu apuesta")

# Botón jugar
jugar = st.button("🎲 JUGAR", key="play_button")

# --- PANTALLA ---
pantalla = st.empty()

if jugar:
    if not apuesta_texto.isdigit():
        pantalla.markdown('<div class="screen">❌ Apuesta inválida</div>', unsafe_allow_html=True)
        st.stop()

    apuesta = int(apuesta_texto)

    if apuesta <= 0:
        pantalla.markdown('<div class="screen">⚠ Apuesta > 0</div>', unsafe_allow_html=True)
        st.stop()

    if apuesta > st.session_state.creditos:
        pantalla.markdown('<div class="screen">❌ Sin créditos suficientes</div>', unsafe_allow_html=True)
        st.stop()

    st.session_state.creditos -= apuesta

    # --- ANIMACIÓN PREMIUM TIPO CS2 ---
    for _ in range(12):
        columna = "".join(
            f'<span class="cs2-box">{random.choice(simbolos)}</span>'
            for _ in range(3)
        )
        pantalla.markdown(f'<div class="screen">{columna}</div>', unsafe_allow_html=True)
        time.sleep(0.08)

    # Resultado final
    resultado = [random.choice(simbolos) for _ in range(3)]
    st.session_state.ultimo_juego = resultado

    final_html = "".join(f'<span class="cs2-box">{s}</span>' for s in resultado)
    pantalla.markdown(f'<div class="screen">{final_html}</div>', unsafe_allow_html=True)

    # Premios
    if resultado[0] == resultado[1] == resultado[2]:
        premio = apuesta * 5
        st.session_state.creditos += premio
        st.success(f"🎉 JACKPOT! +{premio}")
    elif resultado[0] == resultado[1] or resultado[1] == resultado[2] or resultado[0] == resultado[2]:
        premio = apuesta * 2
        st.session_state.creditos += premio
        st.info(f"✨ Dos iguales! +{premio}")
    else:
        st.write("😢 No has ganado esta vez.")

    time.sleep(5)
    st.rerun()

# Último resultado
if st.session_state.ultimo_juego:
    st.write("Último resultado:")
    st.write(" | ".join(st.session_state.ultimo_juego))

st.markdown('</div>', unsafe_allow_html=True)
