from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from .models import Responsavel, Funcionario, Dependente


class CadastroForm(FlaskForm):
    def validate_email_responsavel(self, check_email):
        email = Responsavel.query.filter_by(email = check_email.data).first()
        if email:
            raise ValidationError("E-mail já existe, cadastre outro email.")
    def validate_email_funcionario(self, check_email):
        email = Funcionario.query.filter_by(email = check_email.data).first()
        if email:
            raise ValidationError("Email já existe, cadastre outro email.")
    def id(self):
        id= Responsavel.query.filter_by(id = id.data).first()

    usuario = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='E-mail:', validators=[Email(), DataRequired()])
    senha1 = PasswordField(label='Senha:', validators=[Length(min=4), DataRequired()])
    senha2 = PasswordField(label='Confirmação de senha:', validators=[EqualTo('senha1'), DataRequired()])
    submit = SubmitField(label='Cadastrar')

class LoginForm(FlaskForm):
    usuario = StringField(label="Usuário", validators=[DataRequired()])
    senha = PasswordField(label="Senha", validators=[DataRequired()])
    submit = SubmitField(label="Log In")   

class SaldoForm(FlaskForm):
    idDependente = FloatField(label="Id do dependente", validators=[DataRequired()])
    saldo = FloatField(label="Valor a ser adicionado", validators=[NumberRange(min=1), DataRequired()])
    submit = SubmitField(label="Adicionar")