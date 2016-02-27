import csv

QUOTES_CSV = 'data/DAT_NT_USDCAD_T_LAST_201601.csv'

class Executive(object):
    def __init__(self):
        self.quotes = []
        self.load_csv()

    def start(self):
        pass

    def load_csv(self):
        with open(QUOTES_CSV) as csvfile:
            quotes = csv.reader(csvfile, delimiter=';', quotechar='|')
            for quote in quotes:
                 self.quotes.append(quote[-2])


if __name__ == "__main__":
    trader = Executive()
    trader.start()