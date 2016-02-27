
class Learning(object):
    def __int__(self, q, alpha, reward, discount, indicators):
        self.q = int()
        self.alpha = int()
        self.reward = int()
        self.discount = int()
        self.spaces = dict()
        self.generate_q_space(indicators)

    def learn(self, states, actions):
        self.q = self.Q(states, actions)
    
    def Q(self, s, a):
        return self.q + self.alpha * (self.reward + self.discount * 
                                                    max(self.Q(s, a)) - self.q)