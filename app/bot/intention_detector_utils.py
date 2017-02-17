from app.bot.intention_bot import IntentionBot
from app.bot.greeting_intention_bot import GreetingIntentionBot
from app.bot.english_to_chinese_intention_bot import EnglishToChineseIntentionBot
from app.bot.chinese_to_english_intention_bot import ChineseToEnglishIntentionBot

import jieba
import jieba.posseg as pseg
jieba.set_dictionary("app/data/dict.txt.big")


class Pattern:
    def __init__(self, t):
        self.model = pseg.cut(t)
        self.t = t
        # 把空白和標點符號去掉
        self.model = list(filter(lambda x: x.word != ' ' and x.flag[0] != 'w', self.model))
        self.template = None
        self.targets = []
        self.score = float("-inf")

    def update_matched_information(self, score, template, targets):
        self.score = score
        self.template = template
        self.targets = targets



from itertools import compress
class Template:
    def __init__(self, s, bot_name):
        self.model = pseg.cut(s)
        self.s = s
        self.bot_name = bot_name.strip()
        # 把空白和標點符號去掉
        self.model = list(filter(lambda x: x.word != ' ' and x.flag[0] != 'w', self.model))
        # 把 target 的索引記下來
        self.target_ids = list(compress(range(len(self.model)), [x.word == 'X' for x in self.model]))

    def best_match(self, pattern):
        """ 跑一個小小 DP 計算加權的 edit distance """
        pass

    def exact_match(self, pattern):
        """ 判斷是否完全吻合, T/F, 分數, targets """
        if len(pattern.model) != len(self.model):
            return (False, 0.0, [])

        targets = []
        for i in range(len(self.model)):
            if i in self.target_ids:
                targets.append(pattern.model[i].word)
            else:
                if pattern.model[i].word != self.model[i].word or \
                    pattern.model[i].flag != self.model[i].flag:
                    return (False, 0.0, [])
        return (True, 1.0, targets)


    def match_pattern(self, pattern):
        """ 比對 s 跟 pattern.t 兩個字串的相似分數 """
        
        # 1. 完全比對: 除了 target 以外的部份全部詞性正確、文字正確
        flag, score, targets = self.exact_match(pattern)
        print("[Template Matcher]: %s, %s, %s" % (str(flag), str(score), str(targets)))
        
        if score > pattern.score:
            pattern.update_matched_information(score, self, targets)


        



class TargetIntentionExtrator:
    def __init__(self):
        self.template_loaded = False
        self.all_templates = []

    def init_template_files(self):
        if self.template_loaded == True:
            return

        print("[" + self.__class__.__name__ + "] initializing template files")
        TEMPLATE_FILE = 'app/data/target_templates'
        f = open(TEMPLATE_FILE)
        for line in f:
            v = line.split(";")
            if len(v) >= 2:
                self.all_templates.append(Template(v[0], v[1]))
        f.close()
        self.template_loaded = True

    def fetch_target_and_intention(self, t):

        if self.template_loaded == False:
            self.init_template_files()

        pattern = Pattern(t)
        for template in self.all_templates:
            template.match_pattern(pattern)
        
        bot_name = pattern.template.bot_name
        targets = pattern.targets
        print("[Template Matcher]: bot=%s, targets=%s" %(bot_name, str(targets)))

        if bot_name == EnglishToChineseIntentionBot.__name__:
            if len(targets) >= 1:
                return (targets[0], EnglishToChineseIntentionBot)
        elif bot_name == ChineseToEnglishIntentionBot.__name__:
            if len(targets) >= 1:
                return (targets[0], ChineseToEnglishIntentionBot)
        elif bot_name == GreetingIntentionBot.__name__:
            return (targets, GreetingIntentionBot)

        return (None, IntentionBot)


fetcher = TargetIntentionExtrator()

def fetching_target_and_intention(s):
    """ 從一個中文句子當中嘗試辨認 target """

    return fetcher.fetch_target_and_intention(s)

