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
        user.total_Music += 1
        if correct:
            user.correct_Music += 1
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

def get_stats(username):
    user = User.query.filter_by(username = username).first()
    stats = {}
    if user.total_Arts_and_Literature != 0 :
        stats['Arts & Literature'] = str((user.correct_Arts_and_Literature/user.total_Arts_and_Literature)*100)+ "% correct"
    else:
        stats['Arts & Literature'] = "None answered"

    if user.total_Film_and_TV !=0:
        stats['Film & TV'] = str((user.correct_Film_and_TV/user.total_Film_and_TV)*100) + "% correct"
    else:
        stats['Film & TV'] = "None answered"

    if user.total_Food_and_Drink!=0:
        stats['Food & Drink'] = str((user.correct_Food_and_Drink/user.total_Food_and_Drink)*100) + "% correct"
    else: stats['Food & Drink'] = "None answered"

    if user.total_GeneralKnowledge!=0:
        stats['General Knowledge'] = str((user.correct_GeneralKnowledge/user.total_GeneralKnowledge)*100) + "% correct"
    else:
        stats["General Knowledge"] = "None answered"

    if user.total_Geography!=0:
        stats['Geography'] = str((user.correct_Geography/user.total_Geography)*100)+ "% correct"
    else:
        stats['Geography'] = "None answered"
    
    if user.total_Music !=0:
        stats['Music'] = str((user.correct_Music/user.total_Music)*100) + "% correct"
    else: 
        stats['Music'] = "None answered"
    
    if user.total_Science !=0:
        stats['Science'] = str((user.correct_Science/user.total_Science)*100)+ "% correct"
    else: 
        stats['Science'] = "None answered"
    
    if user.total_Society_and_Culture!=0:
        stats['Society & Culture'] = str((user.correct_Society_and_Culture/user.total_Society_and_Culture)*100)+ "% correct"
    else: 
        stats['Society & Culture'] = "None answered"
    
    if user.total_Sports_and_Leisure!=0:
        stats['Sport & Leisure'] = str((user.correct_Sports_and_Leisure/user.total_Sports_and_Leisure)*100) + "% correct"
    else: 
        stats['Sport & Leisure'] = "None answered"
    
    if user.total_History!=0:
        stats['History'] = str((user.correct_History/user.total_History)*100) + "% correct"
    else:
        stats['History'] = "None answered"
    return stats