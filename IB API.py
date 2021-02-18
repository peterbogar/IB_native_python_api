# Python API to IB using ib-insync library

from ib_insync import *
import pandas as pd
import time

# Display all columns in pandas dataframe
pd.set_option('display.max_columns', None)

ib = IB()
ib.connect(host='127.0.0.1', port=7496, clientId=12)
# ib.qualifyContracts(contract)


def get_stock_data(symbol, real=False, hist=False):
    stock_contract = Stock(symbol, 'SMART', 'USD')

    if real:
        stock_data = ib.reqTickers(stock_contract)[0]
        print()
        print('Real time data for', stock_contract.symbol)
        print('Time: ', stock_data.time.ctime())
        print('Bid: ', stock_data.bid)
        print('Ask: ', stock_data.ask)
        print('Last: ', stock_data.last)
        print('Volume: ', stock_data.volume)

    if hist:
        hist_data = util.df(ib.reqHistoricalData(stock_contract, '', barSizeSetting='1 hour', durationStr='2 D', whatToShow='TRADES', useRTH=True))
        print()
        hist_data.pop('average')
        hist_data.pop('barCount')
        print('Historica data for', stock_contract.symbol)
        print(hist_data)
        print()


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


get_stock_data('AAPL', real=True, hist=False)
get_options_data('AAPL', '20210319', 120, 'C', real=True, hist=False)

time.sleep(1)
ib.disconnect()
