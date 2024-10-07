from flask import render_template, redirect, url_for, flash, request, session
from projeto import app
from projeto.forms import adicionarSaldoRespo, CadastroForm, confirmarFormQuantidade, removerProduto, LoginForm, SaldoForm, adicionarProduto, confirmarForm
from projeto.models import Responsavel, Funcionario, Dependente, Produto, Historico, ADM
from projeto import db
from flask_login import login_user, logout_user, current_user
from bcrypt import _bcrypt, hashpw

from datetime import date
@app.route("/Home")
def homeResponsavel():
    historicos = Historico.query.all()
    dependentes = Dependente.query.all()
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

    print("lista de saldoss", listaSaldo)
    for i in range(len(lista)):
        listaFinal.append(0)
        listaQuantidade.append(0)
        
        for y in historicos:
            print(lista[i].id)
            print(y.idDependente)

            if lista[i].id == y.idDependente:
                print("add")
                listaFinal[i] += y.valor
                listaQuantidade[i] +=y.quantidade
                
    
    produtos = Produto.query.all()
    print(listaFinal)
    return render_template("homeResponsavel.html", produtos=produtos, listaSaldo=listaSaldo, listaQuantidade=listaQuantidade, dados=listaFinal, listaNome=listaNome)

@app.route("/adicionarSaldoResponsavel", methods=['GET', 'POST'])
def adicionarSaldoResponsavel():
    form = adicionarSaldoRespo()

    if form.validate_on_submit():
            
        responsavel = Responsavel.query.get(current_user.id)
        responsavel.saldo = responsavel.saldo+form.adicional.data
        db.session.commit()
        return redirect(url_for('homeResponsavel'))
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
            return redirect(url_for("homeResponsavel"))
        elif dependente_logado and dependente_logado.converte_senha(senha_texto_claro=form.senha.data):
            login_user(dependente_logado)
            session['user_type'] = 'dependente'
            print("deu certo dependente")
            return redirect(url_for("escolherProduto"))

        elif funcionario_logado and funcionario_logado.senha==form.senha.data:
            login_user(funcionario_logado)
            session['user_type'] = 'funcionario'
            return render_template('homeFuncionario.html')
        
        else:
            flash("OCORREU ERRO NO LOGIN!")
            return render_template('index.html', form = form)


    return render_template('index.html', form = form)

@app.route('/perfil-page')
def PerfilPage():
    return render_template('PerfilResponsavel.html') 
    
@app.route('/adicionarSaldo', methods=['GET', 'POST'])
def addsaldo():
    form = SaldoForm()
    id = request.args.get('botao')
    acao = request.args.get('acao')
    idAtual = request.args.get('idAtual')
    current_user= Responsavel.query.get(idAtual)
    print("teste", id)
    dependente = Dependente.query.get(id)    
    if form.validate_on_submit():
        
        if acao == "0":
            if form.saldo.data<=current_user.saldo:
                dependente.saldo = dependente.saldo+form.saldo.data
                current_user.saldo = current_user.saldo-form.saldo.data
                db.session.commit()
                return redirect(url_for('escolherDependente', form=form))
        elif acao =="1":
            if form.saldo.data>dependente.saldo:
                flash("Insuficiente")
                return render_template('homeResponsavel.html') 
            else:
                dependente.saldo = dependente.saldo-form.saldo.data
                current_user.saldo = current_user.saldo+form.saldo.data
                db.session.commit()
                return redirect(url_for('escolherDependente', form=form))

        else:
            flash("Insuficiente")
            return render_template('homeResponsavel.html')
    if acao==0:
        remover="REMOVER"
        return render_template('adicionarSaldo.html', form=form, remover=remover)

    return render_template('adicionarSaldo.html', form=form)
    


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/mudar-senha', methods=['POST', 'GET'])
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
def atualizar(id):
    form = CadastroForm()
    mudar_nome = Responsavel.query.get_or_404(id)
    if request.method=="POST":
        mudar_nome.usuario = request.form['usuario']
        mudar_nome.email = request.form['email']
        senha = request.form['senha1']
        if senha:  
            hashed_senha = _bcrypt.generate_password_hash(senha)  # Hash the password before saving (replace with your hash function)
            mudar_nome.senha = hashed_senha
        try:
            db.session.commit()
            flash("Usuairio atualizado")
            return redirect(url_for('atualizar', id=mudar_nome.id))
        except:
            db.session.rollback()
            flash(f"Erro ao atualizar o usuário")
            return render_template('atualizar.html', form=form, mudar_nome=mudar_nome, id=id)
    else:
        flash(f"Erro ao atualizar o usuário")
        return render_template('atualizar.html', form=form, mudar_nome=mudar_nome, id=id)
    
@app.route('/escolherDependente', methods=['GET', 'POST'])
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

        print("id do dependente", botao_clicado)
        print("acao", acao)
        print("idAtual", idAtual)
        
        return redirect(url_for("addsaldo", botao=botao_clicado, acao=acao, idAtual=idAtual, botaoid=botaoid))
    return render_template("ChoseDependent.html", dependentes=dependentes, idAtual=idAtual)

@app.route('/adicionarProduto', methods=['GET', 'POST'])
def addProduto():
    form = adicionarProduto()
    if form.validate_on_submit():
        produto = Produto(
            lanche = form.lanche.data,
            valor = form.valor.data,
            quantidade = form.quantidade.data
        )
        
        db.session.add(produto)
        db.session.commit()
        return render_template("homeFuncionario.html", form = form)
    return render_template("adicionarProduto.html", form = form)

@app.route('/homeFunc', methods=['GET', 'POST'])
def homeFunc():
    return render_template("homeFuncionario.html")


@app.route("/adicionarEstoques", methods=['GET', 'POST'])
def addProdutoQuantidade():
    produtoSemEstoque = Produto.query.all()
    form = confirmarForm()
    if form.validate_on_submit():
        print("submit")
    return render_template("adicionarEstoque.html", produtos = produtoSemEstoque, form=form)

@app.route("/adicionarEstoqueFim<int:id>", methods=['GET', 'POST'])
def addProdutoQuantidadeFim(id):  
    produto = Produto.query.get(id)
    form = confirmarForm()
    counter_value = int(request.form.get('counter_value', 1))
    if form.validate_on_submit():
        produto.quantidade += counter_value
        db.session.commit()
        print(produto.quantidade)
        return redirect(url_for("addProdutoQuantidade"))
    return render_template("adicionarEstoqueFim.html", form=form, produto = produto)

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

        
@app.route('/dependetes')
def teste():
    return render_template("Dependentes.html")


@app.route('/comprarProduto/<int:id>', methods=['GET', 'POST'])
def comprarProduto(id):
    form = confirmarFormQuantidade()
    obj = Produto.query.get(id)
    print("pode escolher cara")
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
                return redirect(url_for("escolherProduto"))
        return render_template("comprarProduto.html", obj=obj, form=form)
    return render_template("comprarProduto.html", obj=obj, form=form)
    

@app.route('/homeDependente', methods=['GET', 'POST'])
def escolherProduto():
    produtos = Produto.query.all()
    return render_template("homeDependente.html", produtos =produtos)







