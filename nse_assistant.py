from nsetools import Nse
import requests, json


class NseAssist:
    def __init__(self):
        pass

    def get_advanced_indices(self):
        nse = Nse()
        indices_data = nse.get_advances_declines()
        x = sorted(indices_data, key=lambda i: i['advances'] / (i['advances'] + i['declines'] + i['unchanged']),
                   reverse=True)
        print(x[:5])

    def get_top_gainers(self):
        nse = Nse()
        top_gainers = nse.get_top_gainers()
        x = filter(lambda x: x['openPrice'] == x['lowPrice'], top_gainers)
        print(list(x))
        y = list(x)
        for stock in top_gainers:
            print(stock)

    def scan_stocks(self, nse_index):
        nse = Nse()
        with open('index_data.json') as nse_data:
            try:
                nse_dict = json.load(nse_data)
            except FileNotFoundError as e:
                print("unable to find nifty index file")
        bullish_stocks = []
        bearish_stocks = []
        if nse_index in nse_dict:
            for stock in nse_dict[nse_index]:
                print("checking stock {0}:".format(stock))
                q = nse.get_quote(stock)
                if q['open'] == q['dayLow']:
                    bullish_stocks.append(stock)
                if q['open'] == q['dayHigh']:
                    bearish_stocks.append(stock)
            print("bullish stocks found are {0}".format(','.join(bullish_stocks)))
            print("bearish stocks found are {0}".format(','.join(bearish_stocks)))


if __name__ == "__main__":
    n = NseAssist()
    index = input("enter nifty index ")
    n.scan_stocks(index)
