from flask import render_template, redirect, url_for, flash, request, session
from projeto import app
from projeto.forms import adicionarSaldoRespo, CadastroForm,removerProduto, LoginForm, SaldoForm, adicionarProduto, confirmarForm
from projeto.models import Responsavel, Funcionario, Dependente, Produto
from projeto import db
from flask_login import login_user, logout_user, current_user
from bcrypt import _bcrypt


@app.route("/Home")
def homeResponsavel():
    print(current_user.saldo)
    return render_template("homeResponsavel.html")

@app.route("/adicionarSaldoResponsavel", methods=['GET', 'POST'])
def adicionarSaldoResponsavel():
    form = adicionarSaldoRespo()

    if form.validate_on_submit():
            
        responsavel = Responsavel.query.get(current_user.id)
        responsavel.saldo = responsavel.saldo+form.adicional.data
        db.session.commit()
        return render_template('homeResponsavel.html')
    return render_template("adicionarSaldoResp.html", form =form)

@app.route('/adicionarDependente', methods=['GET', 'POST'])
def adicionarDependente():
    form = CadastroForm()
    if form.validate_on_submit():

        usuario = Dependente(
            usuario = form.usuario.data,
            email = form.email.data,
            senhacrip = form.senha1.data,
            idResponsavel = current_user.id
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("homeResponsavel"))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"Erro ao cadastrar usuário {err}", category = "danger")
    return render_template("adicionarDependente.html", form=form)

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
        return redirect(url_for('login'))
    if form.errors != {}:
        for err in form.errors.values():
            flash(f"Erro ao cadastrar usuário {err}", category = "danger")
    return render_template("cadastro.html", form=form)

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()  
    if form.validate_on_submit():
        usuario_logado = Responsavel.query.filter_by(usuario=form.usuario.data).first()
        dependente_logado = Dependente.query.filter_by(usuario=form.usuario.data).first()
        funcionario_logado = Funcionario.query.filter_by(usuario=form.usuario.data).first()
        if usuario_logado and usuario_logado.converte_senha(senha_texto_claro=form.senha.data):
            login_user(usuario_logado)
            session['user_type'] = 'responsavel'
            return render_template('homeResponsavel.html')
        elif dependente_logado and dependente_logado.converte_senha(senha_texto_claro=form.senha.data):
            login_user(dependente_logado)
            session['user_type'] = 'dependente'
            print("deu certo dependente")
            return redirect(url_for("escolherProduto"))

        elif funcionario_logado and funcionario_logado.senha==form.senha.data:
            login_user(funcionario_logado)
            session['user_type'] = 'funcionario'
            return render_template('homeFuncionario.html')

    return render_template('index.html', form = form)


@app.route('/adicionarSaldo', methods=['GET', 'POST'])
def addsaldo():
    form = SaldoForm()
    id = request.args.get('botao')
    if form.validate_on_submit():
        dependente = Dependente.query.get(id)
        if(form.saldo.data<=current_user.saldo):
            dependente.saldo = dependente.saldo+form.saldo.data
            current_user.saldo = current_user.saldo-form.saldo.data
            db.session.commit()
        else:
            flash("Insuficiente")
            return render_template('homeResponsavel.html')
    
    return render_template('adicionarSaldo.html', form=form)
    


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/mudar-senha', methods=['POST', 'GET'])
def mudarSenha():
    form = LoginForm() 
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')
        if email == "" or password == "":
            flash('Existem campos em branco','danger')
            return redirect('/mudar-senha')
    else:
        usuario_logado = Responsavel.query.filter_by(usuario=form.usuario.data).first()
        if usuario_logado:
            hash_password=_bcrypt.generate_password_hash(password,10)
            Responsavel.query.filter_by(email=email).update(dict(password=hash_password))
            db.session.commit()
            flash('Senha Alterada','success')
            return redirect('/mudar-senha')
        else:
            flash('Email Invalido','danger')
            return redirect('/mudar-senha')

    return render_template('mudar-senha.html', title="Mudar Senha", form=form)


@app.route('/escolherDependente', methods=['GET', 'POST'])
def escolherDependente():
    dependentes = Dependente.query.all()
    idAtual = current_user.id
    botao_clicado=None
    if request.method == 'POST':
        botao_clicado = request.form.get('botao')

        return redirect(url_for("addsaldo", botao = botao_clicado))
    return render_template("ChoseDependent.html", botao = botao_clicado, dependentes =dependentes, idAtual=idAtual)


@app.route('/adicionarProduto', methods=['GET', 'POST'])
def addProduto():
    form = adicionarProduto()
    if form.validate_on_submit():
        produto = Produto(
            lanche = form.lanche.data,
            valor = form.valor.data
        )
        db.session.add(produto)
        db.session.commit()
        return render_template("homeFuncionario.html", form = form)
    return render_template("adicionarProduto.html", form = form)


@app.route("/escolherProduto", methods=['GET', 'POST'])
def choseProduto():
    produtos = Produto.query.all()
    return render_template("escolherRemoverProduto.html", produtos=produtos)


@app.route('/removerProduto/<int:id>', methods=['GET', 'POST'])
def removerProdutos(id):
    form = confirmarForm()
    obj = Produto.query.get(id)
    if form.validate_on_submit():
        db.session.delete(obj)
        db.session.commit()
        return redirect(url_for("choseProduto"))
    return render_template("excluirProduto.html", obj=obj, form=form)

        
@app.route('/teste')
def teste():
    return render_template("teste.html")


@app.route('/comprarProduto/<int:id>', methods=['GET', 'POST'])
def comprarProduto(id):
    form = confirmarForm()
    obj = Produto.query.get(id)
    if form.validate_on_submit():
        if current_user.saldo >= obj.valor:
            current_user.saldo = current_user.saldo-obj.valor
            db.session.commit()
            return redirect(url_for("escolherProduto"))
        return render_template("comprarProduto.html", obj=obj, form=form)
    return render_template("comprarProduto.html", obj=obj, form=form)
    

@app.route('/homeDependente', methods=['GET', 'POST'])
def escolherProduto():
    produtos = Produto.query.all()
    return render_template("homeDependente.html", produtos =produtos)





