from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from app_factory import app, db
from models import Games, Users
from helpers import recoverImage


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

@app.route('/update/<int:id>')
def update(id):
    if 'log_user' not in session or session['log_user'] == None:
        return redirect(url_for('login', next='newgame'))
    game = Games.query.filter_by(id=id).first()
    cover_game = recoverImage(game.id)
    return render_template('update.html', titulo='Update Game', game = game, cover_game=cover_game)

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

    file = request.files['file']
    uploads_path = app.config['UPLOAD_PATH']
    file.save(f'{uploads_path}/cover{new_game.id}.jpeg')
    
    return redirect(url_for('home'))

@app.route('/update_game', methods=['POST'])
def update_game():
   game = Games.query.filter_by(id=request.form['id']).first()
   game.name = request.form['name']
   game.genre = request.form['genre']
   game.platform = request.form['platform']

   db.session.add(game)
   db.session.commit()
   file = request.files['file']
   uploads_path = app.config['UPLOAD_PATH']
   file.save(f'{uploads_path}/cover{game.id}.jpeg')
    
   return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete(id):
    if 'log_user' not in session or session['log_user'] == None:
        flash('You need to be logged in to delete a game!')
        return redirect(url_for('login'))
    
    game = Games.query.filter_by(id=id).first()
    db.session.delete(game)
    db.session.commit()
    flash('Game deleted successfully!')
    
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


@app.route('/uploads/<namefile>')
def image(namefile):
    return send_from_directory('uploads', namefile)


