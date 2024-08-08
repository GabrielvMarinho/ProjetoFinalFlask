from projeto import db, login_manager
from projeto import bcrypt
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float
from flask import session

@login_manager.user_loader
def load_user(user_id):##arrumar a questão do current.user (ta mudando o saldo quando vai no home)
    # Aqui você vai buscar o usuário pelo ID e, se possível, pelo tipo
    # Vou usar a variável `user_type` para exemplificar
    user_type = session.get('user_type')
    if user_type == 'responsavel':
        return Responsavel.query.get(int(user_id))
    elif user_type == 'dependente':
        return Dependente.query.get(int(user_id))
    elif user_type == 'funcionario':
        return Funcionario.query.get(int(user_id))
    return None

class Dependente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    saldo = db.Column(db.Integer, nullable=False, unique=False, default=0)
    usuario = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    senha = db.Column(db.String(length=30), nullable=False)
    idResponsavel = db.Column(db.Integer)
    user_type = 'dependente'
    @property
    def senhacrip(self):
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, senha_texto):
        self.senha = bcrypt.generate_password_hash(senha_texto).decode('utf-8')
        
    def converte_senha(self, senha_texto_claro):
        return bcrypt.check_password_hash(self.senha, senha_texto_claro)
    
class Responsavel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    senha = db.Column(db.String(length=30), nullable=False)
    saldo = db.Column(db.Double, nullable=False, default=0)
    user_type = 'responsavel'
    @property
    def senhacrip(self):
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, senha_texto):
        self.senha = bcrypt.generate_password_hash(senha_texto).decode('utf-8')
        
    def converte_senha(self, senha_texto_claro):
        return bcrypt.check_password_hash(self.senha, senha_texto_claro)
    
    def getId(self):
        return self.id
    
class Funcionario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    usuario = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    senha = db.Column(db.String(length=30), nullable=False)
    user_type = 'funcionario'
    @property
    def senhacrip(self):
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, senha_texto):
        self.senha = bcrypt.generate_password_hash(senha_texto).decode('utf-8')
        
    def converte_senha(self, senha_texto_claro):
        return bcrypt.check_password_hash(self.senha, senha_texto_claro)
    
    def getId(self):
        return self.id
    
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    lanche = db.Column(db.String(length=30), nullable=False)
    valor = db.Column(db.Integer, nullable=False)

class Historico(db.Model):
    data = db.Column(db.Date, primary_key = True)
    valor = db.Column(db.Integer, nullable=False)