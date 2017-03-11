
from app.models import db, Term, Description
from app.bot.rule import Rule, ForceChangeStateException, transition
from app.bot.reply_generator import ListTemplate, ButtonTemplate, GenericTemplate

STATE_NEW = 'new'
STATE_POKEMON_SEARCH = 'STATE_POKEMON_SEARCH'
STATE_POKEMON_SEARCH_OK = 'STATE_POKEMON_SEARCH_OK'
STATE_HANDLE_MORE = 'STATE_HANDLE_MORE'
PAYLOAD_POKEMON_DESCRIPTION = 'PAYLOAD_POKEMON_DESCRIPTION'
PAYLOAD_POKEMON_SEARCH = 'PAYLOAD_POKEMON_SEARCH'
PAYLOAD_RELATED_POKEMON = 'PAYLOAD_RELATED_POKEMON'
PAYLOAD_MORE = 'PAYLOAD_MORE'
PAYLOAD_CANCEL = 'PAYLOAD_CANCEL'
PAYLOAD_CONTINUE_POKEMON = 'PAYLOAD_CONTINUE_POKEMON'
PAYLOAD_POKEMON_INFO = 'PAYLOAD_POKEMON_INFO'



import pickle
import jieba
import jieba.posseg as pseg
jieba.set_dictionary('app/data/dict.txt.big')

from app.data import POKEMON_REVERSE_INDEX, POKEMON_NAMES_MAPPING

from collections import defaultdict



def compute_docscore(sentence):
    docscore = defaultdict(float)
    for pair in sentence:
        word = pair.word
        doclist = POKEMON_REVERSE_INDEX.get(word) or []
        for doc, score in doclist:
            docscore[doc] += score

    docs = [(v, k) for k, v in docscore.items()]
    docs.sort(reverse=True)
    return docs



class PokemonRules(Rule):

    @transition(STATE_NEW, {'quick_reply': {'payload': PAYLOAD_POKEMON_INFO}}, STATE_NEW)
    def rule_pokemon_info(self, bot, user, msg, **template_params):
        target = msg['quick_reply'].get('target')
        if not target:
            return True
        term = Term.query.filter_by(english=target).first()
        reply = GenericTemplate(image_aspect_ratio="square")
        photo = term.photos.first()
        buttons = ButtonTemplate()
        buttons.add_postback_button(title="%s的習性" % term.chinese, payload="%s:%d,%s" % (PAYLOAD_POKEMON_DESCRIPTION, term.id, '習性'))
        kwargs = {
            "title": term.chinese,
            "subtitle": term.english,
            "buttons": buttons.button_list,
            "default_action": {
                "type": "web_url",
                "url": "https://wiki.52poke.com/zh-hant/%s" % term.chinese,
            }
        }
        if photo is not None:
            kwargs['image_url'] = photo.url
        reply.add_element(**kwargs)
        reply = reply.generate()
        reply['quick_replies'] = [
            bot.reply_gen.QUICK_REPLY_CANCEL
        ]
        bot.bot_send_message(user.id, reply)
        return True

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
    
    @transition(STATE_POKEMON_SEARCH, {'text':''}, STATE_POKEMON_SEARCH_OK)
    def rule_pokemon_search(self, bot, user, msg, **template_params):
        sentence = pseg.cut(msg['text'])
        docs = compute_docscore(sentence)

        if len(docs) == 0:
            bot.bot_send_message(user.id, {"text": "對不起，查無資料 QQ"})
            raise ForceChangeStateException(state=STATE_NEW, halt=True)

        term = Term.query.filter_by(english=POKEMON_NAMES_MAPPING[docs[0][1]]).first()
        user.set_q(msg['text'])
        user.set_english(term.english)
        user.set_chinese(term.chinese)
        reply = {"text": "%s (%s)" % (term.chinese, term.english)}
        reply['quick_replies'] = [
                bot.reply_gen.make_quick_reply(title="類似寶可夢",
                    payload=PAYLOAD_RELATED_POKEMON,
                    image_url="http://emojis.slackmojis.com/emojis/images/1450464069/186/pokeball.png?1450464069"),
            bot.reply_gen.make_quick_reply(title="輸入新的查詢", payload=PAYLOAD_CONTINUE_POKEMON),
            bot.reply_gen.QUICK_REPLY_MORE,
            bot.reply_gen.QUICK_REPLY_CANCEL
        ]
        bot.bot_send_message(user.id, reply)
        return True

    @transition(STATE_POKEMON_SEARCH_OK, {'quick_reply':{'payload': PAYLOAD_CONTINUE_POKEMON}}, STATE_POKEMON_SEARCH)
    def rule_pokemon_search_continue(self, bot, user, msg, **template_params):
        bot.bot_send_message(user.id, {"text": "請輸入關鍵字查詢寶可夢～"})
        return True

    @transition(STATE_POKEMON_SEARCH_OK, {'quick_reply':{'payload': PAYLOAD_CANCEL}}, STATE_NEW)
    def rule_pokemon_cancel(self, bot, user, msg, **template_params):
        return True

    @transition(STATE_POKEMON_SEARCH_OK, {'quick_reply':{'payload': PAYLOAD_MORE}}, STATE_HANDLE_MORE)
    def rule_pokemon_more(self, bot, user, msg, **template_params):
        user.set_q(user.get_chinese())
        return False

    @transition(STATE_POKEMON_SEARCH_OK, {'quick_reply':{'payload': PAYLOAD_RELATED_POKEMON}}, STATE_POKEMON_SEARCH_OK)
    def rule_pokemon_results(self, bot, user, msg, **template_params):
        sentence = pseg.cut(user.get_q())
        docs = compute_docscore(sentence)

        reply = GenericTemplate()
        for i in range(0, min(5, len(docs))):
            term = Term.query.filter_by(english=POKEMON_NAMES_MAPPING[docs[i][1]]).first()
            photo = term.photos.first()
            buttons = ButtonTemplate()
            buttons.add_postback_button(title="%s的習性" % term.chinese, payload="%s:%d,%s" % (PAYLOAD_POKEMON_DESCRIPTION, term.id, '習性'))
            kwargs = {
                "title": term.chinese,
                "subtitle": term.english,
                "buttons": buttons.button_list,
            }
            if photo is not None:
                kwargs['image_url'] = photo.url
            reply.add_element(**kwargs)

        reply = reply.generate()
        reply['quick_replies'] = [
            bot.reply_gen.make_quick_reply(title="輸入新的查詢", payload=PAYLOAD_CONTINUE_POKEMON),
            bot.reply_gen.QUICK_REPLY_CANCEL
        ]
        bot.bot_send_message(user.id, reply)
        return True

