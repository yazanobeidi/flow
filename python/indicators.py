# moving average cross crossovers                
class Indicators():
    def __init__(self):
        quotes = self.quotes
        
    def Tick_5(self):
        quotes = quotes[-5:]
        num = sum(quotes)/5
        print(num)
        return num

    def Tick_7(self):
        quotes = quotes[-7:]
        num = sum(quotes)/7
        print(num)
        return num

    def Tick_10(self):
        quotes = quotes[-10:]
        num = sum(quotes)/10
        print(num)
        return num
    def Tick_15(self):
        quotes = quotes[-15:]
        num = sum(quotes)/5
        print(num)
        return num
    def Tick_20(self):
        quotes = quotes[-20:]
        num = sum(quotes)/20
        print(num)
        return num
    def Tick_30(self):
        quotes = quotes[-30:]
        num = sum(quotes)/30
        print(num)
        return num
    def Tick_40(self):
        quotes = quotes[-40:]
        num = sum(quotes)/40
        print(num)
        return num
    def Tick_50(self):
        quotes = quotes[-50:]
        num = sum(quotes)/50
        print(num)
        return num
    def Tick_100(self):
        quotes = quotes[-100:]
        num = sum(quotes)/100
        print(num)
        return num
    def Tick_200(self):
        quotes = quotes[-200:]
        num = sum(quotes)/200
        print(num)
        return num

    def X_5_7(self):
        action = 0
        if Tick_5(quotes[-2]) < Tick_7(quotes[-2]):
            if Tick_5(quotes[-1]) > Tick_7(quotes[-1]):
                action = 1
        elif Tick_5(quotes[-2]) > Tick_7(quotes[-2]):
            if Tick_5(quotes[-1]) < Tick_7(quotes[-1]):
                action = -1
        return action

    def X_5_20(self):
        action = 0
        if Tick_5(quotes[-2]) < Tick_20(quotes[-2]):
            if Tick_5(quotes[-1]) > Tick_20(quotes[-1]):
                action = 1
        elif Tick_5(quotes[-2]) > Tick_20(quotes[-2]):
            if Tick_5(quotes[-1]) < Tick_20(quotes[-1]):
                action = -1
        return action

    def X_7_20(self):
        action = 0
        if Tick_7(quotes[-2]) < Tick_20(quotes[-2]):
            if Tick_7(quotes[-1]) > Tick_20(quotes[-1]):
                action = 1
        elif Tick_7(quotes[-2]) > Tick_20(quotes[-2]):
            if Tick_7(quotes[-1]) < Tick_20(quotes[-1]):
                action = -1
        return action

    def X_7_30(self):
        action = 0
        if Tick_7(quotes[-2]) < Tick_30(quotes[-2]):
            if Tick_7(quotes[-1]) > Tick_30(quotes[-1]):
                action = 1
        elif Tick_7(quotes[-2]) > Tick_30(quotes[-2]):
            if Tick_7(quotes[-1]) < Tick_30(quotes[-1]):
                action = -1
        return action

    def X_15_40(self):
        action = 0
        if Tick_15(quotes[-2]) < Tick_40(quotes[-2]):
            if Tick_15(quotes[-1]) > Tick_40(quotes[-1]):
                action = 1
        elif Tick_15(quotes[-2]) > Tick_40(quotes[-2]):
            if Tick_15(quotes[-1]) < Tick_40(quotes[-1]):
                action = -1
        return action

    def X_20_50(self):
        action = 0
        if Tick_20(quotes[-2]) < Tick_50(quotes[-2]):
            if Tick_20(quotes[-1]) > Tick_50(quotes[-1]):
                action = 1
        elif Tick_20(quotes[-2]) > Tick_50(quotes[-2]):
            if Tick_20(quotes[-1]) < Tick_50(quotes[-1]):
                action = -1
        return action

    def X_30_100(self):
        action = 0
        if Tick_30(quotes[-2]) < Tick_100(quotes[-2]):
            if Tick_30(quotes[-1]) > Tick_100(quotes[-1]):
                action = 1
        elif Tick_30(quotes[-2]) > Tick_100(quotes[-2]):
            if Tick_30(quotes[-1]) < Tick_100(quotes[-1]):
                action = -1
        return action

    def X_50_200(self):
        action = 0
        if Tick_50(quotes[-2]) < Tick_200(quotes[-2]):
            if Tick_50(quotes[-1]) > Tick_200(quotes[-1]):
                action = 1
        elif Tick_50(quotes[-2]) > Tick_200(quotes[-2]):
            if Tick_50(quotes[-1]) < Tick_200(quotes[-1]):
                action = -1
        return action
    
    X_5_7(quotes)
    X_7_20(quotes)
    X_7_20(quotes)
    X_7_30(quotes)
    X_15_40(quotes)
    X_20_50(quotes)
    X_30_100(quotes)
    X_50_200(quotes)

    

