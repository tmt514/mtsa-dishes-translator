from app.bot.constants import *
from app.bot.intention_bot import IntentionBot
from app.bot.greeting_intention_bot import GreetingIntentionBot
from app.bot.english_to_chinese_intention_bot import EnglishToChineseIntentionBot
from app.bot.chinese_to_english_intention_bot import ChineseToEnglishIntentionBot

class IntentionDetector:
    """ 判斷使用者傳訊息的意圖為何 

        EnglishToChineseIntentionBot -- 當使用者輸入英文訊息，想要查詢中文時
        ChineseToEnglishIntentionBot -- 當使用者輸入中文，想要取得英文菜名時

        TODO: GreetingIntentionBot -- 當使用者打招呼時要如何回覆
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


    def contains_chinese(self, s):
        try:
            for i in range(len(s)):
                if s[i] > '\u4e00' and s[i] < '\u9fff':
                    print("[%s] ==> true" % s)
                    return True
        except:
            pass
        print("[%s] ==> false" % s)
        return False

    def get_intention_bot(self, sender, state, msgbody):

        # 如果是用 quick reply 回覆剛才的選單的話，直接交給剛才處理的 bot
        if 'quick_reply' in msgbody:
            if state.get_last_handler_bot() == EnglishToChineseIntentionBot.__name__:
                return EnglishToChineseIntentionBot()
            if state.get_last_handler_bot() == ChineseToEnglishIntentionBot.__name__:
                return ChineseToEnglishIntentionBot()

        if state.get_status() == 'new': 
            if 'text' in msgbody and self.contains_chinese(msgbody['text']) == True:
                return ChineseToEnglishIntentionBot()

        return EnglishToChineseIntentionBot()


