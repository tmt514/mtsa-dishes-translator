import urllib.parse
from app.models import db, Term 
from html.parser import HTMLParser
from google import search, get_page
from bs4 import BeautifulSoup
from datetime import datetime
from app.secrets import PAGE_TOKEN
from app.bot.constants import *
from app.bot.reply_generator import ReplyGenerator
from app.bot.intention_bot import IntentionBot

class ColdJokeIntentionBot(IntentionBot):
    def __init__(self, params):
        super().__init__()
        self.params = params

    def handle_message(self, msg, sender, state, msgbody):
        self.bot_send_message(sender, {"text": "說笑話"})

