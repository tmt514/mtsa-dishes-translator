from flask import Blueprint, make_response
from app.models import db, Term
import json

website = Blueprint('website', __name__, template_folder='templates')

@website.route("/alldict")
def list_all_dictionary():
    u = list(map(lambda x: str(x.as_dict()), Term.query.all()))
    u = "<br>".join(u)
    return u
