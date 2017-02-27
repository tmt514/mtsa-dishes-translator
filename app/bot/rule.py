
class ForceChangeStateException(Exception):
    def __init__(self, state, halt=False):
        super().__init__("Forced Change State to: %s" % state)
        self.state = state
        self.halt = halt


class Rule:
    pass


def get_checker(input_format):
    if 'NLP_decision' in input_format:
        decision = input_format['NLP_decision']
        def checker_decision(msg):
            if 'NLP_decision' not in msg:
                return False
            return msg['NLP_decision'] == decision
        return checker_decision

    elif 'quick_reply' in input_format:
        payload = input_format['quick_reply'].get('payload', '')
        def checker_quick_reply(msg):
            if 'quick_reply' not in msg:
                return False
            s = msg['quick_reply'].get('payload', '')
            return s == payload
        return checker_quick_reply
            
    elif 'text' in input_format:
        # TODO: support regex
        def checker_text(msg):
            return ('text' in msg)
        return checker_text

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
