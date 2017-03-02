
from app.models import db, Term, Description
from app.bot.rule import Rule, ForceChangeStateException, transition

STATE_NEW = 'new'
STATE_POKEMON_SEARCH = 'STATE_POKEMON_SEARCH'
PAYLOAD_POKEMON_DESCRIPTION = 'PAYLOAD_POKEMON_DESCRIPTION'
PAYLOAD_POKEMON_SEARCH = 'PAYLOAD_POKEMON_SEARCH'


import pickle
import jieba
import jieba.posseg as pseg
jieba.set_dictionary('app/data/dict.txt.big')

from app.data import POKEMON_REVERSE_INDEX, POKEMON_NAMES_MAPPING

from collections import defaultdict

class PokemonRules(Rule):

    @transition(STATE_NEW, {'postback': {'payload': PAYLOAD_POKEMON_DESCRIPTION}}, STATE_NEW)
    def rule_pokemon_description(self, bot, user, msg, **template_params):
        target = msg['postback'].get('target')
        if not target:
            return True
        term, subheading = target.split(",")
        term = Term.query.get(int(term))
        description = term.descriptions.filter_by(subheading=subheading).first()
        if not description:
            bot.bot_send_message(user.id, {"text": "很抱歉查無資料噢 >___<"})
            return True

        bot.bot_send_message(user.id, {"text": description.content})
        return True


    @transition(STATE_NEW, {'postback': {'payload': PAYLOAD_POKEMON_SEARCH}}, STATE_POKEMON_SEARCH)
    def rule_start_pokemon_search(self, bot, user, msg, **template_params):
        bot.bot_send_message(user.id, {"text": "請輸入關鍵字查詢寶可夢～"})
        return True

    @transition(STATE_NEW, {'NLP_decision': STATE_POKEMON_SEARCH}, STATE_POKEMON_SEARCH)
    def rule_start_pokemon_search2(self, bot, user, msg, **template_params):
        bot.bot_send_message(user.id, {"text": "請輸入關鍵字查詢寶可夢～"})
        return True
    
    @transition(STATE_POKEMON_SEARCH, {'text':''}, STATE_NEW)
    def rule_pokemon_search(self, bot, user, msg, **template_params):
        sentence = pseg.cut(msg['text'])
        docscore = defaultdict(float)
        for pair in sentence:
            word = pair.word
            doclist = POKEMON_REVERSE_INDEX.get(word) or []
            for doc, score in doclist:
                docscore[doc] += score

        docs = [(v, k) for k, v in docscore.items()]
        docs.sort(reverse=True)
        if len(docs) == 0:
            bot.bot_send_message(user.id, {"text": "對不起，查無資料 QQ"})
            return True

        term = Term.query.filter_by(english=POKEMON_NAMES_MAPPING[docs[0][1]]).first()
        bot.bot_send_message(user.id, {"text": "%s (%s)" % (term.chinese, term.english)})
        return True
