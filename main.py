from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'groupisgreat'

# bcrypt = Bcrypt(app) for password hiding
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

@app.route('/')
def create_app():
     # app = Flask(__name__)
     # return '<h1>Hello World!</h1>'
     # app.config['SECRET_KEY'] = 'groupisgreat'
     return render_template('homepage.html')

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5001)





