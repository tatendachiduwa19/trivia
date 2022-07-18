from flask import Flask

app = Flask(__name__)

@app.route('/')
def create_app():
     app = Flask(__name__)
     return '<h1>Hello World!</h1>'
     app.config['SECRET_KEY'] = 'groupisgreat'

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=5001)
   
     