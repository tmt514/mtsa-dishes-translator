
from app.bot.intention_detector_utils import Template, TemplateEnglish, \
        Pattern, PatternEnglish, fetching_target_and_intention_jieba, fetching_target_and_intention_nltk
from app.tests.test_app import AAFoodTestCase


class NLPTest(AAFoodTestCase):

    def test_fetching_target_and_intention_jieba(self):
        suggest_state, template_params = fetching_target_and_intention_jieba("請幫我翻譯 avocado 的中文")
        assert 'target' in template_params
        assert template_params['target'] == 'avocado'
        
        print(suggest_state, template_params)

        suggest_state, template_params = fetching_target_and_intention_jieba("嗨")
        print(suggest_state, template_params)
        assert suggest_state == 'STATE_GREETING'
        
        suggest_state, template_params = fetching_target_and_intention_jieba("謝謝")
        print(suggest_state, template_params)
        assert suggest_state == 'STATE_GREETING'
        

        
    def test_pattern_match(self):
        suggest_state, template_params = fetching_target_and_intention_jieba('冷笑話')
        assert suggest_state == 'STATE_COLD_JOKE'
