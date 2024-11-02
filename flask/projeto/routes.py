from flask import render_template, redirect, url_for, flash, request, session
from projeto import app
from projeto.forms import adicionarSaldoRespo, CadastroForm, confirmarFormQuantidade, removerProduto, LoginForm, SaldoForm, adicionarProduto, confirmarForm
from projeto.models import Responsavel, Funcionario, Dependente, Produto, Historico, ADM
from projeto import db
from flask_login import login_user, logout_user, current_user, login_required
from bcrypt import _bcrypt, hashpw

from datetime import date
@app.route("/Home")
@login_required
def homeResponsavel():
    dependentes = Dependente.query.filter_by(idResponsavel=current_user.id).all()


    historicos = []
    for dependente in dependentes:
        dependente_historicos = Historico.query.filter_by(idDependente=dependente.id).all()
        historicos.extend(dependente_historicos)

    lista = []
    listaNome = []
    listaQuantidade =[]
    listaFinal = []
    listaSaldo =[]
    for i in dependentes:
        if i.idResponsavel == current_user.id:
            listaNome.append(i.usuario)
            lista.append(i)
            

    for i in range(len(dependentes)):
        listaSaldo.append(0)
        for y in dependentes:
            if y.id == lista[i].id:
                listaSaldo[i] = y.saldo

    for i in range(len(lista)):
        listaFinal.append(0)
        listaQuantidade.append(0)
        
        for y in historicos:
            if lista[i].id == y.idDependente:
                listaFinal[i] += y.valor
                listaQuantidade[i] +=y.quantidade
                
    
    produtos = Produto.query.all()
    return render_template("homeResponsavel.html", produtos=produtos, listaSaldo=listaSaldo, listaQuantidade=listaQuantidade, dados=listaFinal, listaNome=listaNome)

@app.route("/historico")

@app.route("/adicionarSaldoResponsavel", methods=['GET', 'POST'])
@login_required
def adicionarSaldoResponsavel():
    form = adicionarSaldoRespo()

    if form.validate_on_submit():
        responsavel = Responsavel.query.get(current_user.id)
        responsavel.saldo = responsavel.saldo+form.adicional.data
        db.session.commit()
        flash("Saldo atualizado", "notError")

        return redirect(url_for('homeResponsavel'))
    
    return render_template("adicionarSaldoResp.html", form =form)

@app.route('/adicionarDependente', methods=['GET', 'POST'])
@login_required
def adicionarDependente():
    form = CadastroForm()
    dependentes = Dependente.query.filter_by(idResponsavel=current_user.id).all()
    if form.validate_on_submit():
        existing_usuario = Responsavel.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario1 = Dependente.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario2 = Funcionario.query.filter_by(usuario=form.usuario.data).first()

        if existing_usuario or existing_usuario1 or existing_usuario2:
            flash('Nome de usuário já existe!')
            return redirect(url_for('adicionarDependente', form=form))
        
        existing_email = Responsavel.query.filter_by(email=form.email.data).first()
        existing_email1 = Dependente.query.filter_by(email=form.email.data).first()
        existing_email2 = Funcionario.query.filter_by(email=form.email.data).first()

        if existing_email or existing_email1 or existing_email2:
            flash("E-mail já cadastrado!")
            return redirect(url_for('adicionarDependente', form=form))
        
        if '@gmail.com' not in form.email.data:
            flash('E-mail inválido!')
            return redirect(url_for('adicionarDependente', form=form))

        if form.senha1.data != form.senha2.data:
            flash("Senhas precisam ser IGUAIS!")
            return redirect(url_for('adicionarDependente', form=form))

        usuario = Dependente(
            usuario = form.usuario.data,
            email = form.email.data,
            senhacrip = form.senha1.data,
            idResponsavel = current_user.id
        )
        db.session.add(usuario)
        flash("Cadastro realizado", "notError")

        db.session.commit()
        return redirect(url_for("homeResponsavel"))
    
    return render_template("adicionarDependente.html", form=form, dependentes=dependentes)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    
    if form.validate_on_submit():
        
        existing_usuario = Responsavel.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario1 = Dependente.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario2 = Funcionario.query.filter_by(usuario=form.usuario.data).first()

        if existing_usuario or existing_usuario1 or existing_usuario2:
            flash('Nome de usuário já existe!')
            return redirect(url_for('cadastro', form=form))
        
        existing_email = Responsavel.query.filter_by(email=form.email.data).first()
        existing_email1 = Dependente.query.filter_by(email=form.email.data).first()
        existing_email2 = Funcionario.query.filter_by(email=form.email.data).first()

        if existing_email or existing_email1 or existing_email2:
            flash("E-mail já cadastrado!")
            return redirect(url_for('cadastro', form=form))
        
        if '@gmail.com' not in form.email.data:
            flash('E-mail inválido!')
            return redirect(url_for('cadastro', form=form))

        if form.senha1.data != form.senha2.data:
            flash("Senhas precisam ser IGUAIS!")
            return redirect(url_for('cadastro', form=form))

        
        usuario = Responsavel(
            usuario = form.usuario.data,
            email = form.email.data,
            senhacrip = form.senha1.data
        )
        
        db.session.add(usuario)
        flash("Cadastro realizado", "notError")

        db.session.commit()
        
        return redirect(url_for('login'))
    
    
    return render_template("cadastro.html", form=form)

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()  
    if form.validate_on_submit():
        usuario_logado = Responsavel.query.filter_by(usuario=form.usuario.data).first()
        dependente_logado = Dependente.query.filter_by(usuario=form.usuario.data).first()
        funcionario_logado = Funcionario.query.filter_by(usuario=form.usuario.data).first()
        if usuario_logado:
            if usuario_logado.converte_senha(senha_texto_claro=form.senha.data):
                login_user(usuario_logado)
                session['user_type'] = 'responsavel'
                return redirect(url_for("homeResponsavel"))
            flash("Senha Incorreta!")

        elif dependente_logado:
            if dependente_logado.converte_senha(senha_texto_claro=form.senha.data):
                login_user(dependente_logado)
                session['user_type'] = 'dependente'
                return redirect(url_for("escolherProduto"))
            flash("Senha Incorreta!")
        elif funcionario_logado:
            if funcionario_logado.senha==form.senha.data:
                login_user(funcionario_logado)
                session['user_type'] = 'funcionario'
                return redirect(url_for("homeFunc"))
            flash("Senha Incorreta!")

        
        else:
            flash("Usuário inexistente!")
            return render_template('index.html', form = form)


    return render_template('index.html', form = form)

@app.route('/perfil')
@login_required
def PerfilPage():
    dependentes = Dependente.query.filter_by(idResponsavel=current_user.id).all()
    historicos = []
    for dependente in dependentes:
        historicos.extend(Historico.query.filter_by(idDependente=dependente.id).all())
    return render_template('PerfilResponsavel.html', dependentes=dependentes, historicos=historicos) 
    
@app.route('/adicionarSaldo', methods=['GET', 'POST'])
@login_required
def addsaldo():
    form = SaldoForm()
    id = request.args.get('botao')
    acao = request.args.get('acao')
    idAtual = request.args.get('idAtual')
    botaoid = request.args.get("botaoid")
    current_user= Responsavel.query.get(idAtual)
    dependente = Dependente.query.get(id)    
    if form.validate_on_submit():
        
        if acao == "0":
            ("0")

            if form.saldo.data<=current_user.saldo:
                print("0")
                dependente.saldo = dependente.saldo+form.saldo.data
                current_user.saldo = current_user.saldo-form.saldo.data
                flash("Saldo adicionado ao dependente - "+dependente.usuario.upper(), "notError")

                db.session.commit()
                return redirect(url_for('escolherDependente', form=form))
            flash("Saldo da conta INSUFICIENTE")
            return redirect(url_for("addsaldo", botao=id, acao=acao, idAtual=idAtual, botaoid=botaoid)) 


        elif acao =="1":

            if form.saldo.data>dependente.saldo:
                flash("Saldo do dependente INSUFICIENTE")
                return redirect(url_for("addsaldo", botao=id, acao=acao, idAtual=idAtual, botaoid=botaoid)) 
            else:
                dependente.saldo = dependente.saldo-form.saldo.data
                current_user.saldo = current_user.saldo+form.saldo.data
                flash("Saldo removido de dependente - "+dependente.usuario.upper(), "notError")

                db.session.commit()
                return redirect(url_for('escolherDependente', form=form))

        else:
            flash("Insuficiente")
            return render_template('homeResponsavel.html')
    if acao==0:
        remover="REMOVER"
        return render_template('adicionarSaldo.html', dependente=dependente, form=form, remover=remover)

    return render_template('adicionarSaldo.html', dependente=dependente, form=form)
    


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/mudar-senha', methods=['POST', 'GET'])
@login_required
def mudarSenha():
    form = LoginForm() 
    if request.method == 'POST':
        usuario=request.form.get('usuario')
        password=request.form.get('password')
        if usuario == "" or password == "":
            flash('Existem campos em branco','danger')
            return redirect('/mudar-senha')
    else:
        usuario_logado = Responsavel.query.filter_by(usuario=form.usuario.data).first()
        if usuario_logado:
            hash_password=_bcrypt.generate_password_hash(password,10)
            Responsavel.query.filter_by(usuario=usuario).update(dict(password=hash_password))
            db.session.commit()
            flash('Senha Alterada','success')
            return redirect('/mudar-senha')
        else:
            flash('Email Invalido','danger')
            return redirect('/mudar-senha')

    return render_template('mudar-senha.html', form=form)

@app.route('/atualizar<int:id>', methods=['POST', 'GET'])
@login_required
def atualizar(id):
    form = CadastroForm()
    mudar_nome = Responsavel.query.get_or_404(id)
    if request.method=="POST":
        novo_usuario = request.form['usuario']
        novo_email = request.form['email']
        
        if not novo_email.endswith('@gmail.com'):
            flash('E-mail inválido!')
            return redirect(url_for('atualizar', id=id))

        usuario_existente = (
            Responsavel.query.filter_by(usuario=novo_usuario).first() or
            Dependente.query.filter_by(usuario=novo_usuario).first() or
            Funcionario.query.filter_by(usuario=novo_usuario).first()
        )

        if usuario_existente and usuario_existente.id != id:
            flash("Usuário já cadastrado!")
            return redirect(url_for('atualizar', id=id))

        email_existente = (
            Responsavel.query.filter_by(email=novo_email).first() or
            Dependente.query.filter_by(email=novo_email).first() or
            Funcionario.query.filter_by(email=novo_email).first()
        )

        if email_existente and email_existente.id != id:
            flash("E-mail já cadastrado!")
            return redirect(url_for('atualizar', id=id))

        if current_user.usuario == novo_usuario and current_user.email == novo_email:
            flash("Dados novos devem ser diferentes dos atuais!")
            return redirect(url_for('atualizar', id=id))

        else:
            mudar_nome.usuario = novo_usuario
            mudar_nome.email = novo_email
            db.session.commit()
            flash("Usuário atualizado", "notError")
            return redirect(url_for('homeResponsavel', id=mudar_nome.id))

    
    return render_template('atualizar.html', form=form, mudar_nome=mudar_nome, id=id)
    
@app.route('/escolherDependente', methods=['GET', 'POST'])
@login_required
def escolherDependente():
    dependentes = Dependente.query.all()
    idAtual = current_user.id
    acao = None
    botao_clicado = None
    
    if request.method == 'POST':
        botaoid = request.form.get('botaoid')

        for dependente in dependentes:
            if request.form.get(f'acao_{dependente.id}') is not None:
                botao_clicado = dependente.id
                acao = request.form.get(f'acao_{dependente.id}')
                break
        
        return redirect(url_for("addsaldo", botao=botao_clicado, acao=acao, idAtual=idAtual, botaoid=botaoid))
    return render_template("ChoseDependent.html", dependentes=dependentes, idAtual=idAtual)

@app.route('/adicionarProduto', methods=['GET', 'POST'])
@login_required
def addProduto():
    form = adicionarProduto()
    produtos = Produto.query.all()
    if form.validate_on_submit():
        produto = Produto(
            lanche = form.lanche.data,
            valor = form.valor.data,
            quantidade = form.quantidade.data
        )
        
        db.session.add(produto)
        db.session.commit()
        flash("Produto adicionado!", "notError")
        return redirect(url_for("homeFunc"))
    return render_template("adicionarProduto.html", form = form, produtos=produtos)

@app.route('/homeFunc', methods=['GET', 'POST'])
@login_required
def homeFunc():
    quantidadeEstoque = []
    produtos = Produto.query.all()
    nomes = []
    for i in produtos:
        quantidadeEstoque.append(i.quantidade)
        nomes.append(i.lanche)

    pessoas = Dependente.query.all()
    nomes1 = []
    listaHist=[]
    for i in pessoas:
        historico = (Historico.query.filter_by(idDependente=i.id))
        soma = 0
        nomes1.append(i.usuario)
        for ii in historico:
            soma +=ii.valor

        listaHist.append(soma)

    return render_template("homeFuncionario.html", quantidadeEstoque=quantidadeEstoque, nomes=nomes, listaHist=listaHist, nomes1=nomes1)


@app.route("/adicionarEstoques", methods=['GET', 'POST'])
@login_required
def addProdutoQuantidade():
    produtoSemEstoque = Produto.query.all()
    form = confirmarForm()
    return render_template("adicionarEstoque.html", produtos = produtoSemEstoque, form=form)

@app.route("/adicionarEstoqueFim<int:id>", methods=['GET', 'POST'])
@login_required
def addProdutoQuantidadeFim(id):  
    produto = Produto.query.get(id)
    form = confirmarForm()
    counter_value = int(request.form.get('counter_value', 1))
    if form.validate_on_submit():
        produto.quantidade += counter_value
        db.session.commit()
        flash("Estoque atualizado!", "notError")
        return redirect(url_for("addProdutoQuantidade"))
    return render_template("adicionarEstoqueFim.html", form=form, produto = produto)

@app.route("/escolherProduto", methods=['GET', 'POST'])
@login_required
def choseProduto():
    produtos = Produto.query.all()
    return render_template("escolherRemoverProduto.html", produtos=produtos)


@app.route('/removerProduto/<int:id>', methods=['GET', 'POST'])
@login_required
def removerProdutos(id):
    obj = Produto.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for("choseProduto"))
        


@app.route('/comprarProduto/<int:id>', methods=['GET', 'POST'])
@login_required
def comprarProduto(id):
    form = confirmarFormQuantidade()
    obj = Produto.query.get(id)
    counter_value = int(request.form.get('counter_value', 1)) 
    if form.validate_on_submit():

        if current_user.saldo >= obj.valor*counter_value:
            if obj.quantidade>=counter_value:
                obj.quantidade = obj.quantidade-counter_value
                current_user.saldo = current_user.saldo-obj.valor*counter_value
                historico = Historico(
                    idproduto = id,
                    data = date.today(),
                    valor = counter_value*obj.valor,
                    quantidade = counter_value, 
                    idDependente = current_user.id

                )
                adm = ADM.query.get(1)
                adm.saldo +=obj.valor*counter_value
                db.session.add(historico)
                db.session.commit()
                flash("Compra realizada com sucesso!", "notError")

                return redirect(url_for("escolherProduto"))
            flash("ESTOQUE insuficiente!")
            return render_template("comprarProduto.html", obj=obj, form=form)
        flash("SALDO insuficiente!")
        return render_template("comprarProduto.html", obj=obj, form=form)
    
    return render_template("comprarProduto.html", obj=obj, form=form)
    

@app.route('/homeDependente', methods=['GET', 'POST'])
@login_required
def escolherProduto():
    produtos = Produto.query.all()
    return render_template("homeDependente.html", produtos =produtos)







