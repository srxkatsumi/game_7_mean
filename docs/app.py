from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

def valor_carta(carta):
    if carta in ['Valete', 'Dama', 'Rei']:
        return 0.5
    elif carta == 'Ás':
        return 1
    else:
        return int(carta)

def sortear_carta(cartas):
    carta = random.choice(cartas)
    cartas.remove(carta)
    return carta

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fichas = int(request.form['fichas'])
        aposta = int(request.form['aposta'])

        if aposta < 50 or aposta > fichas:
            return render_template_string('''
                <h1>7 e Meio</h1>
                <p>Aposta inválida. Tente novamente.</p>
                <form method="post">
                    <label>Fichas disponíveis: </label>
                    <input type="number" name="fichas" value="{{ fichas }}" readonly><br>
                    <label>Quanto deseja apostar (mínimo 50)?</label>
                    <input type="number" name="aposta" required><br>
                    <button type="submit">Jogar</button>
                </form>
            ''', fichas=fichas)

        cartas = ['Ás', '2', '3', '4', '5', '6', '7', 'Valete', 'Dama', 'Rei'] * 4
        random.shuffle(cartas)

        mao_jogador = []
        mao_banca = []
        pontuacao_jogador = 0
        pontuacao_banca = 0

        carta_bonus = sortear_carta(cartas)

        for _ in range(2):
            carta = sortear_carta(cartas)
            mao_banca.append(carta)
            pontuacao_banca += valor_carta(carta)

        carta = sortear_carta(cartas)
        mao_jogador.append(carta)
        pontuacao_jogador += valor_carta(carta)

        if pontuacao_banca > 7.5:
            fichas += aposta
            mensagem = "A banca estourou 7.5, você venceu!"
            premio = random.randint(50, 1000)
            fichas += premio
            mensagem += f" Você ganhou um prêmio de {premio} fichas!"
        elif pontuacao_jogador == 7.5:
            fichas += aposta
            mensagem = "Você fez 7.5, você venceu!"
            premio = random.randint(50, 1000)
            fichas += premio
            mensagem += f" Você ganhou um prêmio de {premio} fichas!"
            if carta_bonus in mao_jogador:
                bonus = aposta * 2
                fichas += bonus
                mensagem += f" Você tem a carta bônus {carta_bonus} e ganha um bônus de {bonus} fichas!"
        else:
            if pontuacao_jogador < pontuacao_banca:
                fichas -= aposta
                mensagem = "Você perdeu! Continue tentando!"
            else:
                fichas += aposta
                mensagem = "Você venceu!"
                premio = random.randint(50, 1000)
                fichas += premio
                mensagem += f" Você ganhou um prêmio de {premio} fichas!"
                if carta_bonus in mao_jogador:
                    bonus = aposta * 2
                    fichas += bonus
                    mensagem += f" Você tem a carta bônus {carta_bonus} e ganha um bônus de {bonus} fichas!"

        return render_template_string('''
            <h1>7 e Meio</h1>
            <p>{{ mensagem }}</p>
            <form method="post">
                <label>Fichas disponíveis: </label>
                <input type="number" name="fichas" value="{{ fichas }}" readonly><br>
                <label>Quanto deseja apostar (mínimo 50)?</label>
                <input type="number" name="aposta" required><br>
                <button type="submit">Jogar</button>
            </form>
        ''', mensagem=mensagem, fichas=fichas)

    return render_template_string('''
        <h1>7 e Meio</h1>
        <form method="post">
            <label>Fichas disponíveis: </label>
            <input type="number" name="fichas" value="300" readonly><br>
            <label>Quanto deseja apostar (mínimo 50)?</label>
            <input type="number" name="aposta" required><br>
            <button type="submit">Jogar</button>
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
