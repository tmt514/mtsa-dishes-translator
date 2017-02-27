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
from app.bot.rule import Rule, ForceChangeStateException, transition

STATE_NEW = 'new'
STATE_GREETING = 'STATE_GREETING'

class GreetingIntentionRule(Rule):

    @transition(STATE_NEW, {'NLP_decision': STATE_GREETING}, STATE_NEW)
    def rule_greeting(self, bot, user, msg, **template_params):
        say = template_params.get('say')
        if say == 'hi':
            bot.bot_send_message(user.id, {"text": "您好！我是 AA食物翻譯小幫手～，直接輸入英文或中文都可以唷！"})
        elif say == 'thanks':
            bot.bot_send_message(user.id, bot.reply_gen.sticker("you are welcome"))
        else:
            bot.bot_send_message(user.id, {"text": say})
