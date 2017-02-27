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

from app.bot.rule import Rule, transition, ForceChangeStateException


STATE_NEW = 'new'
STATE_CHINESE_TO_ENGLISH = 'STATE_CHINESE_TO_ENGLISH'
STATE_CHINESE_TO_ENGLISH_OK = 'STATE_CHINESE_TO_ENGLISH_OK'
STATE_WAIT_FOR_FIX_ENGLISH = 'STATE_WAIT_FOR_FIX_ENGLISH'

PAYLOAD_CONFIRM = 'PAYLOAD_CONFIRM'
PAYLOAD_FIX = 'PAYLOAD_FIX'
PAYLOAD_CANCEL = 'PAYLOAD_CANCEL'
PAYLOAD_MORE = 'PAYLOAD_MORE'

import enchant
import mafan

def wiki_zh_to_en(self, s):
    """ 利用維基百科的頁面跳轉功能找到英文 """
    #""" 利用 google translate 中翻英 """
    #url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-TW&tl=en&dt=t&q=%s" %\
    #    (urllib.parse.quote(s))
    #response = urllib.request.urlopen(url)
    #html = response.read()
    #print(html)
    url = "https://zh.wikipedia.org/wiki/%s" % (urllib.parse.quote(s))
    try:
        page = get_page(url)
            
        soup = BeautifulSoup(page, 'lxml')
        en_link = soup.findAll('li', class_='interwiki-en')
        if len(en_link) == 0:
            return None
        p = en_link[0].a
        if p is None:
            return None
        en = p.get('href', None)
        if en is None:
            return None
        tr = en.split('/')[-1].lower().replace("_", " ")
        print("找到翻譯了... [%s] => %s" % (s, tr))
        return tr
    except Exception as e:
        print("Error: %s" % str(e))
        return None

def zh_to_en(self, s):
    s = mafan.to_traditional(s.strip())
    q = Term.query.filter_by(chinese=s).order_by(Term.hit_counts.desc()).first()

    if q is None:
        tr = self.wiki_zh_to_en(s)
        return tr
    print("search DB: %s <=> %s [%d]" % (q.english, q.chinese, q.hit_counts or 0))
    return q.english

class ChineseToEnglishIntentionRule(Rule):
    
    @transition(STATE_NEW, {'NLP_decision': STATE_CHINESE_TO_ENGLISH}, STATE_CHINESE_TO_ENGLISH_OK)
    def rule_translate_from_chinese_to_english(self, bot, user, msg, **template_params):
        target = template_params.get('target', msg.get('text', None))
        
        user.set_q(target)

        tr = zh_to_en(target)
        if tr is None:
            bot.bot_send_message(user.id, { "text": "翻譯失敗" })
            raise ForceChangeStateException(STATE_NEW, halt=True) # 強制取消

        bot.set_english(tr)
        bot.set_chinese(msgtext.strip())
        bot.bot_send_message(user.id, bot.reply_gen.translated_string(tr))
        
        q = Term.query.filter_by(chinese=msgtext.strip(), english=tr).first()
        if q is not None and q.photos.first() is not None:
            bot.bot_send_message(user.id, bot.reply_gen.image(q.photos.first().url))
        return True


    @transition(STATE_CHINESE_TO_ENGLISH_OK, {'quick_reply': {'payload': PAYLOAD_CANCEL}}, STATE_NEW)
    def rule_quick_cancel(self, bot, user, msg, **template_params):
        return True

    @transition(STATE_CHINESE_TO_ENGLISH_OK, {'quick_reply': {'payload': PAYLOAD_FIX}}, STATE_WAIT_FOR_FIX_ENGLISH)
    def rule_quick_fix(self, bot, user, msg, **template_params):
        # 把近似的翻譯丟出去
        bot.bot_send_message(user.id, { "text": "請輸入「%s」對應的正確英文～" % user.get_q() })
        return True

    @transition(STATE_CHINESE_TO_ENGLISH_OK, {'quick_reply': {'payload': PAYLOAD_CONFIRM}}, STATE_NEW)
    def rule_quick_confirm(self, bot, user, msg, **template_params):
        q = Term.query.filter_by(english=user.get_english(), chinese=user.get_chinese()).first()
        if q is None:
            q = Term(english=user.get_english(), chinese=user.get_chinese(), hit_counts=1)
            db.session.add(q)
        else:
            q.hit_counts = (q.hit_counts+1 if q.hit_counts else 1)
        print("update DB: %s <=> %s [%d]" % (q.english, q.chinese, q.hit_counts or 0))
        db.session.commit()
        bot.bot_send_message(user.id, bot.reply_gen.sticker('thank you'))
        return True
    

    @transition(STATE_WAIT_FOR_FIX_ENGLISH, {'text':''}, STATE_CHINESE_TO_ENGLISH_OK)
    def rule_handle_fix(self, bot, user, msg, **template_params):
        target = msg['text'].strip()
        user.set_english(target.lower())
        bot.bot_send_message(user.id, bot.reply_gen.translated_string("\"" + target + "\" 這樣對嗎？"))
        return True


        
    @transition(STATE_CHINESE_TO_ENGLISH_OK, {'quick_reply': {'payload': PAYLOAD_MORE}}, STATE_NEW)
    def rule_quick_more(self, bot, user, msg, **template_params):
        bot.bot_send_message(user.id, bot.reply_gen.ask_more(user))
        return True
