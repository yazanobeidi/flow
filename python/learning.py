from indicators import indicators
class Learning(object):
    def __int__(self, q, alpha, reward, discount):
        self.q = dict()
        self.alpha = int()
        self.reward = int()
        self.discount = int()

    def learn(self, states, actions):
        self.q[states] = self.Q(states)
    
    def Q(self, s):
        """
        s type: tuple: qstatespace
        """
        return self.q[s] + self.alpha * (self.reward + self.discount * 
                                                        max(self.Q(s)) - self.q)