from projeto import db, login_manager
from projeto import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Responsavel.query.get(int(user_id))   

class Responsavel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    senha = db.Column(db.String(length=30), nullable=False, unique=True)
    
    @property
    def senhacrip(self):
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, senha_texto):
        self.senha = bcrypt.generate_password_hash(senha_texto).decode('utf-8')


class Funcionario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    usuario = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=30), nullable=False, unique=True)
    senha = db.Column(db.String(length=30), nullable=False, unique=True)




def converte_senha(self, senha_texto_claro):
    return bcrypt.check_password_hash(self.senha, senha_texto_claro)