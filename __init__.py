from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'groupisgreat'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) 
#from trivia import main
