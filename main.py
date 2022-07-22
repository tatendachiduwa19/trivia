from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_session import Session
from __init__ import app, db, bcrypt
from models import *
from forms import *
import random
import requests
from statistics import update, get_stats


Session(app)

# home page
@app.route('/')
@app.route('/static/index.html')
def home():
     return render_template('index.html', title="Trivia Game")

# login route
@app.route('/login', methods=['GET', 'POST'])
@app.route('/static/login.html', methods=['GET', 'POST'])
def login():
     global user
     # log in
     form = LoginForm()
     if form.validate_on_submit(): # checks if entries are valid
          email=form.email.data
          password=form.password.data
          # TO-DO: CHECK AGAINST DATA IN DATABASE TO VALIDATE LOGIN
          user = User.query.filter_by(email=form.email.data).first()
          if user and bcrypt.check_password_hash(user.password, form.password.data):
               # flash(f'Logging you in', 'success')
               session['username'] = user.username
               return redirect(url_for('home'))
          else:
               flash('Login Unsuccessful. Please check email and password', 'danger')
     return render_template('login.html', title='Login', form=form)

# logout route
@app.route('/logout')
def logout():
     session.pop('username', None)
     return redirect(url_for('home'))

# show categories
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


# create the quiz
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

@app.route('/retry',methods = ['GET', 'POST'])
def retry():
     global current_question
     global correct
     current_question = 0
     correct = 0
     return redirect(url_for('run'))

#run the quiz
@app.route('/run',methods = ['GET', 'POST'])
def run():
     global correct
     if current_question< len(data):
          q = data[current_question]
          options = q['incorrectAnswers'] + [q['correctAnswer']]
          random.shuffle(options)

          return render_template('question.html', question = q, options = options, n = current_question +1, c = correct, t = len(data))
     else:
          #return '<h1> Correct Answers: ' + str(correct) + '</h1>'
          return render_template('result.html', score=str((correct/len(data)*100)))

        
@app.route("/answered", methods = ['POST'])
def check_answer():
     global correct
     global current_question
     global user
     user = User.query.filter_by(username = session['username']).first()
     id = data[current_question]['id']
     answered = request.form[id]
     correctAnswer = answers[current_question]
     if answered == correctAnswer:
          correct = correct + 1
          a = True
     else:
          a = False
     update(data[current_question]['category'], session['username'], a)
     current_question += 1  
     return render_template('answer.html', answered = answered, correct = correctAnswer) 

@app.route('/register', methods=['GET', 'POST'])
@app.route('/static/register.html', methods=['GET', 'POST'])
def register():
     form = RegistrationForm()
     if form.validate_on_submit(): # checks if entries are valid
          pwd_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")   
          user = User(username = form.username.data, email = form.email.data, password = pwd_hash)
          try:
               db.session.add(user)
               db.session.commit()
          except:
               flash('username or email taken, try again')
               return render_template('register.html', title='Register', form=form)    
          db.session.add(user)
          db.session.commit()
          # flash(f'Account created for {form.username.data}!', 'success')
          return redirect(url_for('login')) # if so - send to home page
     return render_template('register.html', title='Register', form=form)

@app.route('/stats')   
def stats():
     global user
     stats = get_stats(session['username'])
     return render_template('stats.html', stats=stats)
if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5001)
