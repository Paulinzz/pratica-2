from flask import Flask, request, render_template, url_for, session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash  

app = Flask(__name__)

app.config['SECRET_KEY'] = 'MEGADIFICIL_ME_ESCONDE'

usuarios = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        if nome not in usuarios:
            hashed_password = generate_password_hash(senha)
            usuarios[nome] = hashed_password
            return redirect(url_for('login'))
        flash("Você já está cadastrado")
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        if nome in usuarios and check_password_hash(usuarios[nome], senha):
            session['user'] = nome
            return redirect(url_for('dash'))
        flash("Nome ou senha inválidos")
    return render_template('login.html')

@app.route('/dashboard')
def dash():
    if 'user' in session:
        nome = session['user']
        return render_template('dash.html', nome=nome)
    return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user')
    return redirect(url_for('index'))