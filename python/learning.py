
class Learning(object):
    def __int__(self, q, alpha, reward, discount):
        self.q = int()
        self.alpha = int()
        self.reward = int()
        self.discount = int()
    
    def Q(self, s, a):
        return self.q + self.alpha * (self.reward + self.discount * 
                                                    max(self.Q(s, a)) - self.q)