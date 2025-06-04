from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'alura'

app.config['SQLALCHEMY_DATABASE_URI'] = \
'{SGBD}://{user}:{password}@{server}/{database}'.format(
    SGBD='mysql+mysqlconnector',
    user='root',
    password='',
    server='localhost',
    database='gamelib'
)

db = SQLAlchemy(app)

class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(40), nullable=False)
    platform = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Game {self.name}>'
    
class Users(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'    

@app.route('/')
def home():
    games = Games.query.order_by(Games.id)
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

    game = Games.query.filter_by(name=name).first()
    if game:
        flash('Game already exists!')
        return redirect(url_for('new_game'))
    
    new_game = Games(name=name, genre=genre, platform=platform)
    db.session.add(new_game)
    db.session.commit()
    flash('Game added successfully!')
    
    return redirect(url_for('home'))

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)

@app.route('/autenticate', methods=['POST'])
def autenticate():
    user = Users.query.filter_by(username= request.form['username']).first()
    if user:
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