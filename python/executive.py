"""Flow - Algorithmic HF trader

   Copyright 2016, Yazan Obeidi

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from csv import reader
import logging
from trader import Scope
from bankroll import Bankroll

__author__= 'yazan/matthew'

QUOTES_CSV = 'data/DAT_NT_USDCAD_T_LAST_201601.csv'
LOG_FILE = 'logs/runlog.log'
VAULT = 'logs/bankroll.log'
FUNDS = 1000
SCOPES = {1, 50, 1000}
Q = dict()
ALPHA = 0.7
REWARD = tuple()
DISCOUNT = 0.314
LIMIT = 11

class Executive():
    """
    High Frequency Statistical Forex Trading.
    Executive is the gatekeeper and master of all agents. Executive can spawn 
        new agents, kill agents, share learned information between agents. 
        Agents live in scopes, which are resolutions of time. At any hop, there
        is always at least one agent with no open position ready to place a 
        trade.
    """
    def __init__(self):
        self.init_logging()
        self.logger.info('Initializing Executive...')
        self.bankroll = Bankroll(VAULT, FUNDS)
        self.all_quotes = []
        self.quotes = []
        self.scopes = []
        self.load_csv()
        self.load_scopes()

    def supervise(self):
        self.logger.info('Running...')
        hop = 0
        while hop < len(self.all_quotes):
            self.logger.info('Hop {hop} Bankroll: {bankroll}'.format(hop=hop, 
                                         bankroll=self.bankroll.get_bankroll()))
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
        for scope in SCOPES:
            self.scopes.append(Scope(scope, Q, ALPHA, REWARD, DISCOUNT, LIMIT,
                                       self.quotes, self.bankroll, self.logger))
        self.logger.info('Scopes generated')

    def get_new_quote(self, x):
        new_quote = self.all_quotes[-x]
        self.quotes.append(new_quote)
        self.logger.info('Quotes fetched')
        return new_quote

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
    trader.supervise()
