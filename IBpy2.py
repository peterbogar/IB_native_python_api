# ib_api_demo.py

from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection
from time import sleep


def error_handler(msg):
    print('Server Error: %s', msg)


def reply_handler(msg):
    print('Server Response: %s, %s"', msg.typeName, msg)


def create_stock_contract(symbol, sec_type, exch, prim_exch, curr):
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract


def create_stock_order(order_type, quantity, action):
    order = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    return order


def create_options_contract(sym, exp, right, strike):
    opt_contract = Contract()
    opt_contract.m_symbol = sym
    opt_contract.m_secType = 'OPT'
    opt_contract.m_right = right
    opt_contract.m_expiry = exp
    opt_contract.m_strike = float(strike)
    opt_contract.m_exchange = 'SMART'
    opt_contract.m_currency = 'USD'
    # opt_contract.m_localSymbol = ''
    # opt_contract.m_primaryExch = ''
    return opt_contract


def create_options_order(action, order_id, tif, order_type):
    opt_order = Order()
    opt_order.m_orderId = order_id
    opt_order.m_clientId = 0
    opt_order.m_permid = 0
    opt_order.m_action = action
    opt_order.m_lmtPrice = 0
    opt_order.m_auxPrice = 0
    opt_order.m_tif = tif
    opt_order.m_transmit = False
    opt_order.m_orderType = order_type
    opt_order.m_totalQuantity = 1
    return opt_order


tws = Connection.create(port=7496, clientId=12)
tws.connect()
# tws.register(error_handler, 'Error')
# tws.registerAll(reply_handler)

aapl_contract = create_stock_contract('AAPL', 'STK', 'SMART', 'SMART', 'USD')
spy_contract = create_options_contract('SPY', '20210319', 'C', 400)

# Vytvorenie stock order
# aapl_order = create_stock_order('MKT', 100, 'BUY')
# tws.placeOrder(1, aapl_contract, aapl_order)

# Vytvorenie options order
# spy_order = create_options_order('BUY', 100, 'DAY', 'MKT')
# tws.placeOrder(100, spy_contract, spy_order)

# Market data
# con.unregister(watcher, message.tickSize, message.tickPrice, message.tickString, message.tickOptionComputation)
# con.register(my_BidAsk, message.tickPrice)
# tws.reqMktData(1, spy_contract, '', True)

ib.reqHistoricalData(aapl_contract, '', barSizeSetting=bar_size, durationStr=duration, whatToShow='TRADES', useRTH=rth)

sleep(2)
tws.disconnect()
