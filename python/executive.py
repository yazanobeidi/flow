from csv import reader
import sys
import logging
import oandapy
from trader import Scope
from OANDA_streaming import MyStreamer
from bankroll import Bankroll
from order import Order, BUY, SELL, OPEN, ACTIONS
import time

QUOTES_CSV = 'data/DAT_NT_USDCAD_T_LAST_201601.csv'
LOG_FILE = 'logs/runlog.log'
#SCOPES = {10, 50, 100, 1000, 3600, 14400}
SCOPES = {60}
scopenum = []
# SCOPES = {1}
#scopenum = [1]
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
        self.asks = []
        self.bids = []
        self.all_quotes = [1,1]
        self.scopes = []
        self.timer = time.time()
        self.ticks = 0
        self.load_scopes()
        self.live_source = False
        self.oanda = oandapy.API(
            environment="practice", access_token="b80047744433a4551a28ce4734d0"
            "4559-057e8fb7fb775467b97b7f64d313cfd5")
        if len(sys.argv) > 1:
            if sys.argv[1] == "live":
                self.live_source = True
            else: self.load_csv()
        else: self.load_csv()


    def start(self):
        self.logger.info('Running...')
        #should implement a command system
        COMMAND = ''
        hop = 1
        while COMMAND != 'Q' and hop <len(self.all_quotes):
            #determine where to pull quotes
            if self.live_source:
                self.get_quotes_OANDA()
            else:
                self.get_new_quote(hop)
                self.ticks = hop
                hop += 1

            for scope in self.scopes:
                if not scope.agents:
                    self.logger.debug('Adding agent to {}'.format(scope))
                    scope.add_agent()
            self.supervise()

        '''
        things to do after program is 'done'.
         we should identify 'done' state
        '''

    def supervise(self):
        num_available = 0
        for scope in self.scopes:
            agents = scope.get_agents()
            if scope.activate == True:
                for agent in agents:
                    if agent.status['action'] is not OPEN:
                        num_available += 1
                        agent.trade(self.ticks, scope)
                        break
                if num_available == 0:
                    agent.trade(self.ticks, scope)

    def load_scopes(self):
        q = Q
        alpha = ALPHA
        reward = REWARD
        discount = DISCOUNT
        self.all_profit = ALL_profit
        for scope in SCOPES:
            scopenum.append(scope)
            self.scopes.append(Scope(scope, q, alpha, reward, discount,
                                     self.asks, self.bids, self.bankroll,
                                     self.all_profit, self.logger))
        self.logger.info('Scopes generated')

    def print_quotes(self):
        for quote in self.all_bids:
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
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s '
                                      '- %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


    def get_new_quote(self, x):
        new_quote = self.all_quotes[-x]
        ask = new_quote
        bid = new_quote - 0.00038
        self.asks.append(ask)
        self.bids.append(bid)
        self.logger.debug(
            'Ask, Bid {num}: {ask}, {bid}'.format(num=x,
                                                  ask=ask, bid=bid))
        i = 0
        for scope in self.scopes:
            if x%scopenum[i] == 0: 
                self.logger.debug(
                'Updating Scope {num}'.format(num=scopenum[i]))          
                scope.update(ask, bid)
                scope.activate = True
            else:
                scope.activate = False
            i += 1

    def get_quotes_OANDA(self):
        # I SHOULD ADD FUNCTIONALITY TO CHANGE BASED ON SMALLEST SIZED SCOPE
        delta = 0.0
        delta = time.time() - self.timer
        if delta < 1:
            time.sleep(1-delta)
        # elif delta > 1:
            # raise Exception('Code took {} seconds to process quote!'
            #.format(delta))
        self.timer = time.time()
        self.logger.debug('Loop time: {num}'.format(num=delta))

        response = self.oanda.get_prices(instruments="USD_CAD")
        prices = response.get("prices")
        ask = prices[0].get("ask")
        bid = prices[0].get("bid")
        self.ticks += 1
        self.asks.append(ask)
        self.bids.append(bid)
        self.logger.debug(
            'Ask, Bid {num}: {ask}, {bid}'.format(num=self.ticks,
                                                  ask=ask, bid=bid))
        i = 0
        for scope in self.scopes:
            if self.ticks % scopenum[i] == 0:
                self.logger.debug(
                'Updating Scope {num}'.format(num=scopenum[i]))
                scope.update(ask, bid)
                scope.activate = True
            else:
                scope.activate = False
            i += 1


if __name__ == "__main__":
    trader = Executive()
    trader.start()
