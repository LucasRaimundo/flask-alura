from flask import Flask, render_template

class Game:
    def __init__(self, name, genre, platform):
        self.name = name
        self.genre = genre
        self.platform = platform


app = Flask(__name__)

@app.route('/home')
def home():
    game1 = Game('Fortnite', 'Battle Royale', 'All')
    game2 = Game('Hogwarts Legacy', 'Action RPG', 'All')
    game3 = Game('Call of Duty', 'FPS', 'All')
    games = [game1, game2, game3]
    return render_template('lista.html', titulo='Games', games=games)

app.run()