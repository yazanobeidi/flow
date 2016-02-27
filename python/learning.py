
class Learning(object):
    def __int__(self, q, alpha, reward, discount, indicators):
        self.q = dic()
        self.alpha = int()
        self.reward = int()
        self.discount = int()

    def learn(self, states, actions):
        self.q = self.Q(states, actions)
    
    def Q(self, s, a):
        return self.q[s] + self.alpha * (self.reward + self.discount * 
                                                    max(self.Q(s, a)) - self.q)