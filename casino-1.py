import random
import time
import streamlit as st

st.set_page_config(page_title="Test Your Luck", layout="centered")

# --- ESTILOS ---
st.markdown("""
<style>

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

/* CAJAS EN GRIS METÁLICO */
.cs2-box {
    display: inline-block;
    background: linear-gradient(145deg, #d9d9d9, #bfbfbf);
    border: 3px solid #00eaff;
    border-radius: 10px;
    padding: 15px 25px;
    margin: 5px;
    font-size: 45px;
    position: relative;
    z-index: 2;
    box-shadow: 0px 0px 15px #00eaffaa;
}

/* CONTENEDOR PARA SUPERPOSICIÓN */
.symbol-container {
    position: relative;
    display: inline-block;
}

/* LÍNEA QUE ATRAVIESA LOS OBJETOS (color dinámico) */
.line-through {
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 4px;
    z-index: 5;
    transform: translateY(-50%);
    border-radius: 2px;
}

/* TEXTO WIN / LOOSE */
.result-text {
    font-size: 28px;
    font-weight: bold;
    margin-top: 15px;
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

# MÁS OBJETOS
simbolos = ["🍒", "🍋", "⭐", "💎", "🍀", "🔥", "🍉", "🔔", "💰", "🎲"]

# --- MÁQUINA ---
st.markdown('<div class="machine">', unsafe_allow_html=True)

st.markdown('<div class="title-bar">🎰 TEST YOUR LUCK</div>', unsafe_allow_html=True)

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

    # --- ANIMACIÓN ---
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

    # Determinar si gana
    if resultado[0] == resultado[1] == resultado[2]:
        mensaje = "WIN"
        color_linea = "#00ff55"   # verde
        color_texto = "#00ff55"
    elif resultado[0] == resultado[1] or resultado[1] == resultado[2] or resultado[0] == resultado[2]:
        mensaje = "WIN"
        color_linea = "#00ff55"   # verde
        color_texto = "#00ff55"
    else:
        mensaje = "LOOSE"
        color_linea = "#ff0033"   # rojo
        color_texto = "#ff0033"

    # Construcción visual final con línea atravesando los símbolos
    final_html = (
        f'<div class="symbol-container">'
        f'<div class="line-through" style="background:{color_linea};"></div>' +
        "".join(f'<span class="cs2-box">{s}</span>' for s in resultado) +
        '</div>' +
        f'<div class="result-text" style="color:{color_texto};">{mensaje}</div>'
    )

    pantalla.markdown(f'<div class="screen">{final_html}</div>', unsafe_allow_html=True)

    # Premios
    if mensaje == "WIN":
        premio = apuesta * 2
        st.session_state.creditos += premio
        st.success(f"🎉 WIN! +{premio}")
    else:
        st.write("😢 LOOSE")

    time.sleep(5)
    st.rerun()

# Último resultado
if st.session_state.ultimo_juego:
    st.write("Último resultado:")
    st.write(" | ".join(st.session_state.ultimo_juego))

st.markdown('</div>', unsafe_allow_html=True)


