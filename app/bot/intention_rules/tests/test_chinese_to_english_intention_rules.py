from app.tests.test_app import AAFoodTestCase
from app.bot.intention_rules import *
from app.bot.rule import Rule

class ChineseToEnglishIntentionRuleTests(AAFoodTestCase):
    def test_zh_to_en(self):
        all_classes = Rule.__subclasses__()
        for ruleset in all_classes:
            print("\033[0;33mLoading Ruleset <%s>\033[m" % ruleset.__name__)
            for rulename in dir(ruleset):
                rule = getattr(ruleset, rulename)
                if hasattr(rule, 'rule'):
                    print("\033[0;34m... adding rule: %s\033[m" % rule.__name__)
