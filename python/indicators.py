# moving average cross crossovers                
class Indicators():
    def __init__(self, quotes):
        self.quotes = quotes
        
    def Tick_5(self, offset):
        data = self.quotes
        data = data[-5*(offset+1):(-5*offset+offset-1)]
        num = sum(data)/5
        return num

    def Tick_7(self, offset):
        data = self.quotes
        data = data[-7*(offset+1):(-7*offset+offset-1)]
        num = sum(data)/7
        return num
    def Tick_10(self, offset):
        data = self.quotes
        data = data[-10*(offset+1):(-10*offset+offset-1)]
        num = sum(data)/10
        return num
    def Tick_15(self, offset):
        data = self.quotes
        data = data[-15*(offset+1):(-15*offset+offset-1)]
        num = sum(data)/5
        return num
    def Tick_20(self, offset):
        data = self.quotes
        data = data[-20*(offset+1):(-20*offset+offset-1)]
        num = sum(data)/20
        return num
    def Tick_30(self, offset):
        data = self.quotes
        data = data[-30*(offset+1):(-30*offset+offset-1)]
        num = sum(data)/30
        return num
    def Tick_40(self, offset):
        data = self.quotes
        data = data[-40*(offset+1):(-40*offset+offset-1)]
        num = sum(data)/40
        return num
    def Tick_50(self, offset):
        data = self.quotes
        data = data[-50*(offset+1):(-50*offset+offset-1)]
        num = sum(data)/50
        return num
    def Tick_100(self, offset):
        data = self.quotes
        data = data[-100*offset:(-100*(offset-1)+offset-1)]
        num = sum(data)/100
        return num
    def Tick_200(self, offset):
        data = self.quotes
        data = data[-200*offset:(-200*(offset-1)+offset-1)]
        num = sum(data)/200
        return num

    def X_5_7(self):
        data = self.quotes
        action = 0
        if self.Tick_5(1) < self.Tick_7(1):
            if self.Tick_5(0) > self.Tick_7(0):
                action = 1
        elif self.Tick_5(1) > self.Tick_7(1):
            if self.Tick_5(0) < self.Tick_7(0):
                action = -1
        return action

    def X_5_20(self):
        action = 0
        if self.Tick_5(1) < self.Tick_20(1):
            if self.Tick_5(0) > self.Tick_20(0):
                action = 1
        elif self.Tick_5(1) > self.Tick_20(1):
            if self.Tick_5(0) < self.Tick_20(0):
                action = -1
        return action

    def X_7_20(self):
        action = 0
        if self.Tick_7(1) < self.Tick_20(1):
            if self.Tick_7(0) > self.Tick_20(0):
                action = 1
        elif self.Tick_7(1) > self.Tick_20(1):
            if self.Tick_7(0) < self.Tick_20(0):
                action = -1
        return action

    def X_7_30(self):
        action = 0
        if self.Tick_7(1) < self.Tick_30(1):
            if self.Tick_7(0) > self.Tick_30(0):
                action = 1
        elif self.Tick_7(1) > self.Tick_30(1):
            if self.Tick_7(0) < self.Tick_30(0):
                action = -1
        return action

    def X_15_40(self):
        action = 0
        if self.Tick_15(2) < self.Tick_40(2):
            if self.Tick_15(1) > self.Tick_40(1):
                action = 1
        elif self.Tick_15(2) > self.Tick_40(2):
            if self.Tick_15(1) < self.Tick_40(1):
                action = -1
        return action

    def X_20_50(self):
        action = 0
        if self.Tick_20(1) < self.Tick_50(1):
            if self.Tick_20(0) > self.Tick_50(0):
                action = 1
        elif self.Tick_20(1) > self.Tick_50(1):
            if self.Tick_20(0) < self.Tick_50(0):
                action = -1
        return action

    def X_30_100(self):
        action = 0
        if self.Tick_30(1) < self.Tick_100(1):
            if self.Tick_30(0) > self.Tick_100(0):
                action = 1
        elif self.Tick_30(1) > self.Tick_100(1):
            if self.Tick_30(0) < self.Tick_100(0):
                action = -1
        return action

    def X_50_200(self):
        action = 0
        if self.Tick_50(1) < self.Tick_200(1):
            if self.Tick_50(0) > self.Tick_200(0):
                action = 1
        elif self.Tick_50(1) > self.Tick_200(1):
            if self.Tick_50(0) < self.Tick_200(0):
                action = -1
        return action

    def print_quotes(self):
        print(self.X_5_7())
        print(self.X_5_20())
        print(self.X_7_20())
        print(self.X_7_30())
        print(self.X_15_40())
        print(self.X_20_50())
        print(self.X_30_100())
        print(self.X_50_200())

    

    

