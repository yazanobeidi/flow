class Learning(object):
    def __init__(self, q, alpha, reward, discount):
        self.q = q
        self.alpha = alpha
        self.reward = reward
        self.discount = discount

    def qlearn(self, states, actions):
        self.q[states] = [self.Q(states, actions) for action in actions if action is not None]
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
        """
        s type: tuple: qstatespace
        """
        return self.getq(s, a) + self.alpha * (self.reward(s, a) + \
                               self.discount * max(self.Q(s, a)) - self.getq(s))