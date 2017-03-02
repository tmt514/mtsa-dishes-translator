
import json
import urllib.request
from app.secrets import PAGE_TOKEN

def clear_thread_settings():
    pass

def update_thread_settings():
    """ 這個會呼叫 facebook 更新對話視窗底下的 Menu
        詳情請參考 persistent menu:
        https://developers.facebook.com/docs/messenger-platform/thread-settings/persistent-menu
    """
    data = json.dumps({
        "setting_type" : "call_to_actions",
        "thread_state" : "existing_thread",
        "call_to_actions":[
            {
                "type":"postback",
                "title":"答題大挑戰",
                "payload":"STATE_QA_CHALLENGE"
            },
            {
                "type":"postback",
                "title":"安城美食推薦",
                "payload":"STATE_RANDOM_DISH"
            },
            {
                "type":"postback",
                "title":"查詢寶可夢",
                "payload":"STATE_POKEMON_SEARCH"
            }
        ]
    }).encode('utf8')
        
    token = PAGE_TOKEN
    url = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=" + token
    try:
        req = urllib.request.Request(url, data, {'Content-Type': 'application/json'}, method='POST')
        f = urllib.request.urlopen(req)
        response = f.read()
        print(response)
        f.close()
    except Exception as e:
        print(e)
