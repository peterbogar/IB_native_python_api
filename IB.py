# Native IB API
# Based from https://cdcdyn.interactivebrokers.com/webinars/TA-2018-TWS-Python-Receiving-Market-Data-Study-Notes.pdf
# Market data and historical data
# Stock and forex


from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from threading import Timer
from time import sleep


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(self, reqId, tickType, price, attrib):
        print("Id:", reqId, "Type:", TickTypeEnum.to_str(tickType), "Price:", price, end=' ')

    # def tickSize(self, reqId, tickType, size):
    #     print("Tick Size. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Size:", size)

    def historicalData(self, reqId, bar):
        print("Id", reqId, bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:")

    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails)

    def contractDetailsEnd(self, reqId):
        print("\ncontractDetails End\n")

    # def start(self):
    #     contract = Contract()
    #     contract.symbol = "AAPL"
    #     contract.secType = "STK"
    #     contract.exchange = "SMART"
    #     contract.currency = "USD"
    #     contract.primaryExchange = "NASDAQ"
    #     order = Order()
    #     order.action = "BUY"
    #     order.totalQuantity = 10
    #     order.orderType = "LMT"
    #     order.lmtPrice = 185
    #     self.placeOrder(self.nextOrderId, contract, order)

    def stop(self):
        self.done = True
        self.disconnect()


def create_contract(symbol, sec_type='STK', exchange='SMART', currency='USD'):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.exchange = exchange
    contract.currency = currency
    return contract
def create_options_contract(symbol, exp, strike, right, exchange='SMART', currency='USD', multiplier='100'):
    contract = Contract()
    contract.symbol = symbol
    contract.lastTradeDateOrContractMonth = exp
    contract.strike = strike
    contract.right = right
    contract.secType = 'OPT'
    contract.exchange = exchange
    contract.currency = currency
    contract.multiplier = multiplier
    return contract


def main():
    app = TestApp()
    app.connect("127.0.0.1", 7496, 12)
    ticker_id = 1

    # Create contract
    stk_aapl = create_contract('AAPL')
    frx_eurusd = create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
    opt_spy = create_options_contract('SPY', '20210319', '400', 'C')

    # Contract detail
    # ContractDetails(Contract,marketName,minTick,orderTypes,validExchanges,underConId,longName,contractMonth,industry,category,subcategory,timeZoneId,tradingHours,liquidHours,evRule,evMultiplier,aggGroup,tagvalue
    # app.reqContractDetails(ticker_id, opt_spy)

    # Market data
    # reqMarketDataType: 1 (default)- live data, 2- frozen live data, 3- delayed data, 4- delayed frozen
    app.reqMarketDataType(2)
    # reqMktData(tickerId, contract, genericTickList, snapshot, regulatorySnaphsot, mktDataOptions)
    # app.reqMktData(ticker_id, opt_spy, '', True, False, [])

    # Historical data
    # reqHistoricalData (tickerId, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions
    app.reqHistoricalData(ticker_id, opt_spy, '', '2 D', '1 hour', 'TRADES', False, 1, False, [])

    Timer(2, app.stop).start()
    app.run()


if __name__ == "__main__":
    main()
