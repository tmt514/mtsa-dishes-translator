
from app.models import db, Term, Description
from app.bot.rule import Rule, ForceChangeStateException, transition

STATE_NEW = 'new'
PAYLOAD_POKEMON_DESCRIPTION = 'PAYLOAD_POKEMON_DESCRIPTION'

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
