from app.app import celery_handle_message, celery_handle_postback
from app.bot.bot import Bot
from app.bot.intention_bot import IntentionBot

from app.bot.intention_detector import IntentionDetector
from app.bot.state_machine import StateMachine
from app.bot.user_status import UserStatus

from app.tests.test_app import AAFoodTestCase
import json
import mock




class BotCallTest(AAFoodTestCase):

    @mock.patch.object(IntentionBot, 'bot_sender_action')
    @mock.patch.object(IntentionBot, 'bot_send_message')
    def test_pikachu_description(self, mock_bot_send_message, mock_bot_sender_action):
        msg = {"postback":{"payload":"PAYLOAD_POKEMON_DESCRIPTION:25,習性"}}
        sender = "fake_user"
        msgbody = msg['postback']['payload']

        # 真正跑測試的地方~
        celery_handle_postback(msg, sender, msgbody)
        print("\033[0;32m%s\033[m" % json.dumps(mock_bot_send_message.call_args_list, indent=4, sort_keys=True, ensure_ascii=False))

    @mock.patch.object(IntentionBot, 'bot_sender_action')
    @mock.patch.object(IntentionBot, 'bot_send_message')
    def test_pikachu_more(self, mock_bot_send_message, mock_bot_sender_action):
        msg = {"message": {"text": "pikachu"}}
        sender = "fake_user"
        msgbody = msg['message']

        # 真正跑測試的地方~
        celery_handle_message(msg, sender, msgbody)
        user = UserStatus(sender)
        assert user.get_status() == 'STATE_ENGLISH_TO_CHINESE_OK'

        # 接下來按下 "更多"
        msg = {"message": {"quick_reply": {"payload": 'PAYLOAD_MORE'}}}
        msgbody = msg['message']
        celery_handle_message(msg, sender, msgbody)
        print("\033[0;32m%s\033[m" % json.dumps(mock_bot_send_message.call_args_list, indent=4, sort_keys=True, ensure_ascii=False))




    @mock.patch.object(IntentionBot, 'bot_sender_action')
    @mock.patch.object(IntentionBot, 'bot_send_message')
    def test_single_english_to_chinese(self, mock_bot_send_message, mock_bot_sender_action):
        msg = {"message": {"text": "avocado"}}
        sender = "fake_user"
        msgbody = msg['message']

        # 真正跑測試的地方~
        celery_handle_message(msg, sender, msgbody)

        # 檢查已讀是否送出
        assert mock_bot_sender_action.called

        print("\033[0;32m%s\033[m" % json.dumps(mock_bot_send_message.call_args_list, indent=4, sort_keys=True, ensure_ascii=False))
        user = UserStatus(sender)
        assert user.get_status() == 'STATE_ENGLISH_TO_CHINESE_OK'


    @mock.patch.object(IntentionBot, 'bot_sender_action')
    @mock.patch.object(IntentionBot, 'bot_send_message')
    def test_translate_english_to_chinese(self, mock_bot_send_message, mock_bot_sender_action):
        msg = {"message": {"text": "請問 avocado 的中文是什麼"}}
        sender = "fake_user"
        msgbody = msg['message']

        # 真正跑測試的地方~
        celery_handle_message(msg, sender, msgbody)

        # 檢查已讀是否送出
        assert mock_bot_sender_action.called

        print("\033[0;32m%s\033[m" % json.dumps(mock_bot_send_message.call_args_list, indent=4, sort_keys=True, ensure_ascii=False))
        user = UserStatus(sender)
        assert user.get_status() == 'STATE_ENGLISH_TO_CHINESE_OK'


    @mock.patch.object(IntentionBot, 'bot_sender_action')
    @mock.patch.object(IntentionBot, 'bot_send_message')
    def test_joke(self, mock_bot_send_message, mock_bot_sender_action):
        msg = {"message": {"text": "笑話"}}
        sender = "fake_user"
        msgbody = msg['message']

        # 開始跑測試囉~
        celery_handle_message(msg, sender, msgbody)

        print("\033[0;32m%s\033[m" % json.dumps(mock_bot_send_message.call_args_list, indent=4, sort_keys=True, ensure_ascii=False))
        user = UserStatus(sender)
        assert user.get_status() == 'new'
        
