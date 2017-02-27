
class ForceChangeStateException(Exception):
    def __init__(self, state, halt=False):
        super().__init__("Forced Change State to: %s" % state)
        self.state = state
        self.halt = halt


class Rule:
    pass


def get_checker(input_format):
    """ input_format 是 rules 規定的 input_format，通常只有一項。
        如果有很多項的話，可能要訂定優先順序之類的。
    """
    if 'NLP_decision' in input_format:
        decision = input_format['NLP_decision']
        def checker_decision(msg):
            return ('NLP_decision' in msg) and \
                    msg['NLP_decision'] == decision
        return checker_decision

    elif 'quick_reply' in input_format:
        payload = input_format['quick_reply'].get('payload', '')
        def checker_quick_reply(msg):
            return ('quick_reply' in msg) and \
                    msg['quick_reply'].get('payload', '') == payload
        return checker_quick_reply
            
    elif 'text' in input_format:
        # TODO: support regex
        def checker_text(msg):
            return ('text' in msg)
        return checker_text

    elif 'postback' in input_format:
        payload = input_format['postback'].get('payload', '')
        def checker_postback(msg):
            return ('postback' in msg) and \
                    msg['postback'].get('payload', '') == payload
        return checker_postback

    else:
        def checker_reject_all(msg):
            return False
        return checker_reject_all
        


def transition(state_A, input_format, state_B):
    def wrap(f):
        f.rule = {
                'from_state': state_A,
                'input': input_format,
                'input_checker': get_checker(input_format),
                'transition_f': f,
                'to_state': state_B
            }
        return f
    return wrap
