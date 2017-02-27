from app.app import celery_handle_message, celery_handle_postback
from app.bot.bot import Bot
from app.bot.intention_bot import IntentionBot

from app.bot.intention_detector import IntentionDetector
from app.bot.state_machine import StateMachine

from app.tests.test_app import AAFoodTestCase
import mock


class BotCallTest(AAFoodTestCase):

    @mock.patch.object(StateMachine, 'run')
    @mock.patch.object(IntentionDetector, 'parse_msg')
    @mock.patch.object(IntentionBot, 'bot_sender_action')
    @mock.patch.object(IntentionBot, 'bot_send_message')
    def test_bot_handle_message_is_called(self, mock_bot_send_message, mock_bot_sender_action, mock_parse_msg, mock_run):
        msg = {"text": "請問 avocado 的中文是什麼"}
        sender = "fake"
        msgbody = msg['text']

        celery_handle_message(msg, sender, msgbody)

        # 檢查已讀是否送出
        assert mock_bot_sender_action.called

        print(mock_parse_msg.call_args)
        print(mock_run.call_args)

        
