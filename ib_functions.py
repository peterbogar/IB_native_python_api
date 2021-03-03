# Native IB API
# Based from https://cdcdyn.interactivebrokers.com/webinars/TA-2018-TWS-Python-Receiving-Market-Data-Study-Notes.pdf
# Market data and historical data
# Stock, forex and options


from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.order import *
from threading import Timer
import pandas as pd
from time import sleep

ticker_id = 0
output_df = pd.DataFrame()


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.done = None
        self.output_df = pd.DataFrame()

    def error(self, req_id, error_code, error_string):
        if req_id > -1:
            print("Error: ", req_id, " ", error_code, " ", error_string)

    def tickPrice(self, req_id, tick_type, price, attrib):
        # print("Id:", req_id, "Type:", TickTypeEnum.to_str(tick_type), "Price:", price, end=' ')
        global ticker_id, output_df
        ticker_id = req_id
        self.output_df['Symbol'] = None
        if TickTypeEnum.to_str(tick_type) == 'BID' or TickTypeEnum.to_str(tick_type) == 'ASK' or TickTypeEnum.to_str(tick_type) == 'LAST':
            self.output_df.loc[ticker_id, TickTypeEnum.to_str(tick_type)] = price

    # def contractDetails(self, req_id, contract_details):
    #     print("Id:", req_id, contract_details)
    #
    # def contractDetailsEnd(self, req_id):
    #     pass

    def stop(self):
        self.done = True
        self.disconnect()

    # def historicalData(self, req_id, bar):
    #     # print("Id", reqId, bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume)
    #     self.data.append(vars(bar))
    #     self.df = pd.DataFrame(self.data)
    #     self.df['date'] = pd.to_datetime(self.df['date'])
    #     self.df.set_index('date', inplace=True)
    #
    # def next_valid_id(self, order_id):
    #     self.nextOrderId = order_id
    #     self.start()
    #
    # def order_status(self, order_id, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
    #     print("OrderStatus. Id: ", order_id, ", Status: ", status, ", Filled: ", filled, ", Remaining: ", remaining, ", LastFillPrice: ", lastFillPrice)
    #
    # def open_order(self, order_id, contract, order, order_state):
    #     print("OpenOrder. ID:", order_id, contract.symbol, contract.secType, "@", contract.exchange, ":", order.action, order.orderType, order.totalQuantity, order_state.status)
    #
    # def exec_details(self, req_id, contract, execution):
    #     print("ExecDetails. ", req_id, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)


def create_contract(symbol, sec_type='STK', exchange='SMART', currency='USD'):
    # stk_aapl = create_contract('AAPL')
    # frx_eurusd = create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.exchange = exchange
    contract.currency = currency
    return contract
#
#
# def create_options_contract(symbol, exp, strike, right, exchange='SMART', currency='USD', multiplier='100'):
#     # opt_spy = create_options_contract('SPY', '20210319', '400', 'C')
#     contract = Contract()
#     contract.symbol = symbol
#     contract.lastTradeDateOrContractMonth = exp
#     contract.strike = strike
#     contract.right = right
#     contract.secType = 'OPT'
#     contract.exchange = exchange
#     contract.currency = currency
#     contract.multiplier = multiplier
#     return contract
#

# def create_market_order(action, quantity):
#     order = Order()
#     order.action = action  # BUY/SELL
#     order.orderType = 'MKT'
#     order.totalQuantity = quantity
#     # order.transmit = True
#
#
# def send_order(order_id, contract, order):
#     app = TestApp()
#     app.connect("127.0.0.1", 7496, 12)
#
#     app.placeOrder(order_id, contract, order)
#     print('Order sent')
#
#     Timer(3, app.stop).start()
#     app.run()
#
#
# def get_contract_details(contract):
#     app = TestApp()
#     app.connect("127.0.0.1", 7496, 12)
#     ticker_id = 1
#
#     # Desc: ContractDetails(Contract,marketName,minTick,orderTypes,validExchanges,underConId,longName,contractMonth,industry,category,subcategory,timeZoneId,tradingHours,liquidHours,evRule,evMultiplier,aggGroup,tagvalue
#     app.reqContractDetails(ticker_id, contract)
#
#     Timer(2, app.stop).start()
#     app.run()

#
# def get_market_price(ticker_id, contract):
#     # Print current market bid, ask, close
#     # app = TestApp()
#     # app.connect("127.0.0.1", 7496, 12)
#     # ticker_id = 1
#
#     # Desc: reqMarketDataType: 1 (default)- live data, 2- frozen live data, 3- delayed data, 4- delayed frozen
#     app.reqMarketDataType(2)
#     # Desc: reqMktData(tickerId, contract, genericTickList, snapshot, regulatorySnaphsot, mktDataOptions)
#     app.reqMktData(ticker_id, contract, '', False, False, [])
#
#     Timer(10, app.stop).start()
#     app.run()
#
#     return contract.symbol, bid, ask, close


# def get_historical_data(ticker_id, contract, duration, size):
#     # Historical data
#     # app = TestApp()
#     # app.connect("127.0.0.1", 7496, 12)
#     # ticker_id = 1
#
#     # Desc: reqHistoricalData (tickerId, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions
#     app.reqHistoricalData(ticker_id, contract, '', duration, size, 'TRADES', False, 1, False, [])
#
#     Timer(2, app.stop).start()
#     app.run()
#
#     app.df.pop('barCount')
#     app.df.pop('average')
#
#     return app.df
