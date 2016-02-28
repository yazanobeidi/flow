from csv import reader
import logging
from trader import Scope, Agent
from learning import Learning

QUOTES_CSV = 'data/DAT_NT_USDCAD_T_LAST_201601.csv'
LOG_FILE = 'logs/runlog.log'
SCOPES = {1, 10, 50, 100, 500, 1000}
Q = 0
ALPHA = 0
REWARD = 0
DISCOUNT = 0

class Executive(object):
    def __init__(self):
        self.init_logging()
        self.logger.info('Initializing Executive...')
        self.quotes = []
        self.scopes = []
        self.run = True
        self.load_csv()
        self.load_scopes()

    def start(self):
        self.logger.info('Running...')
        hop = 1
        while self.run:
            self.logger.info('Trade {}'.format(hop))
            for scope in self.scopes:
                if not scope.agents:
                    self.logger.info('Adding agent to {}'.format(scope))
                    scope.add_agent()
            self.supervise()
            self.run = False # for debugging
            hop += 1

    def supervise(self):
        for scope in self.scopes:
            agents = scope.get_agents()
            for agent in agents:
                self.logger.info('{agent} in {scope} learning'.format(
                                                      agent=agent, scope=scope))
                agent.start_learning()
    
    def load_scopes(self):
        q = Q
        alpha = ALPHA
        reward = REWARD
        discount = DISCOUNT
        for scope in SCOPES:
            self.scopes.append(Scope(scope, q, alpha, reward, discount))
        self.logger.info('Scopes generated')

    def print_quotes(self):
        for quote in self.quotes:
            print quote

    def load_csv(self):
        with open(QUOTES_CSV) as csvfile:
            quotes = reader(csvfile, delimiter=';', quotechar='|')
            for quote in quotes:
                 self.quotes.append(float(quote[-2]))
            self.logger.info('Loading data complete')

    def init_logging(self):
        self.logger = logging.getLogger('flow')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s '\
                                                                '- %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


if __name__ == "__main__":
    trader = Executive()
    trader.start()
    #trader.print_quotes()
    