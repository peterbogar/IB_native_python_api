# Python API to IB using ib-insync library

from ib_insync import *
import pandas as pd

# Display all columns in pandas dataframe
pd.set_option('display.max_columns', None)


ib = IB()
print()
print(ib.connect(host='127.0.0.1', port=7496, clientId=12))
print()
aapl_contract = Stock('AAPL', 'SMART', 'USD')
print(aapl_contract)
print()
print(ib.qualifyContracts(aapl_contract))
print()

# Real time data
ib.reqMarketDataType(4)
ticker = ib.reqMktData(aapl_contract)
print(ticker.marketPrice())

# Historical data
historical_data_aapl = ib.reqHistoricalData(aapl_contract, '',  barSizeSetting='1 hour', durationStr='2 D',  whatToShow='TRADES',  useRTH=False)
print()
hist_data = util.df(historical_data_aapl)
hist_data.pop('average')
hist_data.pop('barCount')
print(hist_data)
