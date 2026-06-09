import random
import streamlit as st

st.title("🎰 Tragaperras Casino")
st.write("Bienvenido a mi app de prueba Streamlit.")

# Créditos iniciales
creditos = 100

simbolos = ["🍒", "🍋", "⭐", "💎", "7"]

print("=== CASINO PYTHON ===")
print(f"Empiezas con {creditos} créditos.")

while creditos > 0:
    print(f"\nCréditos disponibles: {creditos}")

    try:
        apuesta = int(input("¿Cuánto quieres apostar? (0 para salir): "))
    except ValueError:
        print("Introduce un número válido.")
        continue

    if apuesta == 0:
        print("Gracias por jugar.")
        break

    if apuesta > creditos or apuesta < 0:
        print("Apuesta no válida.")
        continue

    creditos -= apuesta

    # Tirada de la tragamonedas
    resultado = [random.choice(simbolos) for _ in range(3)]

    print("\nGirando...")
    print(" | ".join(resultado))

    # Reglas de premios
    if resultado[0] == resultado[1] == resultado[2]:
        premio = apuesta * 5
        creditos += premio
        print(f"¡JACKPOT! Ganas {premio} créditos.")
    elif resultado[0] == resultado[1] or resultado[1] == resultado[2] or resultado[0] == resultado[2]:
        premio = apuesta * 2
        creditos += premio
        print(f"¡Dos iguales! Ganas {premio} créditos.")
    else:
        print("No has ganado esta vez.")

if creditos <= 0:
    print("\nTe has quedado sin créditos. Fin del juego.")





