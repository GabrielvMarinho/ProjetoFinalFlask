from flask import render_template, redirect, url_for, flash
from projeto import app
from projeto.forms import CadastroForm, LoginForm  
from projeto.models import Responsavel, Funcionario
from projeto import db
from flask_login import login_user, logout_user

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Home")
def homeResponsavel():
    return render_template("homeResponsavel.html")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():

        usuario = Responsavel(
            usuario = form.usuario.data,
            email = form.email.data,
            senhacrip = form.senha1.data
        )
        
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('index'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"Erro ao cadastrar usuário {err}", category = "danger")
    return render_template("cadastro.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  
    if form.validate_on_submit():
        usuario_logado = Responsavel.query.filter_by(usuario=form.usuario.data).first()
        if usuario_logado and usuario_logado.converte_senha(senha_texto_claro=form.senha.data):
            login_user(usuario_logado)
            flash(f'Sucesso! seu login é: {usuario_logado.usuario}', category='success')
            return render_template('home_responsavel.html')
        else:
            flash(f'Usuario ou senha estão incorretos! Tente novamente.', category='danger')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    flash("Você fez o logout", category="info")
    return redirect(url_for("page_home"))