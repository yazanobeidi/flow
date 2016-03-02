from qlearn import QLearn

__author__ = 'yazan'

class Learning(QLearn):
    """
    This class links all learning modules a trader might use together.
    Learning sits on top of Indicators, so really Learning is just a map between
    the state tuple Indicators returns and one of 3 actions (0, 1 or -1).
    #TODO: research and implement new learning algorithms
    #TODO: combine multiple learning algorithms into a single response
    """
    def __init__(self, q, alpha, reward, discount, initial_state, actions):
        self.q = {}
        self.alpha = alpha
        self.reward = reward
        self.discount = discount
        self.states = initial_state
        QLearn.__init__(self, actions, len(initial_state), alpha)