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
    # print(get_stock_market_data('SPY'))
    stock_contract = Stock(symbol, 'SMART', 'USD')
    ib.reqMarketDataType(1)  # Ak vrat -1, treba nstavit Frozen- 2
    stock_data = ib.reqTickers(stock_contract)[0] # Mimo RTH to trva 11s!!, v RTH 0,24s
    # vrati tuple: time, bid, ask, last, volume
    return stock_data.time.strftime('%A %e-%m-%Y %H:%M:%S %Z'), stock_data.bid, stock_data.ask, stock_data.last, stock_data.volume
def get_stock_hist_data(symbol, bar_size, duration, rth):
    # print(get_stock_hist_data(symbol='SPY', bar_size='5 mins', duration='2 D', rth=False))
    stock_contract = Stock(symbol, 'SMART', 'USD')
    hist_data = util.df(ib.reqHistoricalData(stock_contract, '', barSizeSetting=bar_size, durationStr=duration, whatToShow='TRADES', useRTH=rth)) # Toto trva 0,4s (aj pre 100dni)
    hist_data.pop('average')
    hist_data.pop('barCount')
    # Vrati dataframe
    return hist_data
def get_options_market_data(symbol, exp, strike, right):
    # print(get_options_market_data('SPY', '20210319', 400, 'C'))
    options_contract = Option(symbol, exp, strike, right, 'SMART', '100', 'USD')
    ib.reqMarketDataType(2)
    options_data = ib.reqTickers(options_contract)[0]

    # Osetrenie vynimky, ak niesu dostupne live data, iba frozen z predchadzajuceho close, nieje tam delta
    try:
        return options_data.time.strftime('%A %e-%m-%Y %H:%M:%S %Z'), options_data.bid, options_data.ask, options_data.modelGreeks.delta
    except AttributeError:
        return options_data.time.strftime('%A %e-%m-%Y %H:%M:%S %Z'), options_data.bid, options_data.ask
def get_options_hist_data(symbol, exp, strike, right):
    # print(get_options_hist_data('SPY', '20210319', 400, 'C'))
    options_contract = Option(symbol, exp, strike, right, 'SMART', '100', 'USD')
    options_hist_data = ib.reqHistoricalData(options_contract, '',  barSizeSetting='1 hour', durationStr='10 D',  whatToShow='TRADES',  useRTH=True)
    df_options_hist_data = util.df(options_hist_data)
    df_options_hist_data.pop('average')
    df_options_hist_data.pop('barCount')

    return df_options_hist_data


sym = 'SPY'
call_put = ['C', 'P']
expirations = ['20210222', '20210301', '20210319', '20210416', '20210521']
strikes = range(350, 421)

file = open('test_options_data.csv', 'a')

for cp in call_put:
    for expiry in expirations:
        for strk in strikes:
            data = get_options_market_data(sym, expiry, strk, cp)
            content = (data, strk, expiry, cp, sym)
            print(content)
            file.write(str(content))
            file.write('\n')


file.close()
time.sleep(1)
ib.disconnect()
