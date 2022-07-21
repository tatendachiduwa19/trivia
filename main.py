from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import *
from forms import *
import random
import requests
app = Flask(__name__)
app.config['SECRET_KEY'] = 'groupisgreat'
proxied = FlaskBehindProxy(app)  ## handle redirects

# bcrypt = Bcrypt(app) for password hiding
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

@app.route('/')
@app.route('/static/index.html')
def create_app():
     return render_template('index.html', title="Trivia Game")

@app.route('/login', methods=['GET', 'POST'])
@app.route('/static/login.html', methods=['GET', 'POST'])
def login():
     # log in
     form = LoginForm()
     if form.validate_on_submit(): # checks if entries are valid
          email=form.email.data
          password=form.password.data
          # TO-DO: CHECK AGAINST DATA IN DATABASE TO VALIDATE LOGIN
          flash(f'Logging you in', 'success')
          return redirect(url_for('category')) # if so - send to category
     return render_template('login.html', title='Login', form=form)

@app.route('/category', methods = ['GET','POST'])
@app.route('/static/category.html', methods = ['GET','POST'])
def start():
     #show categories
     return render_template('category.html')

@app.route('/difficulty', methods = ['GET','POST'])
def get_difficulty():
     #get category info then ask for difficulty
     global category
     category = request.form['category']  
     return render_template('difficulty.html')

@app.route('/questions', methods = ['GET','POST'])
def get_questions():
     #get difficulty then ask for questions
     global difficulty
     difficulty = request.form['difficulty']
     return redirect(url_for('questions'))

@app.route('/done',methods = ['GET','POST'])
def questions():
     #get questions, then redirect
     global questions
     form = Questions()
     if form.validate_on_submit():
          questions = form.question.data
          quiz()
          return redirect(url_for('run')) # placeholder
     return render_template('questions.html', form=form)

# @app.route('/quiz')
def quiz():
     global data
     global correct
     global current_question
     global answers
     url = 'https://the-trivia-api.com/api/questions?categories=' \
        + category + '&limit=' \
        + str(questions) + '&region=US&difficulty=' + str(difficulty)
     response = requests.get(url)
     data = response.json()
     correct = 0
     current_question = 0  #0 to 9
     answers = [i['correctAnswer'] for i in data]

@app.route('/run',methods = ['GET', 'POST'])
def run():
     if current_question< len(data):
          q = data[current_question]
          options = q['incorrectAnswers'] + [q['correctAnswer']]
          random.shuffle(options)
          return render_template('question.html', question = q, options = options)
     else:
          #return '<h1> Correct Answers: ' + str(correct) + '</h1>'
          return render_template('result.html', score=str((correct/len(data)*100)))
        
@app.route("/answered", methods = ['POST'])
def check_answer():
     global correct
     global current_question
    
     id = data[current_question]['id']
     answered = request.form[id]
     correctAnswer = answers[current_question]
     if answered == correctAnswer:
          correct = correct +1
     current_question +=1  
     return render_template('answer.html', answered = answered, correct = correctAnswer) 

@app.route('/register', methods=['GET', 'POST'])
@app.route('/static/register.html', methods=['GET', 'POST'])
def register():
     form = RegistrationForm()
     if form.validate_on_submit(): # checks if entries are valid
          user = User(username=form.username.data, email=form.email.data, password=form.password.data)
          db.session.add(user)
          db.session.commit()
          flash(f'Account created for {form.username.data}!', 'success')
          return redirect(url_for('home')) # if so - send to home page
     return render_template('register.html', title='Register', form=form)
     
if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5001)
