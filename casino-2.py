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
.card-rank-top {
    position: absolute;
    top: 5px;
    left: 7px;
    font-size: 22px;
    font-weight: bold;
}
.card-suit-top {
    position: absolute;
    top: 28px;
    left: 10px;
    font-size: 20px;
}
.card-suit-center {
    position: absolute;
    top: 45%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 45px;
}
.card-rank-bottom {
    position: absolute;
    bottom: 5px;
    right: 7px;
    font-size: 22px;
    font-weight: bold;
    transform: rotate(180deg);
}
.card-suit-bottom {
    position: absolute;
    bottom: 28px;
    right: 10px;
    font-size: 20px;
    transform: rotate(180deg);
}
</style>
""", unsafe_allow_html=True)

# --- BARAJA ---
palos = ["♠", "♥", "♦", "♣"]
tipos = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
valores = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

def create_deck():
    deck = []
    for palo in palos:
        for tipo in tipos:
            deck.append({"tipo": tipo, "palo": palo, "valor": valores[tipo]})
    random.shuffle(deck)
    return deck

def draw_card(deck):
    return deck.pop() if deck else None

def calcular_puntos(mano):
    total = sum(c["valor"] for c in mano)
    ases = sum(1 for c in mano if c["tipo"] == "A")
    while total > 21 and ases > 0:
        total -= 10
        ases -= 1
    return total

def mostrar_carta(carta):
    color = "red" if carta["palo"] in ["♥", "♦"] else "black"
    return f"""
    <div class="card" style="color:{color};">
        <div class="card-rank-top">{carta['tipo']}</div>
        <div class="card-suit-top">{carta['palo']}</div>
        <div class="card-suit-center">{carta['palo']}</div>
        <div class="card-rank-bottom">{carta['tipo']}</div>
        <div class="card-suit-bottom">{carta['palo']}</div>
    </div>
    """

# --- ESTADO ---
if "deck" not in st.session_state:
    st.session_state.deck = create_deck()
if "player" not in st.session_state:
    st.session_state.player = []
if "dealer" not in st.session_state:
    st.session_state.dealer = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "started" not in st.session_state:
    st.session_state.started = False

# --- SISTEMA DE APUESTAS ---
if "saldo" not in st.session_state:
    st.session_state.saldo = 500  # saldo inicial

if "apuesta" not in st.session_state:
    st.session_state.apuesta = 0

st.title("🃏 Blackjack — Study OS Casino")

st.subheader(f"💰 Saldo: **{st.session_state.saldo}** chips")
st.write("Selecciona tu apuesta:")

colA, colB, colC, colD, colE = st.columns(5)

def apostar(cantidad):
    if st.session_state.saldo >= cantidad:
        st.session_state.apuesta = cantidad

with colA:
    if st.button("5"):
        apostar(5)
with colB:
    if st.button("10"):
        apostar(10)
with colC:
    if st.button("25"):
        apostar(25)
with colD:
    if st.button("50"):
        apostar(50)
with colE:
    if st.button("100"):
        apostar(100)

st.write(f"🎲 Apuesta seleccionada: **{st.session_state.apuesta}** chips")

# REPARTIR
if st.button("Repartir"):
    if st.session_state.apuesta == 0:
        st.warning("Debes seleccionar una apuesta antes de repartir.")
    else:
        st.session_state.saldo -= st.session_state.apuesta
        st.session_state.deck = create_deck()
        st.session_state.player = [draw_card(st.session_state.deck), draw_card(st.session_state.deck)]
        st.session_state.dealer = [draw_card(st.session_state.deck), draw_card(st.session_state.deck)]
        st.session_state.game_over = False
        st.session_state.started = True

st.subheader("Jugador:")
col1, col2 = st.columns([3, 1])

# --- BOTONES ---
with col2:
    if st.session_state.started and not st.session_state.game_over and st.session_state.player:
        puntos_jugador = calcular_puntos(st.session_state.player)

        if puntos_jugador < 21:
            if st.button("Pedir carta"):
                st.session_state.player.append(draw_card(st.session_state.deck))
                puntos_jugador = calcular_puntos(st.session_state.player)
                if puntos_jugador > 21:
                    st.session_state.game_over = True

        if st.button("Plantarse"):
            st.session_state.game_over = True

# --- IA DEL DEALER ---
if st.session_state.game_over and st.session_state.started:
    while calcular_puntos(st.session_state.dealer) < 17:
        st.session_state.dealer.append(draw_card(st.session_state.deck))

# --- CARTAS DEL JUGADOR ---
with col1:
    if st.session_state.player:
        html = "".join(mostrar_carta(c) for c in st.session_state.player)
        st.markdown(html, unsafe_allow_html=True)

# --- DEALER ---
st.subheader("Dealer:")
if st.session_state.dealer:
    html = "".join(mostrar_carta(c) for c in st.session_state.dealer)
    st.markdown(html, unsafe_allow_html=True)

# --- RESULTADO ---
if st.session_state.game_over and st.session_state.started:
    puntos_jugador = calcular_puntos(st.session_state.player)
    puntos_dealer = calcular_puntos(st.session_state.dealer)

    if puntos_jugador > 21:
        st.error("❌ Te pasaste de 21. Pierdes.")
    elif puntos_dealer > 21:
        st.success("🎉 El dealer se pasó de 21. ¡Ganas!")
        st.session_state.saldo += st.session_state.apuesta * 2
    elif puntos_jugador > puntos_dealer:
        st.success("🏆 ¡Has ganado!")
        st.session_state.saldo += st.session_state.apuesta * 2
    elif puntos_jugador < puntos_dealer:
        st.error("❌ Has perdido.")
    else:
        st.info("🤝 Empate.")
        st.session_state.saldo += st.session_state.apuesta  # devuelve apuesta

    if st.button("Jugar otra vez"):
        st.session_state.player = []
        st.session_state.dealer = []
        st.session_state.apuesta = 0
        st.session_state.started = False
        st.session_state.game_over = False

