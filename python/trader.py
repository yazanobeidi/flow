from learning import Learning

class Scope(object):
    def __init__(self, scope, q, alpha, reward, discount):
        self.scope = scope
        self.agents = [Agent(self.scope, q, alpha, reward, discount)]

    def add_agent(self, scope, q, alpha, reward, discount):
        self.agents.append(Agent(scope, q, alpha, reward, discount))

    def get_agents(self):
        return self.agents


class Agent(Learning):
    def __init__(self, scope, q, alpha, reward, discount):
        Learning.__init__(q, alpha, reward, discount)
        Indicators.__init(quotes)
        self.status = ''

    def start_learning(self, states, actions):
        self.learn(states, actions)

    def open_position(self, type):
        pass

    def close_order(self):
        pass