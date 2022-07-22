from __init__ import db
from models import User
def update(category,username,correct):
    user = User.query.filter_by(username = username).first()
    if category == "Arts & Literature":
        if correct:
            user.correct_Arts_and_Literature +=1
        user.total_Arts_and_Literature += 1
    elif category == "Film & TV":
        user.total_Film_and_TV += 1
        if correct:
            user.correct_FilmandTV += 1
    elif category == "Food & Drink":
        user.total_Food_and_Drink += 1
        if correct:
            user.correct_Food_and_Drink += 1
    elif category == "General Knowledge":
        user.total_GeneralKnowledge += 1
        if correct:
            user.correct_GeneralKnowledge += 1
    elif category == "Geography":
        user.total_Geography += 1
        if correct:
            user.correct_Geography += 1
    elif category == "History":
        user.total_History += 1
        if correct:
            user.correct_History += 1
    elif category == "Music":
        user.total_Music = user.total_Music + 1
        if correct:
            user.correct_Music = user.total_Music + 1
    elif category == "Science":
        user.total_Science += 1
        if correct:
            user.correct_Science += 1
    elif category == "Society & Culture":
        user.total_Society_and_Culture += 1
        if correct:
            user.correct_Society_and_Culture += 1
    elif category == "Sport & Leisure":
        user.total_Sports_and_Leisure += 1
        if correct:
            user.correct_Sports_and_Leisure += 1
    db.session.commit()