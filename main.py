from flask import Flask, render_template, request, redirect, session, flash, url_for

class User:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

class Game:
    def __init__(self, name, genre, platform):
        self.name = name
        self.genre = genre
        self.platform = platform

game1 = Game('Fortnite', 'Battle Royale', 'All')
game2 = Game('Hogwarts Legacy', 'Action RPG', 'All')
game3 = Game('Call of Duty', 'FPS', 'All')
games = [game1, game2, game3]

user = User('Lucas', 'lucas', 'Alohomora')
user1 = User('Gabriel', 'gabriel', 'Nox')
user2 = User('Pedro', 'pedro', 'ExpectoPatronum')

users = {user.username: user, user1.username: user1, user2.username: user2}

app = Flask(__name__)
app.secret_key = 'alura'

@app.route('/')
def home():
    
    return render_template('lista.html', titulo='Games', games=games)

@app.route('/newgame')
def new_game():
    if 'log_user' not in session or session['log_user'] == None:
        flash('You need to be logged in to add a game!')
        return redirect(url_for('login', next='newgame'))
    return render_template('new.html', titulo='New Game')

@app.route('/games/new', methods=['POST'])
def create_game():
    name = request.form['name']
    genre = request.form['genre']
    platform = request.form['platform']

    game = Game(name, genre, platform)
    games.append(game)
    return redirect(url_for('home'))

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)

@app.route('/autenticate', methods=['POST'])
def autenticate():
    if request.form['username'] in users:
        user = users[request.form['username']]
        if request.form['password'] == user.password:
            session['log_user'] = user.username
            flash('Login successful!')
            next_page = request.form['next']
            return redirect(next_page)

    else:
        flash('Invalid password!')
        return redirect(url_for('login'))
    

@app.route('/logout')
def logout():
    session['log_user'] = None
    flash('Logout successful!')
    return redirect(url_for('login'))

app.run(debug=True)