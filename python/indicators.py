# moving average cross crossovers                
class Indicators(object):
    def __init__(self, log=None):
        self.logger = log
        self.state = (int(), int(), int(), int(), int(), int(), int(), int())

    def get_states(self, quotes):
        self.quotes = quotes
        self.state = ((0,0,0),
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0)
        return self.state

    def moving_average(self, size, sliced):
        return sum(sliced)/size

    def crossover_indicator(self, q, x, y):
        if self.moving_average(x, q[-x:]) < self.moving_average(y, q[-y:]):
            if self.moving_average(x, q[-x-1:-1]) > self.moving_average(y, 
                                                                    q[-y-1:-1]):
                return 1
        elif self.moving_average(x, q[-x:]) > self.moving_average(y, q[-y:]):
            if self.moving_average(x, q[-x-1:-1]) < self.moving_average(y, 
                                                                    q[-y-1:-1]):
                return -1
        return 0

    def print_quotes(self):
        print crossover_indicator(5, 10)
    

    

