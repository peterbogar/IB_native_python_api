# Python API to IB using ib-insync library

from ib_insync import *
import pandas as pd
import time

# Display all columns in pandas dataframe
pd.set_option('display.max_columns', None)

ib = IB()
ib.connect(host='127.0.0.1', port=7496, clientId=12)
# ib.qualifyContracts(contract)


def get_stock_market_data(symbol):
    stock_contract = Stock(symbol, 'SMART', 'USD')
    ib.reqMarketDataType(1)  # Ak vrat -1, treba nstavit Frozen- 2
    stock_data = ib.reqTickers(stock_contract)[0] # Toto trva 11s!!!!
    # vrati tuple: bid, ask, last, volume
    return stock_data.bid, stock_data.ask, stock_data.last, stock_data.volume


def get_stock_hist_data(symbol, bar_size, duration, rth):
    stock_contract = Stock(symbol, 'SMART', 'USD')
    hist_data = util.df(ib.reqHistoricalData(stock_contract, '', barSizeSetting=bar_size, durationStr=duration, whatToShow='TRADES', useRTH=rth)) # Toto trva 0,4s (aj pre 100dni)
    hist_data.pop('average')
    hist_data.pop('barCount')
    # Vrati dataframe
    return hist_data


print(get_stock_market_data('SPY'))
print(get_stock_hist_data(symbol='SPY', bar_size='1 day', duration='10 D', rth=False))


def get_options_market_data(symbol, exp, strike, right):
    options_contract = Option(symbol, exp, strike, right, 'SMART', '100', 'USD')
    ib.reqMarketDataType(2)
    options_data = ib.reqTickers(options_contract)[0]

    # Osetrenie vynimky, ak niesu dostupne live data, iba frozen z predchadzajuceho close, nieje tam delta
    try:
        return options_data.bid, options_data.ask, options_data.lastGreeks.delta
    except AttributeError:
        return options_data.bid, options_data.ask


# print(get_options_market_data('SPY', '20210319', 400, 'C'))


















def get_options_data(symbol, exp, strike, right, real=False, hist=False):
    options_contract = Option(symbol, exp, strike, right, 'SMART')

    if real:
        print()
        opt_data = ib.reqTickers(options_contract)[0]
        print('Options real time data for', options_contract.symbol)
        print('Time: ', opt_data.time.ctime())
        print('Expiration: ', options_contract.lastTradeDateOrContractMonth)
        print('Strike: ', options_contract.strike)
        print('Call/Put: ', options_contract.right)
        print('Bid: ', opt_data.bid)
        print('Ask: ', opt_data.ask)
        print('Delta: ', round(opt_data.lastGreeks.delta, 3))
        print()

    if hist:
        hist_opt_data = ib.reqHistoricalData(options_contract, '',  barSizeSetting='1 hour', durationStr='1 D',  whatToShow='TRADES',  useRTH=True)
        print()
        print('Options real time data for', options_contract.symbol)
        print('Expiration: ', options_contract.lastTradeDateOrContractMonth)
        print('Strike: ', options_contract.strike)
        print('Call/Put: ', options_contract.right)
        hist_data = util.df(hist_opt_data)
        hist_data.pop('average')
        hist_data.pop('barCount')
        print(hist_data)
        print()



# get_options_data('AAPL', '20210319', 120, 'C', real=True, hist=False)

time.sleep(1)
ib.disconnect()
