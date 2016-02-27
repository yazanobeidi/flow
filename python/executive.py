import csv
from executive import Agent

QUOTES_CSV = 'data/DAT_NT_USDCAD_T_LAST_201601.csv'

class Executive(object):
    def __init__(self):
        self.quotes = []
        self.agents = []
        self.load_csv()

    def start(self):
        if not self.agents:
            self.agents.append(Agent())
        self.supervise()

    def supervise(self):
        for agent in self.agents:
            if agent.status = 'closed'
            

    def load_csv(self):
        with open(QUOTES_CSV) as csvfile:
            quotes = csv.reader(csvfile, delimiter=';', quotechar='|')
            for quote in quotes:
                 self.quotes.append(quote[-2])


if __name__ == "__main__":
    trader = Executive()
    trader.start()