from app.bot.intention_bot import GreetingIntentionBot, En2ZhTwIntentionBot

class IntentionDetector:
    """ 判斷使用者傳訊息的意圖為何 

        En2ZhTwIntentionBot -- 當使用者輸入英文訊息，想要查詢中文時

        TODO: GreetingIntentionBot -- 當使用者打招呼時要如何回覆
        TODO: Tw2EnIntentionBot -- 當使用者輸入中文，想要取得英文菜名時
        TODO: PictureIntentionBot -- 當使用者想更知道方才輸入之食物的圖片時
        TODO: LocationIntentionBot -- 當使用者想知道該如何就近取得食材時
        TODO: MoreInfoIntentionBot -- 當使用者想知道更多有關該食物的訊息

        TODO: 這裡要加上 NLP 的東西，判斷到底使用者想幹嘛
    """
    def __init__(self, bot):
        self.bot = bot
    
    def is_english(self, s):
        try:
            s.encode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return True


    def get_intention_bot(self, sender, state, msg):
        return En2ZhTwIntentionBot()


