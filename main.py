# Main function for IB API

import ib_functions as ib
from threading import Timer


# Create contract
# stk = ib.create_contract('AAPL')
# opt = ib.create_options_contract('AAPL', '20210319', 130, 'C')

ib_connect = ib.TestApp()
ib_connect.connect('127.0.0.1', 7496, 12)

symbols = ['AAPL', 'SPY', 'NVDA', 'QQQ', 'FB']
ib_connect.reqMarketDataType(2)
ib_connect.reqMktData(1, ib.create_contract(symbols[0]), '', True, False, [])
ib_connect.reqMktData(2, ib.create_contract(symbols[1]), '', True, False, [])
ib_connect.reqMktData(3, ib.create_contract(symbols[2]), '', True, False, [])
ib_connect.reqMktData(4, ib.create_contract(symbols[3]), '', True, False, [])
ib_connect.reqMktData(5, ib.create_contract(symbols[4]), '', True, False, [])

Timer(1, ib_connect.stop).start()
ib_connect.run()

print(ib_connect.output_df)
