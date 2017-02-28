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
STATE_ENGLISH_TO_CHINESE = 'STATE_ENGLISH_TO_CHINESE'
STATE_ENGLISH_TO_CHINESE_OK = 'STATE_ENGLISH_TO_CHINESE_OK'
STATE_WAIT_FOR_FIX_CHINESE = 'STATE_WAIT_FOR_FIX_CHINESE'
STATE_HANDLE_MORE = 'STATE_HANDLE_MORE'

PAYLOAD_CONFIRM = 'PAYLOAD_CONFIRM'
PAYLOAD_FIX = 'PAYLOAD_FIX'
PAYLOAD_CANCEL = 'PAYLOAD_CANCEL'
PAYLOAD_MORE = 'PAYLOAD_MORE'

import enchant
import mafan

def ask_google_en_to_zh(s):
    q = s + " wikipedia 中文"
    result = search(q, lang="zh", pause=1.0)
    cnt = 0
    for x in result:
        cnt += 1
        if cnt >= 10:
            break
        if 'wikipedia' in x:
            x = urllib.parse.unquote(x)
            x = x.split('/')[-1]
            if mafan.text.is_traditional(x):
                return x
            if mafan.text.is_simplified(x):
                url = "http://zh.wikipedia.org/zh-tw/" + urllib.parse.quote_plus(x)
                print(url)
                try:
                    w = get_page(url)
                except:
                    continue
                soup = BeautifulSoup(w, 'lxml')
                x = soup.title.string
                x = x.strip().split(' ')[0]
                if '維基百科' not in x:
                    return x
    return None


def en_to_zh(s):
    print("s=%s" %  s)
    s = s.lower().strip()
    q = Term.query.filter_by(english=s).order_by(Term.hit_counts.desc()).first()

    if q is None:
        translated = ask_google_en_to_zh(s)
        return translated
    print("search DB: %s <=> %s [%d]" % (q.english, q.chinese, q.hit_counts or 0))
    return q.chinese

class EnglishToChineseIntentionRules(Rule):

    @transition(STATE_NEW, {'NLP_decision': STATE_ENGLISH_TO_CHINESE}, STATE_ENGLISH_TO_CHINESE_OK)
    def rule_translate_from_english_to_chinese(self, bot, user, msg, **template_params):
        target = template_params.get('target', None) or msg.get('text', None)
        print(target)
        
        user.set_q(target)

        # 找出翻譯內容
        tr = en_to_zh(target)
        if tr is None:
            bot.bot_send_message(user.id, { "text": "搜尋近似詞中，請耐心等候..." })
            bot.bot_sender_action(user.id, "typing_on")
            d = enchant.Dict("en_US")
            suggested = d.suggest(target.strip().lower())
            for term in suggested:
                tr = self.en_to_zh(term)
                if tr is not None:
                    target = term
                    bot.bot_send_message(user.id, { "text": "改成搜尋 \"%s\"" % term })
                    break
        if tr is None:
            tr = "翻譯失敗"
            raise ForceChangeStateException(state=STATE_NEW, halt=True)
        
        user.set_english(target.strip().lower())
        user.set_chinese(tr)
        bot.bot_send_message(user.id, bot.reply_gen.translated_string(tr))
        
        q = Term.query.filter_by(english=target.strip().lower(), chinese=tr).first()

        # 如果是神奇寶貝 才要放圖片?
        if q is not None and q.photos.first() is not None:
            bot.bot_send_message(user.id, bot.reply_gen.image(q.photos.first().url))
        return True

    @transition(STATE_ENGLISH_TO_CHINESE_OK, {'quick_reply': {'payload': PAYLOAD_CANCEL}}, STATE_NEW)
    def rule_quick_cancel(self, bot, user, msg, **template_params):
        return True

    @transition(STATE_ENGLISH_TO_CHINESE_OK, {'quick_reply': {'payload': PAYLOAD_FIX}}, STATE_WAIT_FOR_FIX_CHINESE)
    def rule_quick_fix(self, bot, user, msg, **template_params):
        # TODO: Get Similars as quick replies
        user.set_english(user.get_q().strip().lower())
        bot.bot_send_message(user.id, { "text": "請輸入 \"%s\" 對應的正確中文～" % user.get_q() })
        return True


    @transition(STATE_ENGLISH_TO_CHINESE_OK, {'quick_reply': {'payload': PAYLOAD_CONFIRM}}, STATE_NEW)
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

    @transition(STATE_WAIT_FOR_FIX_CHINESE, {'text': ''}, STATE_ENGLISH_TO_CHINESE_OK)
    def rule_handle_fix(self, bot, user, msg, **template_params):
        target = msg['text'].strip()
        user.set_chinese(target)
        bot.bot_send_message(user.id, bot.reply_gen.translated_string("「" + target + "」這樣對嗎？"))
        return True

    @transition(STATE_ENGLISH_TO_CHINESE_OK, {'quick_reply': {'payload': PAYLOAD_MORE}}, STATE_HANDLE_MORE)
    def rule_quick_more(self, bot, user, msg, **template_params):
        # bot.bot_send_message(user.id, bot.reply_gen.ask_more(user))
        # Do not halt
        return False



