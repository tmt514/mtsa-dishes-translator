from app.app import redis_store
import pickle
from datetime import datetime
class UserStatus:
    def __init__(self, sender):
        self.__key = "state::user%s" % sender
        self.__state = pickle.loads(
            redis_store.get(self.__key) or
            pickle.dumps({
                'status':'new',
                'query_english':'',
                'query_chinese':'',
                'q':'',
                'bot':'',
                'last_active':datetime.now()
                })
            )

    def get_status(self):
        return self.__state.get('status', 'new')

    def set_status(self, status):
        self.__state['status'] = status
        redis_store.set(self.__key, pickle.dumps(self.__state))

    def get_english(self):
        return self.__state.get('query_english', '')

    def set_english(self, value):
        self.__state['query_english'] = value
        redis_store.set(self.__key, pickle.dumps(self.__state))

    def get_chinese(self):
        return self.__state.get('query_chinese', '')

    def set_chinese(self, value):
        self.__state['query_chinese'] = value
        redis_store.set(self.__key, pickle.dumps(self.__state))

    def get_last_active(self):
        return self.__state.get('last_active', datetime.now())

    def set_last_active(self, d):
        self.__state['last_active'] = d
        redis_store.set(self.__key, pickle.dumps(self.__state))

    def get_q(self):
        """ 取得原始輸入字串 """
        return self.__state.get('q', '')

    def set_q(self, value):
        self.__state['q'] = value
        redis_store.set(self.__key, pickle.dumps(self.__state))

    def get_last_handler_bot(self):
        return self.__state.get('bot', '')

    def set_last_handler_bot(self, name):
        self.__state['bot'] = name
        redis_store.set(self.__key, pickle.dumps(self.__state))
