from flask import render_template, redirect, url_for, flash, request, session, make_response
from flask_socketio import SocketIO, join_room, emit, leave_room
from projeto import app
from projeto.forms import adicionarSaldoRespo, CadastroForm, confirmarFormQuantidade, removerProduto, LoginForm, SaldoForm, adicionarProduto, confirmarForm
from projeto.models import Responsavel, Funcionario, Dependente, Produto, Historico, ADM
from projeto import db
from flask_login import login_user, logout_user, current_user, login_required
from bcrypt import _bcrypt, hashpw
from sqlalchemy import desc
from datetime import date
from collections import defaultdict  # Certifique-se de importar defaultdict
from functools import wraps
from time import sleep
from projeto.__init__ import s, mail
from flask_mail import Mail, Message

cont = 0
socketio = SocketIO(app)

rooms_users = defaultdict(set) 

def user_type_required(*allowed_types):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_type' not in session or session['user_type'] not in allowed_types:
                flash("Você não tem permissão para acessar esta página. Faça login com a conta correta.")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@socketio.on("user_join")
def conectar_operador(id):
    print("entrou")
    join_room(id)
    rooms_users[id].add(current_user.usuario) 

   
@app.route("/excluirContaPropria", methods=["POST", "GET"])
def excluirContaPropria():
    resp = Responsavel.query.get(current_user.id)
    for i in Dependente.query.all():
        if i.idResponsavel == resp.id:
            db.session.delete(i)
    db.session.delete(resp)
    db.session.commit()
    return redirect(url_for("login"))


@app.route("/removerFuncionario/<int:id>", methods=["POST", "GET"])
def removerFuncionario(id):
    id = int(id)
    funcionario = Funcionario.query.get(id)
    print(funcionario)
    db.session.delete(funcionario)
    db.session.commit()
    return redirect(url_for("adicionarFuncionario"))



@app.route("/paginamensagens")
@login_required
@user_type_required("funcionario", "adm")
def mensagens():
    return render_template("painel_controle.html")

@app.route("/Home")
@login_required
@user_type_required("responsavel")
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
@login_required
@user_type_required("responsavel")
def historico():
    dependentes_do_responsavel = Dependente.query.filter_by(idResponsavel=current_user.id).all()

    ids_dependentes = [dependente.id for dependente in dependentes_do_responsavel]

    historicos = Historico.query.filter(Historico.idDependente.in_(ids_dependentes)).order_by(desc(Historico.id)).all()


    

    return render_template("historico.html", historicos=historicos)

@app.route("/adicionarSaldoResponsavel/<saldo>", methods=['GET', 'POST'])
@login_required
@user_type_required("responsavel")
def adicionarSaldoResponsavel(saldo):
    try:
        saldo = int(saldo)
        if saldo>0:
            responsavel = Responsavel.query.get(current_user.id)
            responsavel.saldo = responsavel.saldo+saldo
            db.session.commit()
            flash("Saldo atualizado", "notError")
        else:
            flash("Digite um valor válido! ")
    except:
        flash("Digite apenas números!")

    return ""

@app.route("/cardapio_func")
@login_required
@user_type_required("funcionario", "adm")
def cardapio_func():
    return render_template("cardapioFuncionario.html", produtos = Produto.query.filter(Produto.quantidade>0).all())

@app.route("/cardapio_adm")
def cardapio_adm():
    return render_template("cardapioAdm.html", produtos = Produto.query.filter(Produto.quantidade>0).all())


@app.route("/cardapio")
@login_required
@user_type_required("responsavel")
def cardapio():
    return render_template("cardapioResponsavel.html", produtos = Produto.query.filter(Produto.quantidade>0).all())












@app.route("/adicionarFuncionarioFim/<usuario1>/<email1>/<senhacrip1>/<token>")
def adicionarFuncionarioFim(usuario1, email1, senhacrip1, token):



    usuario = Funcionario(
        usuario = usuario1,
        email = email1,
        senha = senhacrip1,
    )
    db.session.add(usuario)
    flash("Cadastro realizado", "notError")

    db.session.commit()
    return redirect(url_for("homeAdm"))


@app.route("/adicionarFuncionario", methods=['GET', 'POST'])
@login_required
@user_type_required("adm")
def adicionarFuncionario():
    form = CadastroForm()
    funcionarios = Funcionario.query.all()
    if form.validate_on_submit():
        existing_usuario = Responsavel.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario1 = Dependente.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario2 = Funcionario.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario3 = ADM.query.filter_by(usuario=form.usuario.data).first()

        if existing_usuario or existing_usuario1 or existing_usuario2 or existing_usuario3:
            flash('Nome de usuário já existe!')
            return redirect(url_for('adicionarFuncionario', form=form))
        
        existing_email = Responsavel.query.filter_by(email=form.email.data).first()
        existing_email1 = Dependente.query.filter_by(email=form.email.data).first()
        existing_email2 = Funcionario.query.filter_by(email=form.email.data).first()

        if existing_email or existing_email1 or existing_email2:
            flash("E-mail já cadastrado!")
            return redirect(url_for('adicionarFuncionario', form=form))
        
        if '@gmail.com' not in form.email.data:
            flash('E-mail inválido!')
            return redirect(url_for('adicionarFuncionario', form=form))

        if form.senha1.data != form.senha2.data:
            flash("Senhas precisam ser IGUAIS!")
            return redirect(url_for('adicionarFuncionario', form=form))


        token = s.dumps(form.email.data, salt="email-confirm")

        msg = Message("Confirm Email", sender="suporte.my.snack@gmail.com", recipients=[form.email.data])

        link = url_for("adicionarFuncionarioFim", usuario1 = form.usuario.data, email1 = form.email.data, senhacrip1 = form.senha2.data,  token=token, _external=True)

        msg.body = "Seu link de confirmação é "+link

        mail.send(msg)
        
        flash("Clique no link de confirmação no E-mail para criar conta de Funcionário!", "notError")


        
    
    return render_template("adicionarFuncionario.html", form=form, funcionarios=funcionarios)



@app.route("/adicionarDependenteFim/<usuario1>/<email1>/<senhacrip1>/<id>")
def adicionarDependenteFim(usuario1, email1, senhacrip1, id):
    usuario = Dependente(
        usuario = usuario1,
        email = email1,
        senhacrip = senhacrip1,
        idResponsavel = id
    )
    db.session.add(usuario)

    flash("Cadastro realizado", "notError")
    db.session.commit()
    
    print("deu certo")

    return redirect(url_for("homeResponsavel"))

@app.route('/adicionarDependente', methods=['GET', 'POST'])
@login_required
@user_type_required("responsavel")
def adicionarDependente():
    form = CadastroForm()
    dependentes = Dependente.query.filter_by(idResponsavel=current_user.id).all()
    if form.validate_on_submit():
        existing_usuario = Responsavel.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario1 = Dependente.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario2 = Funcionario.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario3 = ADM.query.filter_by(usuario=form.usuario.data).first()

        if existing_usuario or existing_usuario1 or existing_usuario2 or existing_usuario3:
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


        token = s.dumps(form.email.data, salt="email-confirm")

        msg = Message("Confirm Email", sender="suporte.my.snack@gmail.com", recipients=[form.email.data])

        link = url_for("adicionarDependenteFim", id = current_user.id, usuario1 = form.usuario.data, email1 = form.email.data, senhacrip1 = form.senha2.data, token=token, _external=True)

        msg.body = "Seu link de confirmação é "+link

        mail.send(msg)
        
        flash("Clique no link de confirmação no E-mail para criar conta de dependente!", "notError")

        
    
    return render_template("adicionarDependente.html", form=form, dependentes=dependentes)


@app.route("/cadastroFinal/<usuario1>/<email1>/<senhacrip1>")
def cadastroFinal(usuario1, email1, senhacrip1):

    usuario = Responsavel(
        usuario = usuario1,
        email = email1,
        senhacrip = senhacrip1
    )
        
    db.session.add(usuario)
    flash("Cadastro realizado", "notError")

    db.session.commit()
        
    return redirect(url_for('login'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    
    if form.validate_on_submit():
        
        existing_usuario = Responsavel.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario1 = Dependente.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario2 = Funcionario.query.filter_by(usuario=form.usuario.data).first()
        existing_usuario3 = ADM.query.filter_by(usuario=form.usuario.data).first()

        if existing_usuario or existing_usuario1 or existing_usuario2 or existing_usuario3:
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
        
        token = s.dumps(form.email.data, salt="email-confirm")

        msg = Message("Confirm Email", sender="suporte.my.snack@gmail.com", recipients=[form.email.data])

        link = url_for("cadastroFinal", usuario1 = form.usuario.data, email1 = form.email.data, senhacrip1 = form.senha2.data,  token=token, _external=True)

        msg.body = "Seu link de confirmação é "+link

        mail.send(msg)
        
        flash("Clique no link de confirmação no E-mail para criar sua conta!", "notError")
    
    return render_template("cadastro.html", form=form)

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()  
    if form.validate_on_submit():
        usuario_logado = Responsavel.query.filter_by(usuario=form.usuario.data).first()
        dependente_logado = Dependente.query.filter_by(usuario=form.usuario.data).first()
        funcionario_logado = Funcionario.query.filter_by(usuario=form.usuario.data).first()
        adm_logado = ADM.query.filter_by(usuario=form.usuario.data).first()

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

        elif adm_logado:
            print(adm_logado.senha)
            print(form.senha.data)
            if adm_logado.senha==form.senha.data:
                login_user(adm_logado)
                print(current_user)
                session['user_type'] = 'adm'
                return redirect(url_for("homeAdm"))
            flash("Senha Incorreta!")
        
        else:
            flash("Usuário inexistente!")
            return render_template('index.html', form = form)


    return render_template('index.html', form = form)

@app.route("/homeAdm")
@login_required
@user_type_required("adm")
def homeAdm():
    funcionarios = Funcionario.query.all()
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
    return render_template("homeAdm.html", funcionarios=funcionarios, quantidadeEstoque=quantidadeEstoque, nomes=nomes, listaHist=listaHist, nomes1=nomes1)

@app.route("/historicoLanches")
@login_required
@user_type_required("funcionario", "adm")
def historicoLaches():
    historicos=[]
    historicos=[]
    historico_dependente = Historico.query.order_by(desc(Historico.id)).all()
    historicos.extend(historico_dependente)
    return render_template("historicoFunc.html", historicos=historicos)



@app.route("/historicoLanchesAdm")
@login_required
@user_type_required("funcionario", "adm")
def historicoLachesAdm():
    historicos=[]
    historicos=[]
    historico_dependente = Historico.query.order_by(desc(Historico.id)).all()
    historicos.extend(historico_dependente)
    return render_template("historicoAdm.html", historicos=historicos)



@app.route('/perfil')
@login_required
@user_type_required("responsavel")
def PerfilPage():
    dependentes = Dependente.query.filter_by(idResponsavel=current_user.id).all()
    historicos = []
    for dependente in dependentes: 
        historicos.extend(Historico.query.filter_by(idDependente=dependente.id).order_by(desc(Historico.id)).all())
    return render_template('PerfilResponsavel.html', dependentes=dependentes, historicos=historicos) 
     
@app.route('/removerSaldo/<valor>/<id>', methods=['GET', 'POST'])
@login_required
@user_type_required("responsavel")
def removSaldo(valor, id):
        
    valor = int(valor)
    dependente = Dependente.query.filter_by(id = id).first()
    if valor<=0:
        flash("Digite um valor VÁLIDO!")
    elif valor>dependente.saldo:
        flash("Saldo do dependente INSUFICIENTE!")

        
    else:
        dependente.saldo = dependente.saldo-valor
        current_user.saldo = current_user.saldo+valor
        flash(f"Saldo removido de dependente: {dependente.usuario.upper()}", "notError")
        db.session.commit()
    
    return ""
           
@app.route('/adicionarSaldo/<valor>/<id>', methods=['GET', 'POST'])
@login_required
@user_type_required("responsavel")
def addSaldo(valor, id):
        
    valor = int(valor)

    dependente = Dependente.query.filter_by(id = id).first()
    if valor<=0:
        flash("Digite um valor VÁLIDO")
    elif valor<=current_user.saldo:
        dependente.saldo = dependente.saldo+valor
        current_user.saldo = current_user.saldo-valor
        flash(f"Saldo adicionado ao dependente: {dependente.usuario.upper()}", "notError")
        db.session.commit()
    else:
        flash(f"Saldo da conta INSUFICIENTE: {current_user.saldo}")

    
    return ""
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/mudar-senha', methods=['POST', 'GET'])
@login_required
@user_type_required("responsavel")
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



@app.route("/atualizarFim/<id1>/<usuario>/<email>")
def atualizarFim(id1, usuario, email):
    mudar_nome = Responsavel.query.get_or_404(id1)
    mudar_nome.usuario = usuario
    mudar_nome.email = email
    db.session.commit()
    flash("Usuário atualizado", "notError")
    return redirect(url_for('homeResponsavel', id=mudar_nome.id))


@app.route('/atualizar<int:id>', methods=['POST', 'GET'])
@login_required
@user_type_required("responsavel")
def atualizar(id):
    dependentes = Dependente.query.filter_by(idResponsavel=current_user.id).all()
    historicos = []
    for dependente in dependentes: 
        historicos.extend(Historico.query.filter_by(idDependente=dependente.id).order_by(desc(Historico.id)).all())
    print(historicos)
    
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
            
            token = s.dumps(novo_email, salt="email-confirm")
            msg = Message("Confirm Email", sender="suporte.my.snack@gmail.com", recipients=[novo_email])
            link = url_for("atualizarFim", id1 = id,  usuario = novo_usuario, email = novo_email,  token=token, _external=True)
            msg.body = "Seu link de confirmação é "+link

            mail.send(msg)
            flash("Clique no link de confirmação no E-mail para criar trocar o E-mail!", "notError")
    
    return render_template('atualizar.html', form=form, mudar_nome=mudar_nome, id=id, dependentes=dependentes, historicos=historicos)
    
@app.route('/escolherDependente', methods=['GET', 'POST'])
@login_required
@user_type_required("responsavel")
def escolherDependente():
    dependentes = Dependente.query.all()
    idAtual = current_user.id
        
    return render_template("ChoseDependent.html", dependentes=dependentes, idAtual=idAtual)

@app.route('/adicionarProduto', methods=['GET', 'POST'])
@login_required
@user_type_required("funcionario", "adm")
def addProduto():
    form = adicionarProduto()
    produtos = Produto.query.all()
    
    if form.validate_on_submit():
        produtoExiste = Produto.query.filter_by(lanche = form.lanche.data).first()
        
        if(produtoExiste):
            flash("Produto com nome existente!")
            return redirect(url_for("addProduto"))
        else:
            
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




@app.route("/addProdutoAdm", methods=['GET', 'POST'])
def addProdutoAdm():
    form = adicionarProduto()
    produtos = Produto.query.all()
    
    if form.validate_on_submit():
        produtoExiste = Produto.query.filter_by(lanche = form.lanche.data).first()
        
        if(produtoExiste):
            flash("Produto com nome existente!")
            return redirect(url_for("addProdutoAdm"))
        else:
            
            produto = Produto(
                lanche = form.lanche.data,
                valor = form.valor.data,
                quantidade = form.quantidade.data
            )
            
            db.session.add(produto)
            db.session.commit()
            flash("Produto adicionado!", "notError")
        return redirect(url_for("homeAdm"))
    return render_template("adicionarProdutoAdm.html", form = form, produtos=produtos)



@app.route('/homeFunc', methods=['GET', 'POST'])
@login_required
@user_type_required("funcionario", "adm")
def homeFunc():
    global rooms_users
    id = "salaFunc"
    if id in rooms_users:
        rooms_users[id].discard(current_user.usuario)
        print("delete")
        print(rooms_users)
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
@user_type_required("funcionario", "adm")
def addProdutoQuantidade():
    produtoSemEstoque = Produto.query.all()
    form = confirmarForm()
    return render_template("adicionarEstoque.html", produtos = produtoSemEstoque, form=form)


@app.route("/adicionarEstoquesAdm", methods=['GET', 'POST'])
@login_required
@user_type_required("funcionario", "adm")
def addProdutoQuantidadeAdm():
    produtoSemEstoque = Produto.query.all()
    form = confirmarForm()
    return render_template("adicionarEstoqueAdm.html", produtos = produtoSemEstoque, form=form)


@app.route("/retirarEstoqueFim/<id>/<quantidade>", methods=['GET', 'POST'])
@login_required
@user_type_required("funcionario", "adm")
def retirarQuantidadeFim(id, quantidade):  
    produto = Produto.query.get(id)
    quantidade = int(quantidade)
    if(quantidade>produto.quantidade):
        flash("Estoque insuficiente!")

    elif(quantidade>0):
        produto.quantidade -= quantidade
        db.session.commit()
        flash("Estoque atualizado!", "notError")
    else:
        flash("Digite um valor válido!")
    
    return ""





@app.route("/adicionarEstoqueFim/<id>/<quantidade>", methods=['GET', 'POST'])
@login_required
@user_type_required("funcionario", "adm")
def addProdutoQuantidadeFim(id, quantidade):  
    produto = Produto.query.get(id)
    quantidade = int(quantidade)
    if(quantidade>0):
        produto.quantidade += quantidade
        db.session.commit()
        flash("Estoque atualizado!", "notError")
    else:
        flash("Digite um valor válido!")
    
    return ""
    


@app.route("/escolherRemoverProdutoAdm")
def choseProdutoAdm():
    produtos = Produto.query.all()
    return render_template("escolherRemoverProdutoAdm.html", produtos=produtos)



@app.route('/removerProdutoAdm/<int:id>', methods=['GET', 'POST'])
@login_required
@user_type_required("funcionario", "adm")
def removerProdutosAdm(id):
    obj = Produto.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for("choseProdutoAdm"))
       



@app.route("/escolherProduto", methods=['GET', 'POST'])
@login_required
@user_type_required("funcionario", "adm")
def choseProduto():
    produtos = Produto.query.all()
    return render_template("escolherRemoverProduto.html", produtos=produtos)


@app.route('/removerProduto/<int:id>', methods=['GET', 'POST'])
@login_required
@user_type_required("funcionario", "adm")
def removerProdutos(id):
    obj = Produto.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for("choseProduto"))
       
@socketio.on("mandarMensagemExclusao")
def confirmarPedido(id, mensagem):
    socketio.emit("mostrarExclusao", mensagem, room="dependente"+id)
    return ""
   
@socketio.on("mandarMensagemConclusao")
def confirmarPedido(id, mensagem):
    socketio.emit("mostrarConclusao", mensagem, room="dependente"+id)
    return ""

@app.route("/cancelarPedido")
def cancelarPedido():
    id = session.pop('id_pedido', 1)
    print(id)
    sleep(0.1)
    socketio.emit("deletarPedido", id, room="salaFunc")

    return ""

@app.route("/compraConfirmadaHistorico/<id>", methods=["GET", "POST"])
def criandoHistorico(id):
    id = int(id)
    counter_value = session.pop('counter_value', 1)


    obj = Produto.query.get(id)

    obj.quantidade = obj.quantidade-counter_value
    current_user.saldo = current_user.saldo-obj.valor*counter_value
    historico = Historico(
        nomeProduto = str(Produto.query.with_entities(Produto.lanche).filter_by(id = id).first()[0]),
        data = date.today(),
        valor = counter_value*obj.valor,
        quantidade = counter_value, 
        idDependente = current_user.id,
        nomeDependente = current_user.usuario

        )
    adm = ADM.query.get(1)
    adm.saldo +=obj.valor*counter_value
    db.session.add(historico)
    db.session.commit()
    return ""

@app.route('/comprarProduto/<int:id>', methods=['GET', 'POST'])
@login_required
@user_type_required("dependente")
def comprarProduto(id):

    global rooms_users

    print(rooms_users["salaFunc"])

    if rooms_users["salaFunc"]:

        form = confirmarFormQuantidade()
        obj = Produto.query.get(id)
        counter_value = int(request.form.get('counter_value', 1)) 
        if form.validate_on_submit():
            
            if current_user.saldo >= obj.valor*counter_value:
                if obj.quantidade>=counter_value:
                    

                    global cont
                    #pequena lógica para o codigo não passar de 1000
                    if(cont>1000):
                        cont =0
                    else:
                        cont = cont+1

                    mensagemFunc = {
                        "id":current_user.id,
                        "nome":current_user.usuario,
                        "lanche":obj.lanche,
                        "quantidade":counter_value,
                        "codigo":cont
                    }
                    #mandando os feedbacks tanto para o dependente quanto para o funcionario
                    socketio.emit("PedidoNovo", mensagemFunc, room="salaFunc")
                    flash(f"Compra realizada com sucesso! seu codigo é {cont}", "modalCodigo")
                    session['counter_value'] = counter_value
                    session['id_pedido'] = cont

                    return redirect(url_for("comprarProduto", id=id))

                else:
                    # return redirect(url_for("escolherProduto"))
                    flash("ESTOQUE insuficiente!")
                    return redirect(url_for("comprarProduto", id=id))
            else:

                flash("SALDO insuficiente!")
                return redirect(url_for("comprarProduto", id=id))
            
        return render_template("comprarProduto.html", obj=obj, form=form)
    else:
        flash("O sistema de compras está fechado no momento!")
        return redirect(url_for("escolherProduto"))

@app.route('/homeDependente', methods=['GET', 'POST'])
@login_required
@user_type_required("dependente")
def escolherProduto():
    produtos = Produto.query.all()
    return render_template("homeDependente.html", produtos =produtos)







