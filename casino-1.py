import random
import time
import streamlit as st

st.title("🎰 Tragaperras Casino")
st.write("Bienvenido a mi app de prueba Streamlit.")

# Estado inicial
if "creditos" not in st.session_state:
    st.session_state.creditos = 100

if "ultimo_juego" not in st.session_state:
    st.session_state.ultimo_juego = None

simbolos = ["🍒", "🍋", "⭐", "💎", "7"]

# Mostrar créditos
st.subheader(f"Créditos disponibles: {st.session_state.creditos}")

# Campo para escribir la apuesta
apuesta_texto = st.text_input(
    "¿Cuánto quieres apostar?",
    placeholder="Escribe tu apuesta aquí"
)

# Botón para jugar
if st.button("🎲 Jugar"):
    # Validar que se ha escrito un número
    if not apuesta_texto.isdigit():
        st.error("Introduce un número válido.")
        st.stop()

    apuesta = int(apuesta_texto)

    # Validaciones
    if apuesta <= 0:
        st.warning("La apuesta debe ser mayor que 0.")
        st.stop()

    if apuesta > st.session_state.creditos:
        st.error("No tienes suficientes créditos.")
        st.stop()

    # Aplicar apuesta
    st.session_state.creditos -= apuesta

    # Tirada
    resultado = [random.choice(simbolos) for _ in range(3)]
    st.session_state.ultimo_juego = resultado

    st.write("**Girando...**")
    st.write(" | ".join(resultado))

    # Reglas de premios
    if resultado[0] == resultado[1] == resultado[2]:
        premio = apuesta * 5
        st.session_state.creditos += premio
        st.success(f"🎉 ¡JACKPOT! Ganas {premio} créditos.")
    elif resultado[0] == resultado[1] or resultado[1] == resultado[2] or resultado[0] == resultado[2]:
        premio = apuesta * 2
        st.session_state.creditos += premio
        st.info(f"✨ ¡Dos iguales! Ganas {premio} créditos.")
    else:
        st.write("😢 No has ganado esta vez.")

    # Esperar 5 segundos y reiniciar
    time.sleep(5)
    st.experimental_rerun()

# Mostrar último resultado si existe
if st.session_state.ultimo_juego:
    st.write("Último resultado:")
    st.write(" | ".join(st.session_state.ultimo_juego))

# Fin del juego
if st.session_state.creditos <= 0:
    st.error("Te has quedado sin créditos. Fin del juego.")
