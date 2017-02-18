import mafan
from app.models import db, Term

def add_vegetables(dryrun=True):
    try:
        f = open("app/data/vegetables")
        for line in f:
            i = 0
            while i < len(line):
                if not all(ord(c) < 128 for c in line[i]):
                    break
                i += 1

            e = line[0:i]
            elist = e.split(",")
            c = line[i:-1]

            for x in elist:
                x = x.strip().lower()
            
                q = Term.query.filter_by(english=x, chinese=c).first()
                if q == None:
                    print("%s, %s" % (c, x))
                    q = Term(english=x, chinese=c)
                    if dryrun == False:
                        db.session.add(q)

    except:
        pass

    if dryrun == False:
        db.session.commit()
