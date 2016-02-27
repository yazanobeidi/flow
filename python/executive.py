from csv import reader
import logging
from trader import Scope, Agent
from learning import Learning

QUOTES_CSV = 'data/DAT_NT_USDCAD_T_LAST_201601.csv'
LOG = 'logs/runlog.log'
SCOPES = {1, 10, 50, 100, 500, 1000}
Q = 0
ALPHA = 0
REWARD = 0
DISCOUNT = 0

class Executive(object):
    def __init__(self):
        self.logger = logging.getLogger(LOG)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s \
                                                                 - %(message)s')
        self.quotes = []
        self.scopes = []
        self.run = True
        self.load_csv()

    def start(self):
        self.load_scopes()
        while self.run:
            for scope in self.scopes:
                if not scope.agents:
                    scope.add_agent()
            self.supervise()
            self.run = False # for debugging

    def supervise(self):
        for scope in self.scopes:
            agents = scope.get_agents()
            for agent in agents:
                agent.start_learning()
    
    def load_scopes(self):
        q = Q
        alpha = ALPHA
        reward = REWARD
        discount = DISCOUNT
        for scope in SCOPES:
            self.scopes.append(Scope(scope, q, alpha, reward, discount))

    def print_quotes(self):
        for quote in self.quotes:
            print quote

    def load_csv(self):
        with open(QUOTES_CSV) as csvfile:
            quotes = reader(csvfile, delimiter=';', quotechar='|')
            for quote in quotes:
                 self.quotes.append(quote[-2])


if __name__ == "__main__":
    trader = Executive()
    trader.start()
    #trader.print_quotes()
    