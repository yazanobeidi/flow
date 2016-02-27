import csv
from executive import Agent, Scope, Learning

QUOTES_CSV = 'data/DAT_NT_USDCAD_T_LAST_201601.csv'
SCOPES = {1, 10, 50, 100, 500, 1000}

class Executive(object):
    def __init__(self):
        self.quotes = []
        self.scopes = []
        self.load_csv()

    def start(self):
        self.load_scopes()
        while True:
            for scope in self.scopes:
                if not scope.agent:
                    scope.addAgent()
            self.supervise()

    def supervise(self):
        for scope in self.scopes:
            for agent in scope.get_agents():
                # Do something with agent
    
    def load_scopes(self):
        for scope in SCOPES:
            self.scopes.append(Scope())

    def load_csv(self):
        with open(QUOTES_CSV) as csvfile:
            quotes = csv.reader(csvfile, delimiter=';', quotechar='|')
            for quote in quotes:
                 self.quotes.append(quote[-2])


if __name__ == "__main__":
    trader = Executive()
    trader.start()
    