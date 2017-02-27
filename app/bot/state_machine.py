from app.bot.rule import Rule, ForceChangeStateException
from collections import defaultdict

class StateMachine():
    def __init__(self):
        self.state_graph = defaultdict(list)
        
        all_classes = Rule.__subclasses__()
        for ruleset in all_classes:
            print("\033[0;33mLoading Ruleset <%s>\033[m" % ruleset.__name__)
            for rulename in dir(ruleset):
                rule_f = getattr(ruleset, rulename)
                if hasattr(rule_f, 'rule'):
                    print("\033[0;34m... adding rule: %s\033[m" % rule_f.__name__)
                    rule = rule_f.rule
                    self.state_graph[rule['from_state']].append(rule)

    def __run(self, bot, user, msg, **template_params):
        state_A = user.get_status()
        if state_A.endswith("__running"):
            # 直接 drop 這個 request: TODO: 待討論
            return

        user.set_status(state_A + "__running")
        for rule in self.state_graph[state_A]:
            if rule['input_checker'](msg) == True:
                try:
                    print("Match rule %s" % rule)
                    halt = rule['transition_f'](bot, user, msg, **template_params)
                    user.set_status(rule['to_state'])
                    return halt
                except ForceChangeStateException as e:
                    print(e)
                    user.set_status(e.state)
                    return e.halt


        user.set_status('new')
        return False

    def run(self, bot, user, msg, **template_params):
        while self.__run(bot, user, msg, **template_params) == False:
            pass
