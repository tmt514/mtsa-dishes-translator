from app.app import app
from app.models import db, Term
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

    def test_assertion(self):
        assert 10 + 10 == 20

