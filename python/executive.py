from csv import reader
import logging
from datetime import datetime

from trader import Scope
from bankroll import Bankroll
from utils.plotter import Plotter

__author__= 'yazan/matthew'

QUOTES_CSV = 'data/DAT_NT_USDCAD_T_LAST_201601.csv'
LOG_FILE = 'logs/runlog.log'
VAULT = 'logs/bankroll.log'
RESOLUTION = 100 # Width factor of bankroll plot output
FUNDS = 100 # Starting bankroll
SCOPES = {1} # Defines what scopes will be initialized
Q = dict() # This could be moved to Learning or QLearn module
ALPHA = 0.888
REWARD = tuple()
DISCOUNT = 0.01 # low discount factor = short sighted
LIMIT = 3 # Maximum number of agents in a given scope

class Executive():
    """
    High Frequency Statistical Forex Trading.
    Executive is the gatekeeper and master of all agents. Executive can spawn 
        new agents, kill agents, share learned information between agents. 
        Agents live in scopes, which are resolutions of time. At any hop, there
        is always at least one agent with no open position ready to place a 
        trade.
    #TODO: Encorporate the idea of "spread"
    """
    def __init__(self):
        self.init_logging()
        self.logger.info('Initializing Executive...')
        self.bankroll_plot = Plotter([0], [FUNDS], RESOLUTION)
        self.bankroll = Bankroll(VAULT, FUNDS, plot=self.bankroll_plot)
        self.all_quotes = []
        self.quotes = []
        self.scopes = []
        self.scope_plots = {}
        self.load_csv()
        self.load_scopes()

    def supervise(self):
        """
        Main Executive function which controls the flow of all activity.
        """
        self.logger.info('Running...')
        hop = 0
        start_time = datetime.now()
        while hop < len(self.all_quotes):
            elapsed = (datetime.now() - start_time).total_seconds()
            self.logger.info('Hop: {hop} Bankroll: {funds} Elapsed: {sec} '\
                             'H/S = {hs}'.format(sec=elapsed, hop=hop, 
                            funds=self.bankroll.get_bankroll(), hs=hop/elapsed))
            new_quote = self.get_new_quote(hop)
            for scope in self.active_scopes(hop):
                scope.refresh(new_quote)
                scope.trade()
            hop += 1
    
    def active_scopes(self, hop):
        """
        Generator of active scopes for a given hop.
        """
        for scope in self.scopes:
            if hop % scope.scope == 0:
                yield scope

    def load_scopes(self):
        """
        Creates scope instances (with their own agents) defined by SCOPES set.
        """
        for scope in SCOPES:
            # Not sure why but if we allow scope plots, Python confuses between
            # scope plot instances and bankroll plot instance.........???????
            #self.scope_plots[scope] = Plotter([1,2,3,4,5], [44,11,64,232,54])
            self.scopes.append(Scope(scope, Q, ALPHA, REWARD, DISCOUNT, LIMIT,
                            self.quotes, self.bankroll, self.logger, plot=True))
        self.logger.info('Scopes generated')

    def get_new_quote(self, x):
        """
        Fetches a single, newest, quote. Simulates an API call.
        """
        new_quote = self.all_quotes[-x]
        self.quotes.append(new_quote)
        self.logger.debug('Quotes fetched')
        return new_quote

    def print_quotes(self):
        """
        For debugging: display all quotes to console.
        """
        for quote in self.all_quotes:
            print quote

    def load_csv(self):
        """
        For development: loads CSV development file into memory.
        """
        with open(QUOTES_CSV) as csvfile:
            quotes = reader(csvfile, delimiter=';', quotechar='|')
            for quote in quotes:
                 self.all_quotes.append(float(quote[-2]))
            self.logger.info('Loading data complete')

    def init_logging(self):
        """
        Logging initialization and boilerplate.
        """
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
    Supervisor = Executive()
    Supervisor.supervise()