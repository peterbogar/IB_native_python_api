# Main function for IB Python API

import ib_functions as ib
from threading import Timer
import pandas as pd


# Define variables
# symbols = ['AAPL', 'FB', 'QQQ', 'SPY', 'NVDA']
symbols = ['SPY']
exps = ['20210319']
strikes = ['380', '381']
rights = ['C', 'P']

# Make connection
ib_connect = ib.TestApp()
ib_connect.connect('127.0.0.1', 7496, 12)

# Get market price for one or more symbols
# ib.get_market_price(ib_connect, symbols)

# Do not mix stock price and options price due to duplicate ticketr ID

# Get market price for options chain for one or more symbols
ib.get_options_market_price(ib_connect, symbols, exps, strikes, rights)

Timer(3, ib_connect.stop).start()
ib_connect.run()

# Print output
print()
ib_connect.output_df = ib_connect.output_df.sort_index()
print(ib_connect.output_df)
print()
