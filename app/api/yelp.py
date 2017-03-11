from app.secrets import YELP_APP_ID, YELP_APP_SECRET
import requests
import json
from datetime import datetime, timedelta
from app.models import db, Location, Photo
        
# default position at Hill Auditorium
HILL_LATITUDE = 42.279150
HILL_LONGITUDE = -83.739059 

class Yelp:
    def __init__(self):
        self.update_access_token()

    def update_access_token(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": YELP_APP_ID,
            "client_secret": YELP_APP_SECRET
        }
        r = requests.post('https://api.yelp.com/oauth2/token', data=data)
        r = json.loads(r.text)
        expired_date = datetime.now() + timedelta(seconds=r['expires_in'])

        self.access_token = r['access_token']
        self.expire = expired_date

    def get_business(self, yelp_id):
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "authorization": "Bearer " + self.access_token
        }
        r = None
        try:
            r = requests.get("https://api.yelp.com/v3/businesses/%s" % yelp_id, headers=headers)
            r = json.loads(r.text)
        except Exception as e:
            print("[Yelp API Error] " + e)
            raise e



        location = Location.query.filter_by(yelp_id=yelp_id).first()
        if location == None:
            name = r.get('name', None)
            phone = r.get('phone', None)
            address = " ".join(r['location'].get('display_address', []))
            open_hours = json.dumps(r.get('hours', {}))
            yelp_url = r.get('url', None)
            location = Location(name=name, phone=phone, address=address, open_hours=open_hours, yelp_url=yelp_url, yelp_id=yelp_id)
            db.session.add(location)

        photos = r['photos']
        for url in photos:
            print("Adding photo [%s] for {%s}" % (url, name))
            photo = Photo(url=url, location=location)
            db.session.add(photo)
        db.session.commit()

    def search_business(self, text, latitude=HILL_LATITUDE, longitude=HILL_LONGITUDE):
        if datetime.now() >= self.expire:
            self.update_access_token()

        params = {
            "term": text,
            "latitude": "%.6f" % latitude,
            "longitude": "%.6f" % longitude,
        }
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "authorization": "Bearer " + self.access_token
        }

        r = None
        try:
            r = requests.get('https://api.yelp.com/v3/businesses/search', params=params, headers=headers)
            r = json.loads(r.text)
        except Exception as e:
            print("[Yelp API Error] " + e)
            raise e

        print("[Yelp] Search for {%s}: %d results found." % (text, r['total']))
        # add business to database

        for x in r['businesses']:
            yelp_id = x['id']
            print("[Yelp] Handling yelp_id={%s}" % yelp_id)
            location = Location.query.filter_by(yelp_id=yelp_id).first()
            if location == None:
                self.get_business(yelp_id)
        return r


yelp = Yelp()

