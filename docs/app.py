import random

def card_value(card):
    if card in ['Jack', 'Queen', 'King']:
        return 0.5
    elif card == 'Ace':
        return 1
    else:
        return int(card)

def draw_card(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card

def play_game(chips, bet):
    cards = ['Ace', '2', '3', '4', '5', '6', '7', 'Jack', 'Queen', 'King'] * 4
    random.shuffle(cards)

    player_hand = []
    dealer_hand = []
    player_score = 0
    dealer_score = 0

    bonus_card = draw_card(cards)

    for _ in range(2):
        card = draw_card(cards)
        dealer_hand.append(card)
        dealer_score += card_value(card)

    card = draw_card(cards)
    player_hand.append(card)
    player_score += card_value(card)

    if dealer_score > 7.5:
        chips += bet
        message = "The dealer exceeded 7.5, you win!"
        prize = random.randint(50, 1000)
        chips += prize
        message += f" You won a prize of {prize} chips!"
    elif player_score == 7.5:
        chips += bet
        message = "You got 7.5, you win!"
        prize = random.randint(50, 1000)
        chips += prize
        message += f" You won a prize of {prize} chips!"
        if bonus_card in player_hand:
            bonus = bet * 2
            chips += bonus
            message += f" You have the bonus card {bonus_card} and win a bonus of {bonus} chips!"
    else:
        if player_score < dealer_score:
            chips -= bet
            message = "You lose! Keep trying!"
        else:
            chips += bet
            message = "You win!"
            prize = random.randint(50, 1000)
            chips += prize
            message += f" You won a prize of {prize} chips!"
            if bonus_card in player_hand:
                bonus = bet * 2
                chips += bonus
                message += f" You have the bonus card {bonus_card} and win a bonus of {bonus} chips!"

    return chips, message
