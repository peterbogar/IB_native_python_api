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
print('Apple stock real time data:')
print(ticker.marketPrice())
print()

# Historical data
historical_data_aapl = ib.reqHistoricalData(aapl_contract, '',  barSizeSetting='1 hour', durationStr='1 D',  whatToShow='TRADES',  useRTH=False)
hist_data = util.df(historical_data_aapl)
hist_data.pop('average')
hist_data.pop('barCount')
print('Apple stock historical data:')
print(hist_data)
print()

# Real time option data
ib.reqMarketDataType(4)
aapl_option_contract = Option('AAPL', '20210219', 130, 'C', 'SMART')
ticker = ib.reqMktData(aapl_option_contract)
print('Apple options real time data:')
print(ticker.marketPrice())
print()

# Options historical data
historical_data_aapl = ib.reqHistoricalData(aapl_option_contract, '',  barSizeSetting='1 hour', durationStr='1 D',  whatToShow='TRADES',  useRTH=False)
print('Apple options historical data:')
hist_data = util.df(historical_data_aapl)
hist_data.pop('average')
hist_data.pop('barCount')
print(hist_data)
print()
