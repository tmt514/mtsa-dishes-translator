from app.bot.rule import Rule, ForceChangeStateException, transition
from app.models import Category 
import random

STATE_NEW = 'new'
STATE_QA_CHALLENGE = 'STATE_QA_CHALLENGE'
STATE_DESCRIBE_CHALLENGE = 'STATE_DESCRIBE_CHALLENGE'
STATE_DESC_WAIT_RESP = 'STATE_DESCRIBE_WAIT_RESPONSE'
STATE_CHALLENGES = [STATE_DESCRIBE_CHALLENGE]
PAYLOAD_QA_NEXT_CHALLENGE = 'PAYLOAD_QA_NEXT_CHALLENGE'
PAYLOAD_CANCEL = 'PAYLOAD_CANCEL'


import logging
import json

def setup_log():
    logger = logging.getLogger('pokemon')
    filelog = logging.FileHandler('log/pokemon_qa_challenges.log')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(filelog)
    return (filelog, logger)

my_filelog, my_logger = setup_log()


def pick_qa_challenge(bot, user, msg, **template_params):
    challenge_state = state=random.choice(STATE_CHALLENGES)
    bot.bot_send_message(user.id, {"text": "華麗！酷炫！神奇寶貝描述大挑戰！！"}) 
    if challenge_state == STATE_DESCRIBE_CHALLENGE: 
        raise ForceChangeStateException(state=challenge_state, halt=False)

class MenuQAChallengeRules(Rule):

    
    @transition(STATE_NEW, {'postback':{'payload':STATE_QA_CHALLENGE}}, STATE_QA_CHALLENGE)
    def rule_start_qa_challenge(self, bot, user, msg, **template_params):
        #bot.bot_send_message(user.id, {"text": "目前還在施工中，吃個 \U0001F354 休息一下吧～"})
        pick_qa_challenge(bot, user, msg, **template_params)
        return True
    
    @transition(STATE_QA_CHALLENGE, {'text': ''}, STATE_QA_CHALLENGE)
    def continue_qa_challenge(self, bot, user, msg, **template_params):
        #TODO: 可能要改rule.py
        msg['postback'] = {}
        msg['postback']['payload'] = STATE_QA_CHALLENGE
        pick_qa_challenge(bot, user, msg, **template_params)
        return True

    @transition(STATE_DESCRIBE_CHALLENGE, {'postback':{'payload': STATE_QA_CHALLENGE}}, STATE_DESC_WAIT_RESP)
    def rule_describe_challenge(self, bot, user, msg, **template_params): 
        c = Category.query.filter_by(name='pokemon').first()
        pokemon_list = c.terms
        
        photo = None
        target_pokemon = None
        while photo is None:
            target_pokemon = random.choice(pokemon_list)
            photo = target_pokemon.photos.first()

        user.set_q(target_pokemon.english)

        bot.bot_send_message(user.id, {"text": "請有創意地描述這個神奇寶貝！"})
        bot.bot_send_message(user.id, bot.reply_gen.image(photo.url,
            quick_replies=[
                bot.reply_gen.make_quick_reply(title='跳過此題', payload=PAYLOAD_QA_NEXT_CHALLENGE),
                bot.reply_gen.QUICK_REPLY_CANCEL
                ]))
        return True

    @transition(STATE_NEW, {'quick_reply':{'payload': PAYLOAD_QA_NEXT_CHALLENGE}}, STATE_QA_CHALLENGE)
    def rule_next_challenge_new(self, bot, user, msg, **template_params):
        return False

    @transition(STATE_DESC_WAIT_RESP, {'quick_reply':{'payload': PAYLOAD_QA_NEXT_CHALLENGE}}, STATE_DESCRIBE_CHALLENGE)
    def rule_next_challenge(self, bot, user, msg, **template_params):
        return False

    @transition(STATE_DESC_WAIT_RESP, {'quick_reply':{'payload': PAYLOAD_CANCEL}}, STATE_NEW)
    def rule_cancel(self, bot, user, msg, **template_params):
        return True

    @transition(STATE_DESC_WAIT_RESP, {'text': ''}, STATE_NEW)
    def rule_process_describe_response(self, bot, user, msg, **template_params):
        #TODO: parse msg.text, store Noun, Adj tag
        #TODO: show most frequence tags (ex/ 紅色的神秘的直升機蘿蔔)

        my_logger.info(json.dumps([user.id, user.get_q(), msg['text']], ensure_ascii=False))
        my_filelog.flush()
        term = Term.query.filter_by(english=user.get_q()).first()

        reply = {"text": "你好棒棒！這隻叫做 %s（%s）～" % (term.chinese, term.english)}
        reply['quick_replies'] = [
            bot.reply_gen.make_quick_reply(title='下一題！', payload=PAYLOAD_QA_NEXT_CHALLENGE),
            bot.reply_gen.QUICK_REPLY_CANCEL
        ]
        bot.bot_send_message(user.id, reply)
        return True
