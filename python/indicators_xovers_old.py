# moving average cross crossovers                
class Indicators(object):
    def __init__(self, log=None):
        self.logger = log
        self.state = (0,0,0,0,0,0,0,0,0,0)
        
    def get_states(self, prev_states, quotes):
        self.quotes = quotes
        self.prev_states = prev_states
        #print len(quotes)
        self.state = (self.crossover_indicator(self.prev_states[0], self.quotes, 5, 7),
                      self.crossover_indicator(self.prev_states[1], self.quotes, 5, 20),
                      self.crossover_indicator(self.prev_states[2], self.quotes, 7, 30),
                      self.crossover_indicator(self.prev_states[3], self.quotes, 12, 26),
                      self.crossover_indicator(self.prev_states[4], self.quotes, 50, 100),
                      self.crossover_indicator(self.prev_states[4], self.quotes, 50, 200),
                      self.MACD_sig_line(self.prev_states[5], self.quotes, 12, 26, 9),
                      self.MACD_zero_cross(self.prev_states[6], self.quotes, 12, 26),
                      self.MACD_trend(self.quotes, 12, 26, 9),
                      self.RSI(self.quotes, 14, 25))
        self.logger.debug('State: {}'.format(self.state))
        return self.state

    def moving_average(self, size, sliced):
        if len(sliced) < size:
            return 0.0
        multiplier = 0.0
        multiplier = 2/(float(size) + 1)
        ema = sum(sliced)/float(size)
        for value in sliced:
            ema = (multiplier*value) + ((1-multiplier)*ema)
        return ema

    def crossover_indicator(self, prev, q, x, y):
        #print("if current x less than y")
        if self.moving_average(x, q[-x:]) < self.moving_average(y, q[-y:]):
            #print "if prev x greater than y"
            if self.moving_average(x, q[-x-1:-1]) > self.moving_average(y, 
                                                                    q[-y-1:-1]):
                #print -1 
                return -1
        
        elif self.moving_average(x, q[-x:]) > self.moving_average(y, q[-y:]):
            #print "if prev x less than y"
            if self.moving_average(x, q[-x-1:-1]) < self.moving_average(y, 
                                                                    q[-y-1:-1]):
                #print 1
                return 1
        #print 0
        return prev

#https://en.wikipedia.org/wiki/MACD#Mathematical_interpretation
    def MACD(self, q, m1, m2):
        if len(q) < m2: 
            return 0.0
        signal = self.moving_average(m1, q[-m1:]) - self.moving_average(m2, q[-m2:])
        return signal

    def MACD_series(self, q, m1, m2):
        if len(q) < m2: 
            return 0.0
        series = []
        i = 0
        for quotes in q:
            if m2 > i:
                series.append(self.moving_average(m1, q[-m1-i:-i]) - self.moving_average(m2, q[-m2-i:-i]))
            i += 1
        if m2 < i:                                                
            series.append(self.MACD(q,m1,m2))                                              
        return series

    def MACD_sig_line(self, prev, q, m1, m2, m3):
        if len(q) < m3 or len(q) < m2:
            return 0
        self.series = self.MACD_series(q, m1, m2)
        if self.MACD(q, m1, m2) < self.moving_average(m3, self.series[-m2:]):
            if self.MACD(q[:-1], m1, m2) > self.moving_average(m3, self.series[-m2-1:-1]):
                return -1
        elif self.MACD(q, m1, m2) > self.moving_average(m3, self.series[-m2:]):
            if self.MACD(q[:-1], m1, m2) < self.moving_average(m3, self.series[-m2-1:-1]):
                return 1
        return prev

    def MACD_zero_cross(self, prev, q, m1, m2):
        if self.MACD(q[:-1], m1, m2) > 0 and self.MACD(q, m1, m2) < 0:
            return -1
        elif self.MACD(q[:-1], m1, m2) < 0 and self.MACD(q, m1, m2) > 0:
            return 1
        return prev

    def RSI(self, q, period, threshold):
        i = 0
        upcount = 0
        downcount = 0
        RS = 50.0
        updays = []
        downdays = []
        if len(q) < 4*period:
            return 0
        while (upcount <= period and downcount <= period) and i < len(q) - 1:
            if q[1+i] < q[i]:
                updays.append(q[1+i])
                upcount += 1
            elif q[1+i] > q[i]:
                downdays.append(q[1+i])
                downcount += 1
            i += 1
        try:
            RS = self.moving_average(period, updays) / self.moving_average(period, downdays)
        except:
            RS = 0
        #print self.moving_average(period, downdays)
        if float(self.moving_average(period, downdays)) != 0.0:
            RS = float(self.moving_average(period, updays)) / float(self.moving_average(period, downdays))
            #print RS
        #print len(q)
        RSI = (100-(100/(1+RS)))
        print RSI
        #print RSI
        if RSI < threshold:
            return 1
        elif RSI > (100-threshold):
            return -1
        return 0

    def MACD_trend(self, q, m1, m2, m3):
        if len(q) < m1 or len(q) < m2 or len(q) < m3:
            return 0
        self.series = self.MACD_series(q, m1, m2)
        if self.MACD(q, m1, m2) < self.moving_average(m3, self.series[-m2:]):
            return -1
        elif self.MACD(q, m1, m2) > self.moving_average(m3, self.series[-m2:]):
            return 1
        return 0

    
                
                
        

    

