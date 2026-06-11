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
.card-back {
    width: 90px;
    height: 130px;
    background: linear-gradient(45deg, #b30000, #660000);
    border-radius: 10px;
    border: 3px solid #000;
    margin: 6px;
    display: inline-block;
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

/* CHIPS REALISTAS */
.chip-btn {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    border: 4px solid white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 26px;
    font-weight: bold;
    color: white;
    cursor: pointer;
    margin: auto;
    box-shadow: 0px 0px 10px #00000055;
}
.chip-red { background: #d40000; }
.chip-blue { background: #0044cc; }
.chip-green { background: #009933; }
.chip-black { background: #111; }
.chip-purple { background: #6a0dad; }
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

def carta_oculta():
    return """<div class="card-back"></div>"""

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
if "saldo" not in st.session_state:
    st.session_state.saldo = 500
if "apuesta" not in st.session_state:
    st.session_state.apuesta = 0
if "apuesta_realizada" not in st.session_state:
    st.session_state.apuesta_realizada = False

st.title("🃏 Blackjack — Study OS Casino")

# --- REPARTIR FLOP ---
if st.button("Repartir (Flop)"):
    st.session_state.deck = create_deck()
    st.session_state.player = [draw_card(st.session_state.deck), draw_card(st.session_state.deck)]
    st.session_state.dealer = [draw_card(st.session_state.deck), draw_card(st.session_state.deck)]
    st.session_state.started = True
    st.session_state.game_over = False
    st.session_state.apuesta_realizada = False
    st.session_state.apuesta = 0

# --- MOSTRAR CARTAS DEL JUGADOR ---
st.subheader("Jugador:")
if st.session_state.player:
    html = "".join(mostrar_carta(c) for c in st.session_state.player)
    st.markdown(html, unsafe_allow_html=True)

# --- APUESTA DESPUÉS DEL FLOP ---
if st.session_state.started and not st.session_state.apuesta_realizada:
    st.subheader("💰 Selecciona tu apuesta:")

    cols = st.columns(5)

    chips = [
        (5, "chip-red"),
        (10, "chip-blue"),
        (25, "chip-green"),
        (50, "chip-black"),
        (100, "chip-purple")
    ]

    for i, (valor, clase) in enumerate(chips):
        with cols[i]:
            if st.button(
                f"<div class='chip-btn {clase}'>{valor}</div>",
                key=f"chip{valor}",
                help=f"Apostar {valor} chips",
                use_container_width=True
            ):
                if st.session_state.saldo >= valor:
                    st.session_state.apuesta = valor
                    st.session_state.saldo -= valor
                    st.session_state.apuesta_realizada = True

    st.write(f"🎲 Apuesta: **{st.session_state.apuesta}** chips")

# --- DEALER ---
st.subheader("Dealer:")

if st.session_state.dealer:
    if not st.session_state.game_over:
        html = mostrar_carta(st.session_state.dealer[0]) + carta_oculta()
    else:
        html = "".join(mostrar_carta(c) for c in st.session_state.dealer)

    st.markdown(html, unsafe_allow_html=True)

# --- BOTONES DE ACCIÓN ---
if st.session_state.apuesta_realizada and not st.session_state.game_over:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Pedir carta"):
            st.session_state.player.append(draw_card(st.session_state.deck))
            if calcular_puntos(st.session_state.player) > 21:
                st.session_state.game_over = True

    with col2:
        if st.button("Plantarse"):
            st.session_state.game_over = True

# --- IA DEL DEALER ---
if st.session_state.game_over and st.session_state.started:
    while calcular_puntos(st.session_state.dealer) < 17:
        st.session_state.dealer.append(draw_card(st.session_state.deck))

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
        st.session_state.saldo += st.session_state.apuesta

    if st.button("Jugar otra vez"):
        st.session_state.started = False
        st.session_state.game_over = False
        st.session_state.player = []
        st.session_state.dealer = []
        st.session_state.apuesta = 0
        st.session_state.apuesta_realizada = 
