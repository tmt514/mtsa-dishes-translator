import urllib.parse
from random import randint

from app.models import db, Joke
from app.secrets import PAGE_TOKEN
from app.bot.constants import *
from app.bot.reply_generator import ReplyGenerator
from app.bot.intention_bot import IntentionBot

class ColdJokeIntentionBot(IntentionBot):
    def __init__(self, params):
        super().__init__()
        self.params = params

    def handle_message(self, msg, sender, state, msgbody):
        cnt = Joke.query.filter_by().count()
        q = Joke.query.get(randint(1,cnt))
        content = q.content
        self.bot_send_message(sender,{"text": content})

