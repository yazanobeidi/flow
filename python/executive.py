import csv

QUOTES_CSV = 'DAT_NT_USDCAD_T_LAST_201601'

class Executive(object):
    def __init__(self):
        self.load_csv()


    def start(self):
        pass

    def load_csv(self):
        with open(QUOTES_CSV) as csvfile:
            quotes = csv.reader(csvfile, delimeter='')




if __name__ == "__main__":
    trader = Executive()
    trader.start()