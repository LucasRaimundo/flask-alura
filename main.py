from flask import Flask, render_template


app = Flask(__name__)

@app.route('/home')
def home():
    games = ['Fortinte', 'Hogwarts Legacy', 'Call of Duty', 'Fifa 23']
    return render_template('lista.html', titulo='Games', games=games)

app.run()