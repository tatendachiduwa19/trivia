from __init__ import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    correct = db.Column(db.Integer, nullable=False, default=0)
    total = db.Column(db.Integer, nullable=False, default=0)
    ArtsandLiterature = db.Column(db.Integer, nullable = False, default=0)
    FilmandTV = db.Column(db.Integer, nullable = False, default=0)
    FoodandDrink = db.Column(db.Integer, nullable = False, default=0)
    GeneralKnowledge = db.Column(db.Integer, nullable = False, default=0)
    Geography = db.Column(db.Integer, nullable = False, default=0)
    History = db.Column(db.Integer, nullable = False, default=0)
    Music = db.Column(db.Integer, nullable = False, default=0)
    science = db.Column(db.Integer, nullable = False, default=0)
    SocietyandCulture = db.Column(db.Integer, nullable = False, default=0)
    SportsandLeisure = db.Column(db.Integer, nullable = False, default=0)
    questions = db.relationship('Question', backref='user', lazy=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    question_id = db.Column(db.String(100), nullable = False)
    correct = db.Column(db.String(100), nullable=False)
    incorrect1 = db.Column(db.String(100), nullable=False)
    incorrect2 = db.Column(db.String(100), nullable=False)
    incorrect3 = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Text, db.ForeignKey('user.id'), nullable=False)
    db.UniqueConstraint('user_id', 'question_id', name='uix_1')
    def __repr__(self):
        return f"Question('{self.question}')"
