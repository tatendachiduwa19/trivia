from __init__ import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    correct = db.Column(db.Integer, nullable=False, default=0)
    total = db.Column(db.Integer, nullable=False, default=0)

    total_ArtsandLiterature = db.Column(db.Integer, nullable = False, default=0)
    correct_ArtsandLiterature = db.Column(db.Integer, nullable = False, default=0)

    total_FilmandTV = db.Column(db.Integer, nullable = False, default=0)
    correct_FilmandTV = db.Column(db.Integer, nullable = False, default=0)

    total_FoodandDrink = db.Column(db.Integer, nullable = False, default=0)
    correct_FoodandDrink = db.Column(db.Integer, nullable = False, default=0)

    total_GeneralKnowledge = db.Column(db.Integer, nullable = False, default=0)
    correct_GeneralKnowledge = db.Column(db.Integer, nullable = False, default=0)

    total_Geography = db.Column(db.Integer, nullable = False, default=0)
    correct_Geography = db.Column(db.Integer, nullable = False, default=0)

    total_History = db.Column(db.Integer, nullable = False, default=0)
    correct_History = db.Column(db.Integer, nullable = False, default=0)

    total_Music = db.Column(db.Integer, nullable = False, default=0)
    correct_Music = db.Column(db.Integer, nullable = False, default=0)

    total_science = db.Column(db.Integer, nullable = False, default=0)
    correct_science = db.Column(db.Integer, nullable = False, default=0)

    total_SocietyandCulture = db.Column(db.Integer, nullable = False, default=0)
    correct_SocietyandCulture = db.Column(db.Integer, nullable = False, default=0)

    total_SportsandLeisure = db.Column(db.Integer, nullable = False, default=0)
    correct_SportsandLeisure = db.Column(db.Integer, nullable = False, default=0)
    
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

db.create_all()
