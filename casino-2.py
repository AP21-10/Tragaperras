import random
import streamlit as st

st.set_page_config(page_title="Blackjack", layout="centered")

# --- ESTILOS DE CARTAS REALISTAS ---
st.markdown("""
<style>
.card {
    width: 90px;
    height: 130px;
    background: white;
    border-radius: 10px;
    border: 3px solid #000;
    margin: 6px;
    display: inline-block;
    position: relative;
    font-family: 'Arial', sans-serif;
}

/* Número arriba */
.card-rank-top {
    position: absolute;
    top: 5px;
    left: 7px;
    font-size: 22px;
    font-weight: bold;
}

/* Palo arriba */
.card-suit-top {
    position: absolute;
    top: 28px;
    left: 10px;
    font-size: 20px;
}

/* Palo grande centro */
.card-suit-center {
    position: absolute;
    top: 45%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 45px;
}

/* Número abajo invertido */
.card-rank-bottom {
    position: absolute;
    bottom: 5px;
    right: 7px;
    font-size: 22px;
    font-weight: bold;
    transform: rotate(180deg);
}

/* Palo abajo invertido */
.card-suit-bottom {
    position: absolute;
    bottom: 28px;
    right: 10px;
    font-size: 20px;
    transform: rotate(180deg);
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

# --- FUNCIÓN PARA MOSTRAR CARTA REALISTA ---
def mostrar_carta(carta):
    color = "red" if carta["palo"] in ["♥", "♦"] else "black"

    html = f"""
    <div class="card" style="color:{color};">
        <div class="card-rank-top">{carta['tipo']}</div>
        <div class="card-suit-top">{carta['palo']}</div>
        <div class="card-suit-center">{carta['palo']}</div>
        <div class="card-rank-bottom">{carta['tipo']}</div>
        <div class="card-suit-bottom">{carta['palo']}</div>
    </div>
    """
    return html

# --- ESTADO ---
if "deck" not in st.session_state:
    st.session_state.deck = create_deck()

if "player" not in st.session_state:
    st.session_state.player = []

if "dealer" not in st.session_state:
    st.session_state.dealer = []

# --- INTERFAZ ---
st.title("🃏 Blackjack — Study OS Casino")

# BOTÓN REPARTIR
if st.button("Repartir"):
    st.session_state.deck = create_deck()
    st.session_state.player = [draw_card(st.session_state.deck), draw_card(st.session_state.deck)]
    st.session_state.dealer = [draw_card(st.session_state.deck), draw_card(st.session_state.deck)]

# BOTÓN HIT (PEDIR CARTA)
if st.button("Pedir carta"):
    if st.session_state.deck:
        st.session_state.player.append(draw_card(st.session_state.deck))

# BOTÓN STAND (PLANTARSE)
if st.button("Plantarse"):
    st.write("Te has plantado. (Aquí luego añadimos la lógica del dealer)")

# --- MOSTRAR MANOS ---
st.subheader("Jugador:")
if st.session_state.player:
    cartas_html = "".join([mostrar_carta(c) for c in st.session_state.player])
    st.markdown(cartas_html, unsafe_allow_html=True)

st.subheader("Dealer:")
if st.session_state.dealer:
    cartas_html = "".join([mostrar_carta(c) for c in st.session_state.dealer])
    st.markdown(cartas_html, unsafe_allow_html=True)


