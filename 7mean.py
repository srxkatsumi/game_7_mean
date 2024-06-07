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

def play_seven_and_a_half():
    deck = ['Ace', '2', '3', '4', '5', '6', '7', 'Jack', 'Queen', 'King'] * 4
    chips = 300
    minimum_bet = 50

    while chips >= minimum_bet:
        random.shuffle(deck)
        
        player_hand = []
        dealer_hand = []
        player_score = 0
        dealer_score = 0

        # Bet
        while True:
            bet = int(input(f"You have {chips} chips. How much do you want to bet (minimum {minimum_bet})? "))
            if bet >= minimum_bet and bet <= chips:
                break
            else:
                print("Invalid bet. Try again.")

        # Draw the bonus card
        bonus_card = draw_card(deck)
        print(f"Bonus card for this round: {bonus_card}")

        # Dealer receives two cards
        for _ in range(2):
            card = draw_card(deck)
            dealer_hand.append(card)
            dealer_score += card_value(card)

        # Player receives one card
        card = draw_card(deck)
        player_hand.append(card)
        player_score += card_value(card)

        print("\nDealer's hand:", dealer_hand)
        print("Dealer's score:", dealer_score)
        
        if dealer_score > 7.5:
            print("The dealer exceeded 7.5, you win!")
            chips += bet
            continue
        
        if player_score == 7.5:
            print("\nYour hand:", player_hand)
            print("Score:", player_score)
            print("You got 7.5, you win!")
            chips += bet
            continue

        while True:
            print("\nYour hand:", player_hand)
            print("Score:", player_score)
            
            if player_score >= 7.5:
                break
            
            choice = input("Do you want to draw a card? (y/n): ").lower()
            
            if choice == 'y':
                card = draw_card(deck)
                player_hand.append(card)
                player_score += card_value(card)
            else:
                break
        
        if player_score > 7.5:
            print("\nYou exceeded 7.5, you lose!")
            chips -= bet
            print("Keep trying!")
        elif player_score == 7.5:
            print("\nYou got 7.5, you win!")
            chips += bet
            
            # Check for bonus card
            if bonus_card in player_hand:
                bonus = bet * 2
                chips += bonus
                print(f"You have the bonus card {bonus_card} and win a bonus of {bonus} chips!")
            
            # Check for maximum prize
            max_prize = random.randint(50, 1000)
            if player_score == 7.5 and bonus_card in player_hand:
                chips += max_prize
                print(f"You got 7.5 and have the bonus card {bonus_card}! You win the maximum prize of {max_prize} chips!")
        elif player_score > dealer_score:
            print("\nYou win!")
            chips += bet
            
            # Check for bonus card
            if bonus_card in player_hand:
                bonus = bet * 2
                chips += bonus
                print(f"You have the bonus card {bonus_card} and win a bonus of {bonus} chips!")

            # Check for random prize
            prize = random.randint(50, 1000)
            chips += prize
            print(f"You won a prize of {prize} chips!")
        elif player_score < dealer_score:
            print("\nYou lose!")
            chips -= bet
            print("Keep trying!")
        else:
            print("\nDraw!")
        
        # Continue or quit
        continue_playing = input("Do you want to continue playing? (y/n): ").lower()
        if continue_playing != 'y':
            break

    print(f"Game over. You finished with {chips} chips.")

if __name__ == "__main__":
    print("Welcome to Seven and a Half!")
    play_seven_and_a_half()
