# Python API to IB using ib-insync library

from ib_insync import *
import pandas as pd
import time

# Display all columns in pandas dataframe
pd.set_option('display.max_columns', None)

ib = IB()
ib.connect(host='127.0.0.1', port=7496, clientId=12)
# ib.qualifyContracts(contract)

# Real time data for stock
stock_contract = Stock('AAPL', 'SMART', 'USD')
stock_data = ib.reqTickers(stock_contract)[0]
print('Time: ', stock_data.time.ctime())
print('Stock: ', stock_data.contract.symbol)
print('Bid: ', stock_data.bid)
print('Ask: ', stock_data.ask)
print('Last: ', stock_data.last)
print('Volume: ', stock_data.volume)


# Historical data
# historical_data_aapl = ib.reqHistoricalData(aapl_contract, '',  barSizeSetting='1 hour', durationStr='2 D',  whatToShow='TRADES',  useRTH=True)
# hist_data = util.df(historical_data_aapl)
# hist_data.pop('average')
# hist_data.pop('barCount')
# print('Apple stock historical data:')
# print(hist_data)
# print()

# Options historical data
# historical_data_aapl = ib.reqHistoricalData(aapl_option_contract, '',  barSizeSetting='1 hour', durationStr='1 D',  whatToShow='TRADES',  useRTH=True)
# print('Apple options historical data:')
# hist_data = util.df(historical_data_aapl)
# hist_data.pop('average')
# hist_data.pop('barCount')
# print(hist_data)
# print()

time.sleep(1)
ib.disconnect()
