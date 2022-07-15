import requests
import random
import time
from threading import Thread
from pytimedinput import timedInput
from pytimedinput import timedKey
import sqlalchemy as db
import pandas as pd
import copy
# install pytimedinput!!!

# https://the-trivia-api.com/
# user can choose number of questions(up to 20)
# desired difficulty (easy, medium, hard), and question category

# should have method to print categories, and get response
# method to get difficulty
# method to get number of questions

# can store quiz in database if user wishes to return to a a past quiz?

# data is a list where each element is a dictionary for each question
# ( has the question, the correct answers and incorrectAnswers)

# iterate through each question's dictionary

# this is an example url and quiz


# url = 'https://the-trivia-api.com/api/' \
# + 'questions?categories=science&limit=10&region=US&difficulty=medium'
# response = requests.get(url)
# data = response.json()
# score = 0
# total = 10
# # end of example


# Testing function examples

def func1(x):
    x = x - 1
    return x


def func2(x, y):
    return x + y


# global variable used for the countdown
count = True
# run the countdown for each question


def runn():
    i = 15
    print('Choose an Answer: ')
    print(i, end='')

    while i >= 0:
        i -= 1
        time.sleep(1)  # sleep one second
        if count is False:
            break
        print('\r' + str(i) + ' ', end='', flush=True)  # update timer


# display categories
def print_categories():
    print(
      '''
      0- Arts & Literature       5- History
      1- Film & TV               6- Music
      2- Food & Drink            7- Science
      3- General Knowledge       8- Society & Culture
      4- Geography               9- Sports & Leisure

      ''')


# get category selection and return it
def get_category():
    print_categories()
    categories = {'0': 'arts_and_literature', '1': 'film_and_tv',
                  '2': 'food_and_drink', '3': 'general_knowledge',
                  '4': 'geography', '5': 'history', '6': 'music',
                  '7': 'science', '8': 'society_and_culture',
                  '9': 'sports_and_leisure'}

    # get response and check if it is an integer
    check_category = True
    while check_category:
        try:
            response = input("Please choose a category and press enter: ")
            category = categories[response]
            check_category = False  # end the loop if successful

        # if input is not int or not in the range 0-9, continue loop
        except KeyError:
            print('Please input a number 0-9')
    return category


# get the difficulty (easy, medium, hard) and return it
def get_difficulty():
    choices = {"1": "easy", "2": "medium", "3": "hard"}
    check_difficulty = True
    while check_difficulty:
        try:
            chosen = input("Choose difficulty. \n"
                           " 1. Easy \n 2. Medium \n 3. Hard \n : ")
            difficulty = choices[chosen]
            check_difficulty = False
        except KeyError:
            print('Please input a number 1-3')
    return difficulty


# get input on the number of questions and return it
def get_questions():
    question = input("How many questions would you like to answer?: 1-20 ")
    while not question.isnumeric() or int(question) > 20 or int(question) <= 0:
        question = input("How many questions would you like to answer?: 1-20 ")
    questions = str(question)
    return questions


# create the quiz and returns the list of questions
def create_quiz(category, difficulty, questions):
    url = 'https://the-trivia-api.com/api/questions?categories=' \
        + category + '&limit=' \
        + questions + '&region=US&difficulty=' + difficulty
    response = requests.get(url)
    data = response.json()
    return data


# takes the list of questions as parameter and runs the quiz
def run_quiz(quiz, total):
    score = 0
    total = total
    global count  # boolean used for countdown

    for i in quiz:
        print()
        print("********************************")
        print(f"Score : {score} / {total}")

        # print question
        print(i['question'])

        # list all answer choices
        # print them in a random order'])
        list_i = [i['correctAnswer']] + i['incorrectAnswers']

        a = random.choice(list_i)
        list_i.remove(a)
        b = random.choice(list_i)
        list_i.remove(b)
        c = random.choice(list_i)
        list_i.remove(c)
        d = list_i[0]

        # determine which choice is the right answer
        if i['correctAnswer'] == a:
            correct = 'a'
        elif i['correctAnswer'] == b:
            correct = 'b'
        elif i['correctAnswer'] == c:
            correct = 'c'
        else:
            correct = 'd'

        # prompt user to select an option
        print(f" (a) {a}")
        print(f" (b) {b}")
        print(f" (c) {c}")
        print(f" (d) {d}")
        print(f" press \"q\" to quit")

        # start the countdown
        t = Thread(target=runn)
        t.start()

        # the user has 15 seconds and can only select a,b,c,d, or q
        answer, timedOut = timedKey(timeout=16, allowCharacters='abcdq')
        count = False
        print()

        # test if user gives correct input,
        if timedOut:  # if ran out of time
            print("Sorry you ran out of time!")
            print(f"Correct Answer: {i['correctAnswer']}")
        elif answer == correct:  # if correct
            score += 1
            print("Congratulations you are correct!")
        elif answer == 'q':  # to quit
            break
        else:  # if incorrect
            print("Wrong! :(")
            print(f"Correct Answer: {i['correctAnswer']}")
        print("********************************")
        time.sleep(2)
        count = True

    print(f"Your Score is: {score}/{total}")
    print()


# takes user response, and the correct answer?
# (may not be needed)
def compare_answers(response, correct_answer):
    pass
    # print the many different responses


def make_database(data):
    # create dataframe
    for question in data:
        incorrect = question['incorrectAnswers']
        question['incorrectAnswers'] = incorrect[0] + '*' \
            + incorrect[1] + '*' + incorrect[2]
    df = pd.DataFrame(data)

    # remove unnecessary parts
    del df['type']
    del df['id']
    del df['tags']
    del df['difficulty']
    del df['regions']

    # create database
    engine = db.create_engine('sqlite:///trivia.db')
    df.to_sql('past_questions', con=engine, if_exists='replace', index=False)
    query_result = engine.execute("SELECT * FROM past_questions;").fetchall()


def update_database(data):
    # create dataframe
    for question in data:
        incorrect = question['incorrectAnswers']
        question['incorrectAnswers'] = incorrect[0] + '*' \
            + incorrect[1] + '*' + incorrect[2]
    df = pd.DataFrame(data)

    # remove unnecessary parts
    del df['type']
    del df['id']
    del df['tags']
    del df['difficulty']
    del df['regions']

    # update database
    engine = db.create_engine('sqlite:///trivia.db')
    df.to_sql('past_questions', con=engine, if_exists='append', index=False)


def revisit():
    engine = db.create_engine('sqlite:///trivia.db')
    query_result = engine.execute("SELECT * FROM past_questions;").fetchall()
    questions = []

    # create dictionaries from query result to add to the list of questions
    for question in query_result:
        d = {}
        d['correctAnswer'] = question[1]
        incorrectAnswers = question[2].split('*')
        d['incorrectAnswers'] = incorrectAnswers
        d['question'] = question[3]
        questions.append(d)

    # randomly choose until we have 10 (or less if not possible)
    random_questions = []
    while len(random_questions) < 10 and len(questions) > 0:
        q = questions.pop(random.randint(0, len(questions)-1))
        random_questions.append(q)
    return random_questions


if __name__ == '__main__':
    first_run = True  # boolean to determine if this is the first run
    while True:
        # different menu options for first run vs not first run
        run = True
        if not first_run:
            while run:
                print('Choose an option and press enter:'
                      '\n "n" to begin a new quiz \n "r" '
                      'to revist past questions \n "q" to quit')
                option = input("option:")
                if option in 'nqr':
                    run = False
        else:
            while run:
                print('Choose an option and press enter: '
                      '\n "n" to begin a new quiz \n "q" to quit ')
                option = input("option:")
                if option in 'nq':
                    run = False

        # revisitng past questions
        if option == 'r':
            quiz = revisit()
            run_quiz(quiz, len(quiz))
        elif option == 'q':
            break
        else:  # new
            category = get_category()
            difficulty = get_difficulty()
            questions = get_questions()
            quiz = create_quiz(category, difficulty, questions)
            run_quiz(quiz, int(questions))

            if first_run:
                make_database(copy.deepcopy(quiz))
                first_run = False
            else:
                update_database(copy.deepcopy(quiz))
