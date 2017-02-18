from app.models import db, Term, Photo



def add_pokemons(dryrun=True):
    try:
        f = open('app/data/pokemon', 'r')
        for line in f:
            v = line.split(" ")
            # 編號、中文、日文、英文
            seq = int(v[0][1:])
            e = " ".join(v[3:]).strip().lower()
            c = v[1].strip()
            if Term.query.filter_by(english=e, chinese=c).first():
                continue

            print("%s, %s" % (c, e))

            term = Term(english=e, chinese=c, hit_counts=0)
            if not dryrun:
                db.session.add(term)
            if seq <= 151:
                photo = Photo(term=term, url="https://rankedboost.com/wp-content/plugins/ice/riot/poksimages/pokemons/%03d.png" % (seq))
                if not dryrun:
                    db.session.add(photo)
            elif seq <= 251:
                photo = Photo(term=term, url="https://rankedboost.com/wp-content/plugins/ice/riot/poksimages/pokemons2/%03d.png" % (seq))
                if not dryrun:
                    db.session.add(photo)
        
        db.session.commit()
    except Exception as e:
        print(e)
        pass
            
            
