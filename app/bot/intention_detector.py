from app.bot.intention_detector_utils import *


import jieba
class IntentionDetector:
    """ 判斷使用者傳訊息的意圖為何 
        parse_msg 會把原本的 msgbody 修改成大家通吃的格式 (quick_reply, NLP_decision...)

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

    def parse_msg(self, user, msgbody):
        params = {}
        if 'quick_reply' in msgbody:
            payload = msgbody['quick_reply'].get('payload', '')
            pos = payload.find(":")
            if pos != -1:
                target = payload[pos+1:]
                payload = payload[0:pos]
                msgbody['quick_reply']['payload'] = payload
                msgbody['quick_reply']['target'] = target

        if 'text' in msgbody:
            is_chinese = self.contains_chinese(msgbody['text'])
            if is_chinese == True:
                NLP_decision, params = fetching_target_and_intention_jieba(msgbody['text'])
                msgbody['NLP_decision'] = NLP_decision
            else:
                NLP_decision, params = fetching_target_and_intention_nltk(msgbody['text'])
                msgbody['NLP_decision'] = NLP_decision

        return (msgbody, params)


    def get_postback_intention_bot(self, sender, state, payload, target):
        return IntentionBot()
