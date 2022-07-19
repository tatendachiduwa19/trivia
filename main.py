from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import *
from forms import *
import requests
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
     return render_template('index.html', title="Trivia Game")

@app.route('/category', methods = ['GET','POST'])
def start():
     return render_template('category.html')  #show categories

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
        return render_template('question.html', data = data, current_question = current_question) 
     else:
        return '<h1> Correct Answers: ' + str(correct) + '</h1>'
        
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

     
if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5001)





