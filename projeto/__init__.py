from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_message = "Por favor, faça login para acessar esta página!"
login_manager.login_view = 'login'
app = Flask(__name__)
app.config.from_pyfile("config.cfg")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SECRET_KEY"] = '934fhdr58g6jj643dg4d55fg'

s = URLSafeTimedSerializer(app.config["SECRET_KEY"])

db.init_app(app)
bcrypt = Bcrypt(app)

mail = Mail(app)

login_manager.init_app(app)


from projeto import routes
