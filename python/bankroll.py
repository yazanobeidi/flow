class Bankroll(object):
    def __init__(self):
        self.bankroll = 1000

    def transaction(self, val):
        self.bankroll += val

    def get_bankroll(self):
        return self.bankroll