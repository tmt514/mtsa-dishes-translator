import urllib.parse
from random import randint

from app.models import db, Joke
from app.bot.constants import *
from app.bot.reply_generator import ReplyGenerator
from app.bot.rule import Rule, transition

STATE_NEW = 'new'
STATE_COLD_JOKE = 'STATE_COLD_JOKE'

class ColdJokeIntentionRule(Rule):

    @transition(STATE_NEW, {'NLP_decision': STATE_COLD_JOKE}, STATE_NEW)
    def rule_cold_joke(self, bot, user, msg, **template_params):
        cnt = Joke.query.filter_by().count()
        q = Joke.query.get(randint(1,cnt))
        content = q.content
        self.bot_send_message(user.id, {"text": content})
        return True

