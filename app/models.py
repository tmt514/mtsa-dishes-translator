from .app import app
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


similars = db.Table('terms',
        db.Column('x', db.Integer, db.ForeignKey('term.id')),
        db.Column('y', db.Integer, db.ForeignKey('term.id'))
    )

class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(128), index=True)
    chinese = db.Column(db.String(128), index=True)
    similars = db.relationship('Term', secondary=similars,
            primaryjoin=(id==similars.c.x),
            secondaryjoin=(id==similars.c.y),
            backref=db.backref('term',lazy='dynamic'))
    hit_counts = db.Column(db.Integer)


