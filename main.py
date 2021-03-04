# Main function for IB API

import ib_functions as ib
from threading import Timer
import pandas as pd


# Define variables
# symbols = ['AAPL', 'FB', 'QQQ', 'SPY', 'NVDA']
symbols = ['AAPL']
exps = ['20210319']
strikes = ['380', '381', '382']
right = ['C', 'P']
ticker_id = 0

# Create dataframe with options chain definitions
option_chain_df = pd.DataFrame({'Symbol': [], 'Exp': [], 'Strike': [], 'Right': [], 'Bid': [], 'Ask': []})
for symbol in symbols:
    for exp in exps:
        for strike in strikes:
            for r in right:
                # print(symbol, exp, strike, r)
                option_chain_df.loc[ticker_id, 'Symbol'] = symbol
                option_chain_df.loc[ticker_id, 'Exp'] = exp
                option_chain_df.loc[ticker_id, 'Strike'] = strike
                option_chain_df.loc[ticker_id, 'Right'] = r
                option_chain_df.loc[ticker_id, 'Bid'] = 0
                option_chain_df.loc[ticker_id, 'Ask'] = 0
                ticker_id += 1


# ib_connect = ib.TestApp()
# ib_connect.connect('127.0.0.1', 7496, 12)
#
# for symbol in symbols:
#     contract = ib.create_contract(symbol)
#     ib_connect.reqMarketDataType(2)
#     ib_connect.reqMktData(ticker_id, contract, '', True, False, [])
#     ticker_id += 1
#
# Timer(1, ib_connect.stop).start()
# ib_connect.run()
#
# print()
# ib_connect.output_df = ib_connect.output_df.sort_index()
# print(ib_connect.output_df)
# print()

print(option_chain_df)
