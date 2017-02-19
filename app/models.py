from .app import app
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


class Term(db.Model):
    """ 最原始的中英對照字典表, 此外有 hit_count 記錄被查詢的頻率 """
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(128), index=True)
    chinese = db.Column(db.String(128), index=True)
    hit_counts = db.Column(db.Integer)

    similars = db.relationship('Similar', foreign_keys='Similar.x_id', backref='term', lazy='dynamic')

    #similars = db.relationship('Term', secondary=similars,
    #        primaryjoin=(id==similars.c.x),
    #        secondaryjoin=(id==similars.c.y),
    #        backref=db.backref('term',lazy='dynamic'))

    photos = db.relationship('Photo', backref='term', lazy='dynamic')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Similar(db.Model):
    """ 描述兩個 Term 之間是否相近 """
    id = db.Column(db.Integer, primary_key=True)
    x_id = db.Column(db.Integer, db.ForeignKey('term.id'), index=True)
    y_id = db.Column(db.Integer, db.ForeignKey('term.id'), index=True)
    x = db.relationship(Term, foreign_keys=x_id, backref='similar')
    y = db.relationship(Term, foreign_keys=y_id, backref='similar_to')
    
    score = db.Column(db.Float)

class Location(db.Model):
    """ 記錄附近的商家 """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    phone = db.Column(db.String(128))
    address = db.Column(db.Text())
    open_hours = db.Column(db.Text()) # 是一個 structure, 描述每天什麼時候開門

    website_url = db.Column(db.Text())
    facebook_url = db.Column(db.Text())
    yelp_url = db.Column(db.Text())

    photos = db.relationship('Photo', backref='location', lazy='dynamic')


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class Photo(db.Model):
    """ 儲存照片的網址, 上傳者與相關資訊 """
    id = db.Column(db.Integer, primary_key=True)
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'), index=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), index=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    url = db.Column(db.Text())
    comment = db.Column(db.Text(), index=True)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    


class User(db.Model):
    """ 使用者資料, 以 sender id 作為索引 """
    id = db.Column(db.Integer, index=True)
    senderid = db.Column(db.String(128), primary_key=True)
    # fbuid = db.Column(db.String(128), index=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Joke(db.Model):
    """ 使用者資料, 以 sender id 作為索引 """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1024))
    # fbuid = db.Column(db.String(128), index=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
