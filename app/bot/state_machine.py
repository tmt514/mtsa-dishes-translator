from app.bot.rule import Rule, ForceChangeStateException
from app.bot.intention_rules import *
from collections import defaultdict

class StateMachine():
    def __init__(self):
        self.state_graph = defaultdict(list)
        self.has_initialized = False

    def __init(self):
        self.has_initialized = True

        all_classes = Rule.__subclasses__()
        for Ruleset in all_classes:
            print("\033[0;33mLoading Ruleset <%s>\033[m" % Ruleset.__name__)
            # 生一個 instance 出來
            ruleset = Ruleset()
            for rulename in dir(ruleset):
                rule_f = getattr(ruleset, rulename)
                if hasattr(rule_f, 'rule'):
                    print("\033[0;34m... adding rule: %s\033[m" % rule_f.__name__)
                    rule = rule_f.rule
                    self.state_graph[rule['from_state']].append(rule)

    def __run(self, bot, user, msg, **template_params):
        state_A = user.get_status()
        print("[StateMachine] %s" % (msg))
        #if state_A.endswith("__running"):
            ## 直接 drop 這個 request: TODO: 待討論
            # print("\033[0;31mLogic running!\033[m")
            # return

        user.set_status(state_A + "__running")
        for rule in self.state_graph[state_A]:
            if rule['input_checker'](msg) == True:
                try:
                    print("\033[0;34mMatch rule %s\033[m" % rule['transition_f'].__name__)
                    halt = rule['transition_f'](None, bot, user, msg, **template_params)
                    user.set_status(rule['to_state'])
                    print("\033[0;35m%s -> %s\033[m" % (state_A, rule['to_state']))
                    return halt
                except ForceChangeStateException as e:
                    print(e)
                    user.set_status(e.state)
                    print("\033[0;35m%s -> %s\033[m" % (state_A, e.state))
                    return e.halt
                else:
                    print("\033[0;35m%s -> %s\033[m" % (state_A, 'CRASHED'))
                    user.set_status('CRASHED')



        user.set_status('new')
        # if STATE_NEW and could not find any logic -> halt
        print("\033[0;35m%s -> %s\033[m" % (state_A, 'new'))
        print("\033[0;31mLogic not found!\033[m")
        return (state_A == 'new')

    def run(self, bot, user, msg, **template_params):

        # 對於不同的 worker, 每一隻都會分別初始化
        if self.has_initialized == False:
            self.__init()

        # 在 state diagram 上面跑直到停下來為止
        while self.__run(bot, user, msg, **template_params) == False:
            pass
