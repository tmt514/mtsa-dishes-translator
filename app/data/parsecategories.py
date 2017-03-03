from app.models import db, Category


def add_categories():
    try:
        f = open('app/data/categories', 'r')
        for line in f:
            chain = line.split("::")
            for i in range(len(chain)):
                chain[i] = chain[i].strip().lower()
                q = Category.query.filter_by(name=chain[i]).first() or Category(name=chain[i])
                db.session.add(q)
        db.session.commit()
        f.seek(0, 0)
        for line in f:
            chain = list(map(lambda x: x.strip().lower(), line.split("::")))
            for i in range(1, len(chain)):
                q = Category.query.filter_by(name=chain[i]).first()
                p = Category.query.filter_by(name=chain[i-1]).first()
                print(p.name, p.id, q.name, q.id)
                q.parent = p
                db.session.add(q)

        db.session.commit()
    except Exception as e:
        print("\033[1;31m%s\033[m" % e)
        pass
