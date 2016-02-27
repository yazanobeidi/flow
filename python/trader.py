
class Scope(object):
    def __init__(self, scope):
        self.agents = [Agent(scope)]


class Agent(object):
    def __init__(self, scope):
        self.status = ''

    def open_position(self, type):
        pass

    def close_order(self):
        pass


if __name__ == "__main__":
    trader = Executive()
    trader.start()