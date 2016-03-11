import oandapy

class MyStreamer(oandapy.Streamer):
    def __init__(self, all_asks, all_bids, scopes, log, *args, **kwargs):
        oandapy.Streamer.__init__(self, *args, **kwargs)
        self.all_bids = all_bids
        self.all_asks = all_asks
        self.logger = log
        self.scopes = scopes
        self.ticks = 0
        self.start(accountId=3191815, instruments="USD_CAD")

    def on_success(self, data):
        self.ticks += 1
        ask = str(data).split(":")[2]
        ask = ask.split(",")[0]
        ask = float(ask.strip())
        bid = str(data).split(":")[4]
        bid = bid.split(",")[0]
        bid = float(bid.strip())

        self.all_asks.append(ask)
        self.all_bids.append(bid)
        
        print self.all_asks[self.ticks-1]
        print self.all_bids[self.ticks-1]
        i = 0
        for scope in self.scopes:
            if self.ticks%scopenum[i] == 0:
                self.logger.debug('Updating Scope {num}'.format(num=scopenum[i]))
                scope.update(ask, bid)
            i+=1

    def on_error(self, data):
        self.disconnect()
        raise Exception('Stream disconnected due to error')