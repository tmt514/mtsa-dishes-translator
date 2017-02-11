import mafan
from app.models import db, Term

def add_dishes(dryrun=True):
    try:
        f = open("app/data/dishes")
        for line in f:
            i = 0
            while i < len(line):
                if all(ord(c) < 128 for c in line[i]):
                    break
                i += 1
            c = line[0:i]
            e = line[i:-2]

            c = mafan.to_traditional(c)
            e = e.strip().lower()
            print("%s, %s" % (c, e))
            if dryrun == False:
                q = Term.query.filter_by(english=e, chinese=c).first()
                if q == None:
                    q = Term(english=e, chinese=c)
                    db.session.add(q)

    except:
        pass
    if dryrun == False:
        db.session.commit()
