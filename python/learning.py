
class Learning(object):
    def __int__(self, q, alpha, reward, discount, indicators):
        self.q = int()
        self.alpha = int()
        self.reward = int()
        self.discount = int()
        self.generate_q_space()

    def learn(self, states, actions):
        self.q = self.Q(states, actions)

    def generate_q_space(self):
        #3^8 state spaces
        self.space = {}
        for options in range(0, indicators):
            self.space[[]] = int()

    
    def Q(self, s, a):
        return self.q + self.alpha * (self.reward + self.discount * 
                                                    max(self.Q(s, a)) - self.q)