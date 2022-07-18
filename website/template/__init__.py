from flask import Flask

@app.route('/')
def create_app():
     app = Flask(__name__)
     return '<h1>Hello World!</h1>'
     app.config['SECRET_KEY'] = 'groupisgreat'
   
     return app