# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, session, url_for
from celery import Celery
from app.app_celery import make_celery
from app.secrets import APP_CONFIG_SECRET_KEY, APP_CONFIG_CELERY_BROKER_URL, \
        APP_CONFIG_CELERY_RESULT_BACKEND, APP_CONFIG_REDIS_URL
import json
import urllib.request
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = APP_CONFIG_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aafood.db'

app.config['CELERY_BROKER_URL']= APP_CONFIG_CELERY_BROKER_URL
app.config['CELERY_RESULT_BACKEND'] = APP_CONFIG_CELERY_RESULT_BACKEND

celery = make_celery(app)

from flask_redis import FlaskRedis
app.config['REDIS_URL'] = APP_CONFIG_REDIS_URL 
redis_store = FlaskRedis(app)



@app.route('/')
def index():
    return "OK"


@app.route("/callback", methods=['GET'])
def hello():
    """ webhook 一開始的認證使用 """
    challenge = request.args.get('hub.challenge', '')
    secret = request.args.get('hub.verify_token', '')
    print(challenge)
    print(secret)
    return challenge


from app.bot import Bot
bot = Bot(app)

@celery.task
def celery_handle_message(msg, sender, msgbody):
    """ 背景作業：處理每一個傳進來的訊息 """
    with app.app_context():
        try:
            # 先已讀
            bot.intention_bot.bot_sender_action(sender, "mark_seen")

            # 然後處理
            bot.handle_message(msg, sender, msgbody)
        except Exception as e:
            print(e)

            # 後台炸裂, 跟使用者說抱歉
            bot.intention_bot.bot_send_message(sender, {"text": "講尛？"})

@celery.task
def celery_handle_postback(msg, sender, payload):
    with app.app_context():
        try:
            # 先已讀
            bot.intention_bot.bot_sender_action(sender, "mark_seen")
            print ("bot_sender_action")
            # 然後處理
            bot.handle_postback(msg, sender, payload)
        except Exception as e:
            print(e)

            # 後台炸裂, 跟使用者說抱歉
            bot.intention_bot.bot_send_message(sender, {"text": "傳尛？"})
            

@app.route("/callback", methods=['POST'])
def messenge_updates():
    """ 實際 webhook 會呼叫的地方，理論上必須儘快回覆 HTTP 200 """
    data = request.data
    data = json.loads(str(data, 'utf-8'))
    entries = data['entry']
    for entry in entries:
        if 'messaging' in entry:
            messages = entry['messaging']
            for msg in messages:
                if 'message' in msg and 'is_echo' in msg['message']:
                    continue
                if 'sender' in msg and 'message' in msg:
                    sender = msg['sender']['id']
                    msgbody = msg['message']
                    # 這邊使用 Async Task:
                    #   先送到 Redis 去存起來, 然後交給 celery 完成任務
                    celery_handle_message.delay(msg, sender, msgbody)
                if 'sender' in msg and 'postback' in msg and 'payload' in msg['postback']:
                    sender = msg['sender']['id']
                    payload = msg['postback']['payload']
                    # 知道更多：圖片、食譜、哪裡買得到
                    celery_handle_postback.delay(msg, sender, payload)

    return "OK"
   
from .website import website
app.register_blueprint(website)

if __name__ == '__main__':
    main()

