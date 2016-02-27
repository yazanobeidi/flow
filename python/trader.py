
class Scope(object):
    def __init__(self, scope):
        self.scope = scope
        self.agents = [Agent(self.scope)]

    def addAgent(self):
        self.agents.append(Agent())

    def getAgents(self):
        return self.agents


class Agent(object):
    def __init__(self, scope):
        self.status = ''

    def open_position(self, type):
        pass

    def close_order(self):
        pass