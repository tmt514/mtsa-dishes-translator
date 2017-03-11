import json
from app.models import db, Term
from app.bot.rule import Rule, ForceChangeStateException, transition
from app.bot.reply_generator import ButtonTemplate

STATE_NEW = 'new'
STATE_HANDLE_MORE = 'STATE_HANDLE_MORE'

PAYLOAD_MORE = 'PAYLOAD_MORE'
PAYLOAD_POKEMON_DESCRIPTION = 'PAYLOAD_POKEMON_DESCRIPTION'

class MoreInfoRules(Rule):

    @transition(STATE_HANDLE_MORE, {'quick_reply': {'payload': PAYLOAD_MORE}}, STATE_NEW)
    def rule_handle_more(self, bot, user, msg, **template_params):
        e = user.get_english()
        c = user.get_chinese()
        term = Term.query.filter_by(english=e, chinese=c).first()
        if term is None:
            bot.bot_send_message(user.id, {"text": "你不能知道更多了...(沒有資料)"})
            return True


        reply = ButtonTemplate("您想要知道什麼呢？")

        categories = term.categories.all()
        for category in categories:
            if category.name == 'pokemon':
                for desc in term.descriptions.all():
                    title = "%s的%s" % (user.get_q(), desc.subheading)
                    payload = "%s:%d,%s" % (PAYLOAD_POKEMON_DESCRIPTION, term.id, desc.subheading)
                    reply.add_postback_button(title=title, payload=payload)
        
        
        if len(reply.button_list) == 0:
            bot.reply_gen.ask_more(reply, user, msg, **template_params)

        print(reply.generate())
        bot.bot_send_message(user.id, reply.generate())
        return True


