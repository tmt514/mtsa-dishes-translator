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
from app.bot.intention_bot import IntentionBot


import enchant
import mafan
class PostPictureResponseBot(IntentionBot):
    def __init__(self, target=None):
        super().__init__()
        self.target = target

    def handle_postback(msg, sender, payload):

        state.set_status('new')
        self.bot_send_message(sender, { "text": "看圖片這個功能還沒做出來" })
        return

        
