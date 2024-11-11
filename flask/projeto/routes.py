from flask import render_template, redirect, url_for, flash, request, session
from flask_socketio import SocketIO, join_room, emit
from projeto import app
from projeto.forms import adicionarSaldoRespo, CadastroForm, confirmarFormQuantidade, removerProduto, LoginForm, SaldoForm, adicionarProduto, confirmarForm
from projeto.models import Responsavel, Funcionario, Dependente, Produto, Historico, ADM
from projeto import db
from flask_login import login_user, logout_user, current_user, login_required
from bcrypt import _bcrypt, hashpw
from sqlalchemy import desc
from datetime import date


cont = 0
socketio = SocketIO(app)

@socketio.on("user_join")
def conectar_operador(id):
    join_room(id)

   
@app.route("/paginamensagens")
def mensagens():
    return render_template("painel_controle.html")



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
@login_required
def historico():
    dependentes_do_responsavel = Dependente.query.filter_by(idResponsavel=current_user.id).all()

    ids_dependentes = [dependente.id for dependente in dependentes_do_responsavel]

    historicos = Historico.query.filter(Historico.idDependente.in_(ids_dependentes)).order_by(desc(Historico.id)).all()


    

    return render_template("historico.html", historicos=historicos)
@app.route("/adicionarSaldoResponsavel/<saldo>", methods=['GET', 'POST'])
@login_required
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
def cardapio_func():
    return render_template("cardapioFuncionario.html", produtos = Produto.query.filter(Produto.quantidade>0).all())

    
@app.route("/cardapio")
def cardapio():
    return render_template("cardapioResponsavel.html", produtos = Produto.query.filter(Produto.quantidade>0).all())

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


@app.route("/historicoLanches")
def historicoLaches():
    historicos=[]
    
    historicos=[]
    
    
    
    historico_dependente = Historico.query.order_by(desc(Historico.id)).all()
    historicos.extend(historico_dependente)



    return render_template("historicoFunc.html", historicos=historicos)

@app.route('/perfil')
@login_required
def PerfilPage():
    dependentes = Dependente.query.filter_by(idResponsavel=current_user.id).all()
    historicos = []
    for dependente in dependentes: 
        historicos.extend(Historico.query.filter_by(idDependente=dependente.id).order_by(desc(Historico.id)).all())
    return render_template('PerfilResponsavel.html', dependentes=dependentes, historicos=historicos) 
    
    
@app.route('/removerSaldo/<valor>/<id>', methods=['GET', 'POST'])
@login_required
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
        
    return render_template("ChoseDependent.html", dependentes=dependentes, idAtual=idAtual)

@app.route('/adicionarProduto', methods=['GET', 'POST'])
@login_required
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

@app.route("/adicionarEstoqueFim/<id>/<quantidade>", methods=['GET', 'POST'])
@login_required
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
        
@socketio.on("mandarMensagem")
def confirmarPedido(id, mensagem):
    socketio.emit("mostrarConclusao", mensagem, room="dependente"+id)
    return ""

@app.route("/cancelarPedido/<int:id>")
def cancelarPedido(id):

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
def comprarProduto(id):
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
    

@app.route('/homeDependente', methods=['GET', 'POST'])
@login_required
def escolherProduto():
    produtos = Produto.query.all()
    return render_template("homeDependente.html", produtos =produtos)







