import ib_functions as ib

output = None

# Create contract
stk_aapl = ib.create_contract('AAPL')

ib.get_contract_details(stk_aapl)
# output = ib.get_market_price(stk_aapl)
# output = ib.get_historical_data(stk_aapl, '1 D', '30 mins')
print(type(output))
print(output)
