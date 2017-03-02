from app.app import celery_handle_message
from app.tests.test_app import AAFoodTestCase
from app.bot.user_status import UserStatus
from app.bot.intention_bot import IntentionBot
import mock
import json

class TestPokemonRules(AAFoodTestCase):

    @mock.patch.object(IntentionBot, 'bot_sender_action')
    @mock.patch.object(IntentionBot, 'bot_send_message')
    def test_pokemon_search(self, mock_bot_send_message, mock_bot_sender_action):
        msg = {'message':{'text':'黃色電氣老鼠'}}
        sender = "fake_user"
        msgbody = msg['message']

        user = UserStatus(sender)
        user.set_status('STATE_SEARCH_POKEMON')

        # 真正跑測試的地方~
        celery_handle_message(msg, sender, msgbody)
        print("\033[0;32m%s\033[m" % json.dumps(mock_bot_send_message.call_args_list, indent=4, sort_keys=True, ensure_ascii=False))
