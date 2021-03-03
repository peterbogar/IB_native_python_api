# Main function for IB API

import ib_functions as ib
from threading import Timer


ib_connect = ib.TestApp()
ib_connect.connect('127.0.0.1', 7496, 12)

symbols = ['AAPL', 'FB', 'QQQ', 'SPY', 'NVDA']
# symbols = ['AAPL']
ticker_id = 0

for symbol in symbols:
    ticker_id += 1
    contract = ib.create_contract(symbol)
    ib_connect.reqMarketDataType(2)
    ib_connect.reqMktData(ticker_id, contract, '', True, False, [])

Timer(1, ib_connect.stop).start()
ib_connect.run()

print()
print(ib_connect.output_df)
