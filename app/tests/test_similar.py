from app.tests.test_app import AAFoodTestCase
from app.models import db, Similar, Term

class AppTestCase(AAFoodTestCase):

    def test_db_create(self):
        term_a = Term(english='test', chinese='測試')
        term_b = Term(english='bamboo', chinese='竹子')
        db.session.add(term_a)
        db.session.add(term_b)
        similar = Similar(x=term_a, y=term_b, score=0.8)
        term_a.similars.append(similar)
        print(len(Term.query.all()))

    def test_assertion(self):
        assert 10 + 10 == 20

