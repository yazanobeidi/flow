class Learning(object):
    def __init__(self, q, alpha, reward, discount):
        self.q = q
        self.alpha = alpha
        self.reward = reward
        self.discount = discount

    def qlearn(self, states):
        self.q[states] = self.Q(states)
        return self.q[states]

    def get(self, s, default=0):
        try:
            return self.q[s]
        except KeyError:
            return default

    def Q(self, s):
        """
        s type: tuple: qstatespace
        """
        return self.get(s) + self.alpha * (self.reward + self.discount * 
                                                   max(self.Q(s)) - self.get(s))