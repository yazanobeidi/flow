from csv import reader
import logging
from trader import Scope
from bankroll import Bankroll

QUOTES_CSV = '../data/DAT_NT_USDCAD_T_LAST_201601.csv'
LOG_FILE = '../logs/runlog.log'
#SCOPES = {10, 50, 100, 500, 3600, 14400}
#scopenum = [10, 50, 100, 500, 3600, 14400]
SCOPES = {100}
scopenum = [100]
Q = dict()
ALPHA = 0.5
REWARD = tuple()
DISCOUNT = 0.5
ALL_profit = []

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
        self.hop = 1
        while self.hop < len(self.all_quotes):
            #self.logger.info('Bankroll: {}'.format(self.bankroll.get_bankroll()))
            self.get_new_quote(self.hop)
            self.logger.debug('Quote {}'.format(self.hop))
            for scope in self.scopes:
                if not scope.agents:
                    self.logger.info('Adding agent to {}'.format(scope))
                    scope.add_agent()
                else:
                    i = 0
                    for agent in scope.agents:
                        if agent.status['status'] != 'open':
                            i += 1;
                    #if i == 0:
                        #self.logger.info('Adding agent to {}'.format(scope))
                        #scope.add_agent(scope, Q, ALPHA, REWARD, DISCOUNT, self.quotes, self.bankroll)

            self.supervise()
            self.hop += 1
        for i in range(len(self.all_profit)-1):
            self.logger.info('Ave. Profit:'.format(sum(self.all_profit)/len(self.all_profit)))
            self.logger.info('{}'.format(self.all_profit[i]))



    def supervise(self):
        for scope in self.scopes:
            agents = scope.get_agents()
            #i = 0
            #for agent in agents:
            #    if agent.status['status'] != 'open':
            #        i+=1
            #if i > 0:
            #    scope.add_agent()
    
    def load_scopes(self):
        q = Q
        alpha = ALPHA
        reward = REWARD
        discount = DISCOUNT
        self.all_profit = ALL_profit
        for scope in SCOPES:
            self.scopes.append(Scope(scope, q, alpha, reward, discount, 
                                       self.quotes, self.bankroll, self.all_profit, self.logger))
        self.logger.info('Scopes generated')

    def get_new_quote(self, x):
        new_quote = self.all_quotes[-x]
        self.quotes.append(new_quote)
        i = 0
        for scope in self.scopes:
            if self.hop%scopenum[i] == 0:
                self.logger.debug('Updating Scope {num}'.format(num=scopenum[i]))
                scope.update(new_quote)
            i+=1
        #self.logger.info('Quotes fetched')

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
    