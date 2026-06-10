import random

# Créditos iniciales
creditos = 100
#baraja de cartas y valores para blackjack

import random

# Definimos palos y rangos
suits = ["♠", "♥", "♦", "♣"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

# Valores para blackjack
values = {
    "A": 11,   # luego puedes tratarlo como 1 si te pasas de 21
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}

def create_deck():

   # Crea una baraja estándar de 52 cartas para blackjack.
    deck = []
    for suit in suits:
        for rank in ranks:
            card = {
                "rank": rank,
                "suit": suit,
                "value": values[rank]
            }
            deck.append(card)
    random.shuffle(deck)
    return deck

def draw_card(deck):
    """Roba una carta de la baraja."""
    return deck.pop() if deck else None

# Ejemplo de uso
if __name__ == "__main__":
    deck = create_deck()
    player_hand = [draw_card(deck), draw_card(deck)]
    dealer_hand = [draw_card(deck), draw_card(deck)]

    print("Player:", player_hand)
    print("Dealer:", dealer_hand)
