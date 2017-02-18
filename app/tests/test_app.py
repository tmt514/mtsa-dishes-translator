from app.app import app
from app.models import db, Term, Similar
import unittest

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aafood-test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.init_app(app)
            db.create_all()
            q = len(Term.query.all())
            print(q)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_db_create(self):
        term_a = Term(english='test', chinese='測試')
        term_b = Term(english='bamboo', chinese='竹子')
        db.session.add(term_a)
        db.session.add(term_b)
        similar = Similar(x=term_a, y=term_b, score=0.8)
        term_a.similars.append(similar)
        print("\033[1;33m測試log\033[m")

    def test_assertion(self):
        assert 10 + 10 == 20

