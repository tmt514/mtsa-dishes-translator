from app.models import db, Term, Photo

import json

def add_pokemons(dryrun=True):
    try:
        f = open('app/data/pokemon_data', 'r')
        for line in f:
            v = json.loads(line)
            # 編號、中文、日文、英文
            seq = v['seq']
            e = v['english']
            c = v['chinese']
            if Term.query.filter_by(english=e).first():
                pass
            else:
                print("%s, %s" % (c, e))

                term = Term(english=e, chinese=c, hit_counts=0)
                if not dryrun:
                    db.session.add(term)

            term = Term.query.filter_by(english=e, chinese=c).first()
            photo = Photo.query.filter_by(term=term).first()

            if photo is not None:
                if v['image'] is not None:
                    photo.url = "http:" + v['image']
                else:
                    print("Warning for " + v['seq'] + ": " + v['chinese'])
            else:
                photo = Photo(term=term)
                if v['image'] is not None:
                    photo.url = "http:" + v['image']
                else:
                    print("Warning for " + v['seq'] + ": " + v['chinese'])
                if not dryrun:
                    db.session.add(photo)
        
        db.session.commit()
    except Exception as e:
        print(e)
        pass
            
            
