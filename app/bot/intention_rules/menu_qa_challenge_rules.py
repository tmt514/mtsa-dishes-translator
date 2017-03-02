from app.bot.rule import Rule, ForceChangeStateException, transition

STATE_NEW = 'new'
STATE_QA_CHALLENGE = 'STATE_QA_CHALLENGE'

class MenuQAChallengeRules(Rule):

    @transition(STATE_NEW, {'postback':{'payload':STATE_QA_CHALLENGE}}, STATE_NEW)
    def rule_start_qa_challenge(self, bot, user, msg, **template_params):
        bot.bot_send_message(user.id, {"text": "目前還在施工中，吃個 \U0001F354 休息一下吧～"})
        return True
