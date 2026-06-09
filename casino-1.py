import random
import time
import streamlit as st

st.set_page_config(page_title="Tragaperras", layout="centered")

# --- ESTILOS DE MÁQUINA REAL ---
st.markdown("""
<style>
.machine {
    border: 6px solid #b30000;
    border-radius: 20px;
    padding: 20px;
    background: linear-gradient(to bottom, #4d0000, #1a0000);
    box-shadow: 0px 0px 25px #ff0000;
}
.screen {
    background: black;
    color: #00ff00;
    font-size: 40px;
    text-align: center;
    padding: 20px;
    border-radius: 10px;
    border: 4px solid #333;
    margin-bottom: 20px;
}
.button-play {
    background-color: #ffcc00;
    color: black;
    font-size: 28px;
    padding: 15px;
    border-radius: 10px;
    width: 100%;
    border: 3px solid #b38f00;
}
.lights {
    text-align: center;
    font-size: 25px;
    margin-bottom: 10px;
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

st.markdown('<div class="lights">🔴 🟡 🔵 🟢 🔵 🟡 🔴</div>', unsafe_allow_html=True)

st.title("🎰 TRAGAPERRAS DELUXE")

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

# --- PANTALLA DE LA MÁQUINA ---
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

    # --- ANIMACIÓN PREMIUM ---
    for _ in range(12):
        columna = "\n".join(random.choice(simbolos) for _ in range(5))
        pantalla.markdown(f'<div class="screen">{columna}</div>', unsafe_allow_html=True)
        time.sleep(0.08)

    # Resultado final
    resultado = [random.choice(simbolos) for _ in range(3)]
    st.session_state.ultimo_juego = resultado

    pantalla.markdown(
        f'<div class="screen">{resultado[0]} | {resultado[1]} | {resultado[2]}</div>',
        unsafe_allow_html=True
    )

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

