import random
from qlearn import QLearn

class Learning(QLearn):
    def __init__(self, q, alpha, reward, discount, initial_state, actions):
        self.q = {}
        self.alpha = alpha
        self.reward = reward
        self.discount = discount
        self.states = initial_state
        QLearn.__init__(self, actions, len(initial_state), alpha)