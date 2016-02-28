from csv import reader
import logging
from trader import Scope
from bankroll import Bankroll

QUOTES_CSV = 'data/DAT_NT_USDCAD_T_LAST_201601.csv'
LOG_FILE = 'logs/runlog.log'
SCOPES = {1, 10, 50, 100, 500, 1000}
Q = dict()
ALPHA = 0.5
REWARD = tuple()
DISCOUNT = 0.5

class Executive():
    def __init__(self):
        self.init_logging()
        self.logger.info('Initializing Executive...')
        self.bankroll = Bankroll()
        self.all_quotes = []
        self.quotes = []
        self.scopes = []
        self.load_csv()
        self.load_scopes()

    def start(self):
        self.logger.info('Running...')
        hop = 1
        while hop < len(self.all_quotes):
            self.logger.info('Bankroll: {}'.format(self.bankroll.get_bankroll()))
            self.get_new_quote(hop)
            self.logger.info('Trade {}'.format(hop))
            for scope in self.scopes:
                if not scope.agents:
                    self.logger.info('Adding agent to {}'.format(scope))
                    scope.add_agent()
            self.supervise()
            hop += 1

    def supervise(self):
        for scope in self.scopes:
            agents = scope.get_agents()
            for agent in agents:
                self.logger.debug('{agent} in {scope} is learning'.format(
                                                      agent=agent, scope=scope))
                agent.trade()
    
    def load_scopes(self):
        q = Q
        alpha = ALPHA
        reward = REWARD
        discount = DISCOUNT
        for scope in SCOPES:
            self.scopes.append(Scope(scope, q, alpha, reward, discount, 
                                       self.quotes, self.bankroll, self.logger))
        self.logger.info('Scopes generated')

    def get_new_quote(self, x):
        new_quote = self.all_quotes[-x]
        self.quotes.append(new_quote)
        for scope in self.scopes:
            scope.update(new_quote)
        self.logger.info('Quotes fetched')

    def print_quotes(self):
        for quote in self.all_quotes:
            print quote

    def load_csv(self):
        with open(QUOTES_CSV) as csvfile:
            quotes = reader(csvfile, delimiter=';', quotechar='|')
            for quote in quotes:
                 self.all_quotes.append(float(quote[-2]))
            self.logger.info('Loading data complete')

    def init_logging(self):
        self.logger = logging.getLogger('flow')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(LOG_FILE, mode='w')
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
    