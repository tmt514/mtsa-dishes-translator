from app.app import app, redis_store
from app.models import db, Term, Similar
from app.data import add_data
import unittest
import os
import shutil


class AAFoodTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aafood-test.db'
        app.config['REDIS_URL'] = 'redis://localhost:6379/30'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.init_app(app)
            if os.path.exists('app/aafood.db') == True:
                #TODO: 未來的 DB 從 production 複製過去
                shutil.copyfile('app/aafood.db', 'app/aafood-test.db')
            if os.path.exists("app/aafood-test.db") == False:
                db.create_all()
                add_data()
            redis_store.init_app(app)

    def tearDown(self):
        # TODO: 未來的 DB 從 production 複製過去
        with app.app_context():
            db.session.remove() # 把當前的 session 移除掉
            #db.drop_all()      # 就不要移除 data, 以增加效率
            db.session.commit() # 記得要 commit, 不然多組 test 會有 error
            redis_store.flushdb()


