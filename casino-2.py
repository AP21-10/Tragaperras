import random
import streamlit as st

st.set_page_config(page_title="Blackjack", layout="centered")

# --- ESTILOS VISUALES ---
st.markdown("""
<style>
.card {
    display: inline-flex;
    justify-content: center;
    align-items: center;

    background: white;
    border-radius: 10px;
    margin: 5px;

    width: 90px;      /* ancho fijo */
    height: 120px;    /* alto fijo */

    font-size: 35px;
    font-weight: bold;
    border: 3px solid #000;
    text-align: center;

    line-height: 1;   /* evita que el 10 se parta */
}
</style>
""", unsafe_allow_html=True)

# --- DEFINICIÓN DE BARAJA ---
palos = ["♠", "♥", "♦", "♣"]
tipos = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

valores = {
    "A": 11,
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 10, "Q": 10, "K": 10
}

def create_deck():
    deck = []
    for palo in palos:
        for tipo in tipos:
            deck.append({
                "tipo": tipo,
                "palo": palo,
                "valor": valores[tipo]
            })
    random.shuffle(deck)
    return deck

def draw_card(deck):
    return deck.pop() if deck else None

def mostrar_carta(carta):
    # Palos rojos
    if carta["palo"] in ["♥", "♦"]:
        color = "red"
    else:
        color = "black"

    return f"<span class='card' style='color:{color};'>{carta['tipo']}{carta['palo']}</span>"

# --- ESTADO ---
if "deck" not in st.session_state:
    st.session_state.deck = create_deck()

if "player" not in st.session_state:
    st.session_state.player = []

if "dealer" not in st.session_state:
    st.session_state.dealer = []

# --- INTERFAZ ---
st.title("🃏 Blackjack — Study OS Casino")

if st.button("Repartir cartas"):
    st.session_state.deck = create_deck()
    st.session_state.player = [draw_card(st.session_state.deck), draw_card(st.session_state.deck)]
    st.session_state.dealer = [draw_card(st.session_state.deck), draw_card(st.session_state.deck)]

# --- MOSTRAR MANOS ---
st.subheader("Jugador:")
if st.session_state.player:
    st.markdown("".join(mostrar_carta(c) for c in st.session_state.player), unsafe_allow_html=True)

st.subheader("Dealer:")
if st.session_state.dealer:
    st.markdown("".join(mostrar_carta(c) for c in st.session_state.dealer), unsafe_allow_html=True)

