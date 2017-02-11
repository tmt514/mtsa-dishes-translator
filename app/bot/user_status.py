from app.app import redis_store
import pickle
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
                'last_active':datetime.now()
                })
            )

    def get_status(self):
        return self.__state['status']

    def set_status(self, status):
        self.__state['status'] = status
        redis_store.set(self.__key, pickle.dumps(self.__state))

    def get_english(self):
        return self.__state['query_english']

    def set_english(self, value):
        self.__state['query_english'] = value
        redis_store.set(self.__key, pickle.dumps(self.__state))

    def get_chinese(self):
        return self.__state['query_chinese']

    def set_chinese(self, value):
        self.__state['query_chinese'] = value
        redis_store.set(self.__key, pickle.dumps(self.__state))

    def get_last_active(self):
        return self.__state['last_active']

    def set_last_active(self, d):
        self.__state['last_active'] = d
        redis_store.set(self.__key, pickle.dumps(self.__state))

    def get_q(self):
        """ 取得原始輸入字串 """
        return self.__state['q']

    def set_q(self, value):
        self.__state['q'] = value
        redis_store.set(self.__key, pickle.dumps(self.__state))
