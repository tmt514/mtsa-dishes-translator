import json
import urllib.request
import urllib.parse
from app.models import db, Term 
from html.parser import HTMLParser
from google import search, get_page
from bs4 import BeautifulSoup
from datetime import datetime
from app.secrets import PAGE_TOKEN
from app.bot.constants import *
from app.bot.reply_generator import ReplyGenerator

class IntentionBot:
    def __init__(self):
        self.reply_gen = ReplyGenerator()

    def handle_message(self, msg, sender, state, msgbody):
        raise Exception("Not Implemented!")

    def bot_sendAPI(self, data):
        token = PAGE_TOKEN
        url = "https://graph.facebook.com/v2.8/me/messages?access_token=" + token
        try:
            req = urllib.request.Request(url, data, {'Content-Type': 'application/json'})
            f = urllib.request.urlopen(req)
            response = f.read()
            print(response)
            f.close()
        except Exception as e:
            print(e)

    def bot_sender_action(self, recipient_id, action):
        data = json.dumps({
            "recipient": {
                "id": str(recipient_id)
            },
            "sender_action": action
            }).encode('utf8')
        self.bot_sendAPI(data)

    def bot_send_message(self, recipient_id, msg):
        data = json.dumps({
            "recipient": {
                "id": str(recipient_id)
            },
            "message": msg
            }).encode('utf8')
        self.bot_sendAPI(data)




