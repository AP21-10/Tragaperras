import random
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

# Elegir apuesta
apuesta = st.number_input("¿Cuánto quieres apostar?", min_value=0, max_value=st.session_state.creditos, step=1)

# Botón para jugar
if st.button("🎲 Jugar"):
    if apuesta == 0:
        st.warning("Introduce una apuesta mayor que 0 para jugar.")
    elif apuesta > st.session_state.creditos:
        st.error("No tienes suficientes créditos.")
    else:
        st.session_state.creditos -= apuesta
        resultado = [random.choice(simbolos) for _ in range(3)]
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
# Fin del juego
if st.session_state.creditos <= 0:
    st.error("Te has quedado sin créditos. Fin del juego.")





