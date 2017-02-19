import mafan
from app.models import db, Joke

def add_jokes(dryrun=True):
    try:
        f = open("app/data/coldjoke")
        current = 0
        max_line = Joke.query.filter_by().count()
        print(max_line)
        for line in f:
            current = current + 1
            if current <= max_line:
                continue
            print(current)
            joke = Joke(id=current, content=line)
            db.session.add(joke)
    except:
        pass

    if dryrun == False:
        db.session.commit()
