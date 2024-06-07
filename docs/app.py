from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('game.html')

@app.route('/play_game')
def play_game():
    # Aqui você colocaria o código Python para gerar a página do jogo dinamicamente
    return "<p>Game content goes here.</p>"

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        chips = int(request.form['chips'])
        bet = int(request.form['bet'])

        if bet < 50 or bet > chips:
            return render_template_string('''
                <h1>7 and a Half</h1>
                <p>Invalid bet. Please try again.</p>
                <form method="post">
                    <label>Available chips: </label>
                    <input type="number" name="chips" value="{{ chips }}" readonly><br>
                    <label>How much do you want to bet (minimum 50)?</label>
                    <input type="number" name="bet" required><br>
                    <button type="submit">Play</button>
                </form>
            ''', chips=chips)

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

        return render_template_string('''
            <h1>7 and a Half</h1>
            <p>{{ message }}</p>
            <form method="post">
                <label>Available chips: </label>
                <input type="number" name="chips" value="{{ chips }}" readonly><br>
                <label>How much do you want to bet (minimum 50)?</label>
                <input type="number" name="bet" required><br>
                <button type="submit">Play</button>
            </form>
        ''', message=message, chips=chips)

    return render_template_string('''
        <h1>7 and a Half</h1>
        <form method="post">
            <label>Available chips: </label>
            <input type="number" name="chips" value="300" readonly><br>
            <label>How much do you want to bet (minimum 50)?</label>
            <input type="number" name="bet" required><br>
            <button type="submit">Play</button>
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
