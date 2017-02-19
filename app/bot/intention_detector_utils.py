from app.bot.intention_bot import IntentionBot
from app.bot.greeting_intention_bot import GreetingIntentionBot, YouAreWelcomeIntentionBot
from app.bot.cold_joke_intention_bot import ColdJokeIntentionBot
from app.bot.english_to_chinese_intention_bot import EnglishToChineseIntentionBot
from app.bot.chinese_to_english_intention_bot import ChineseToEnglishIntentionBot

import jieba
import jieba.posseg as pseg
jieba.set_dictionary("app/data/dict.txt.big")

import nltk
import json

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


class PatternEnglish(Pattern):
    def __init__(self, t):
        super().__init__(t)
        self.model = [pseg.pair(word=x[0].strip().lower(), flag=x[1]) for x in nltk.pos_tag(nltk.word_tokenize(t))]
        self.model = list(filter(lambda x: x.word != ' ' and x.flag[0] != '.', self.model))



from itertools import compress
class Template:
    def __init__(self, s, bot_name, bot_params):
        self.model = pseg.cut(s)
        self.s = s
        self.bot_name = bot_name.strip()
        self.bot_params = bot_params
        # 把空白和標點符號去掉
        self.model = list(filter(lambda x: x.word != ' ' and x.flag[0] != 'w', self.model))
        # 把 target 的索引記下來
        self.target_ids = list(compress(range(len(self.model)), [x.word == 'X' for x in self.model]))
        

    def best_match(self, pattern):
        """ 跑一個小小 DP 計算加權的 edit distance:

            計算規則：
            - 詞性相符:         SCORE_FLAG_MATCH[詞性] =
            - 詞性和詞句皆相符: SCORE_EXACT_MATCH[詞性] =
            - target 不能跳過   SCORE_TARGET_MATCH
        """
        # TODO: move these to proper config file
        SCORE_FLAG_MATCH_DEFAULT = 1.0
        SCORE_FLAG_MATCH = {}
        SCORE_EXACT_MATCH_DEFAULT = 2.0
        SCORE_EXACT_MATCH = {}
        SCORE_TARGET_MATCH = 0.0

        dp = [[(0.0, []) for y in range(len(pattern.model)+1)] for x in range(len(self.model)+1)]
        n = len(self.model)
        m = len(pattern.model)
        for i in range(len(self.model)):
            if i in self.target_ids:
                # Target --
                for j in range(len(pattern.model)):
                    dp[i+1][j+1] = (dp[i][j][0], dp[i][j][1] + [pattern.model[j].word])
            else:
                for j in range(len(pattern.model)):

                    # Not Target -- No Match
                    if dp[i+1][j+1][0] < dp[i+1][j][0]:
                        dp[i+1][j+1] = dp[i+1][j]
                    if dp[i+1][j+1][0] < dp[i][j+1][0]:
                        dp[i+1][j+1] = dp[i][j+1]

                    # Not Target -- Case 1: Exact match
                    if self.model[i].word == pattern.model[j].word and\
                            self.model[i].flag == pattern.model[j].flag:
                        new_score = dp[i][j][0] + SCORE_EXACT_MATCH.get(self.model[i].flag, SCORE_EXACT_MATCH_DEFAULT)
                        if dp[i+1][j+1][0] < new_score:
                            dp[i+1][j+1] = (new_score, dp[i][j][1])
                    # Not Target -- Case 2: only flag match
                    elif self.model[i].flag == pattern.model[j].flag:
                        new_score = dp[i][j][0] + SCORE_FLAG_MATCH.get(self.model[i].flag, SCORE_FLAG_MATCH_DEFAULT)
                        if dp[i+1][j+1][0] < new_score:
                            dp[i+1][j+1] = (new_score, dp[i][j][1])

        return (True, dp[n][m][0] / n, dp[n][m][1])


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
        return (True, 100.0, targets)


    def match_pattern(self, pattern):
        """ 比對 s 跟 pattern.t 兩個字串的相似分數 """
        
        # 1. 完全比對: 除了 target 以外的部份全部詞性正確、文字正確
        flag, score, targets = self.exact_match(pattern)
        print("[%s]: %s, %s, %s" % (self.__class__.__name__, str(flag), str(score), str(targets)))
        if flag == True and score > pattern.score:
            pattern.update_matched_information(score, self, targets)

        # 2. Edit Distance 比對
        flag, score, targets = self.best_match(pattern)
        print("[%s]: %s, %s, %s" % (self.__class__.__name__, str(flag), str(score), str(targets)))
        if flag == True and score > pattern.score:
            pattern.update_matched_information(score, self, targets)

        

class TemplateEnglish(Template):
    def __init__(self, s, bot_name, bot_params):
        super().__init__(s, bot_name, bot_params)
        self.model = [pseg.pair(word=x[0].strip().lower(), flag=x[1]) for x in nltk.pos_tag(nltk.word_tokenize(s))]
        self.model = list(filter(lambda x: x.word != ' ' and x.flag[0] != '.', self.model))
        self.target_ids = list(compress(range(len(self.model)), [x.word == 'X' for x in self.model]))

        



class TargetIntentionExtrator:
    def __init__(self):
        self.template_loaded = False
        self.all_templates = []
        self.template_file = 'app/data/target_templates'
        self.template_class = Template
    
    def make_template(self, s, bot_name, bot_params={}):
        return self.template_class(s, bot_name, bot_params)

    def init_template_files(self):
        if self.template_loaded == True:
            return

        print("[" + self.__class__.__name__ + "] initializing template files")
        f = open(self.template_file)
        for line in f:
            v = line.split(";")
            if len(v) >= 3:
                self.all_templates.append(self.make_template(v[0], v[1], v[2].split(",")))
            elif len(v) >= 2:
                self.all_templates.append(self.make_template(v[0], v[1]))
        f.close()
        self.template_loaded = True

    def fetch_target_and_intention(self, pattern):

        if self.template_loaded == False:
            self.init_template_files()

        for template in self.all_templates:
            template.match_pattern(pattern)
        
        bot_name = pattern.template.bot_name
        targets = pattern.targets
        params = pattern.template.bot_params
        print("[%s]: bot=%s, targets=%s, params=%s" %(self.__class__.__name__, bot_name, str(targets), json.dumps(params)))

        if bot_name == EnglishToChineseIntentionBot.__name__:
            if len(targets) >= 1:
                return (targets[0], EnglishToChineseIntentionBot)
        elif bot_name == ChineseToEnglishIntentionBot.__name__:
            if len(targets) >= 1:
                return (targets[0], ChineseToEnglishIntentionBot)
        elif bot_name == GreetingIntentionBot.__name__:
            return (params, GreetingIntentionBot)
        elif bot_name == YouAreWelcomeIntentionBot.__name__:
            return (params, YouAreWelcomeIntentionBot)
        elif bot_name == ColdJokeIntentionBot.__name__:
            return (params, ColdJokeIntentionBot)

        return (None, None)


class TargetIntentionExtratorEnglish(TargetIntentionExtrator):
    def __init__(self):
        super().__init__()
        self.template_file = 'app/data/target_templates_english'
        self.template_class = TemplateEnglish


fetcher_jieba = TargetIntentionExtrator()
fetcher_nltk = TargetIntentionExtratorEnglish()


def fetching_target_and_intention_jieba(s):
    """ 從一個中文句子當中嘗試辨認 target """
    return fetcher_jieba.fetch_target_and_intention(Pattern(s))

def fetching_target_and_intention_nltk(s):
    """ 從一個英文句子中嘗試辨認 target """
    return fetcher_nltk.fetch_target_and_intention(PatternEnglish(s))
