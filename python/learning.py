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
"""
    def qlearn(self, states, actions):
        self.q[states] = [self.Q(states, action) for action in actions]
        self.states = states
        return self.q[states]

    def getq(self, s, a, default=0):
        try:
            return self.q[s][a]
        except KeyError:
            return default

    def getr(self, s, a, default=0):
        try:
            return self.reward[s][a]
        except IndexError:
            return default

    def Q(self, s, a):
        '''
        s type: tuple: qstatespace
        '''
        return self.getq(self.states, a) + self.alpha * \
                                (self.reward(self.states, a) + self.discount * \
                                  max(self.Q(s, a)) - self.getq(self.states, a))


    """


