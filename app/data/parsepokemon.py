from app.models import db, Term, Photo, Description, Category

import json

def add_pokemons(dryrun=True):
    try:
        pkmn = Category.query.filter_by(name="pokemon").first() or Category(name="pokemon")
        db.session.add(pkmn)

        f = open('app/data/pokemon_data', 'r')
        for line in f:
            v = json.loads(line)
            # 編號、中文、日文、英文
            seq = v['seq']
            e = v['english'].lower().strip()
            c = v['chinese'].strip()
            if Term.query.filter_by(english=e).first():
                pass
            else:
                # print("%s, %s" % (c, e))

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

            if pkmn not in term.categories.all():
                term.categories.append(pkmn)

            desc = v['desc']
            if desc is not None:
                d = Description.query.filter_by(term=term).first() or Description(term=term, content=desc, subheading="習性")
                db.session.add(d)
        
        if not dryrun:
            db.session.commit()
    except Exception as e:
        print(e)
        pass
            
            
