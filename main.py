from flask import Flask, render_template, request, redirect, session, flash

class Game:
    def __init__(self, name, genre, platform):
        self.name = name
        self.genre = genre
        self.platform = platform

game1 = Game('Fortnite', 'Battle Royale', 'All')
game2 = Game('Hogwarts Legacy', 'Action RPG', 'All')
game3 = Game('Call of Duty', 'FPS', 'All')
games = [game1, game2, game3]


app = Flask(__name__)
app.secret_key = 'alura'

@app.route('/')
def home():
    
    return render_template('lista.html', titulo='Games', games=games)

@app.route('/newgame')
def new_game():
    return render_template('new.html', titulo='New Game')

@app.route('/games/new', methods=['POST'])
def create_game():
    name = request.form['name']
    genre = request.form['genre']
    platform = request.form['platform']

    game = Game(name, genre, platform)
    games.append(game)
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html', titulo='Login')

@app.route('/autenticate', methods=['POST'])
def autenticate():
    if 'alohomora' == request.form['password']:
        session['log_user'] = request.form['username']
        flash( session['log_user'] +' Login successful!')
        return redirect('/')
    else:
        flash('Invalid password!')
        return redirect('/login')

app.run(debug=True)