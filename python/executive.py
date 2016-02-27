from csv import reader
from trader import Scope, Agent
from learning import Learning

QUOTES_CSV = 'data/DAT_NT_USDCAD_T_LAST_201601.csv'
SCOPES = {1, 10, 50, 100, 500, 1000}

class Executive(object):
    def __init__(self):
        self.quotes = []
        self.scopes = []
        self.run = True
        self.load_csv()

    def start(self):
        self.load_scopes()
        while self.run:
            for scope in self.scopes:
                if not scope.agents:
                    scope.addAgent()
            self.supervise()
            self.run = False

    def supervise(self):
        for scope in self.scopes:
            agents = scope.getAgents()
            #print agents
    
    def load_scopes(self):
        for scope in SCOPES:
            self.scopes.append(Scope(scope))

    def load_csv(self):
        with open(QUOTES_CSV) as csvfile:
            quotes = reader(csvfile, delimiter=';', quotechar='|')
            for quote in quotes:
                 self.quotes.append(quote[-2])


if __name__ == "__main__":
    trader = Executive()
    trader.start()
    