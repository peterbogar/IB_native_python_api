# Native IB API
# Based from https://cdcdyn.interactivebrokers.com/webinars/TA-2018-TWS-Python-Receiving-Market-Data-Study-Notes.pdf
# Market data and historical data
# Stock, forex and options


from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from threading import Timer
import pandas as pd


bid = 0
ask = 0
close = 0


class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []
        self.df = pd.DataFrame()

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(self, reqId, tickType, price, attrib):
        # print("Id:", reqId, "Type:", TickTypeEnum.to_str(tickType), "Price:", price, end=' ')
        global bid, ask, close
        if TickTypeEnum.to_str(tickType) == 'BID':
            bid = price
        if TickTypeEnum.to_str(tickType) == 'ASK':
            ask = price
        if TickTypeEnum.to_str(tickType) == 'CLOSE':
            close = price

    # def tickSize(self, reqId, tickType, size):
    #     print("Tick Size. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Size:", size)

    def contractDetails(self, reqId, contractDetails):
        print("Id:", reqId, contractDetails)

    def contractDetailsEnd(self, reqId):
        pass

    def stop(self):
        self.done = True
        self.disconnect()

    def historicalData(self, reqId, bar):
        # print("Id", reqId, bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume)
        self.data.append(vars(bar))
        self.df = pd.DataFrame(self.data)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df.set_index('date', inplace=True)


def create_contract(symbol, sec_type='STK', exchange='SMART', currency='USD'):
    # stk_aapl = create_contract('AAPL')
    # frx_eurusd = create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.exchange = exchange
    contract.currency = currency
    return contract


def create_options_contract(symbol, exp, strike, right, exchange='SMART', currency='USD', multiplier='100'):
    # opt_spy = create_options_contract('SPY', '20210319', '400', 'C')
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


def get_contract_details(contract):
    app = TestApp()
    app.connect("127.0.0.1", 7496, 12)
    ticker_id = 1

    # Desc: ContractDetails(Contract,marketName,minTick,orderTypes,validExchanges,underConId,longName,contractMonth,industry,category,subcategory,timeZoneId,tradingHours,liquidHours,evRule,evMultiplier,aggGroup,tagvalue
    app.reqContractDetails(ticker_id, contract)

    Timer(2, app.stop).start()
    app.run()


def get_market_price(contract):
    # Print current market bid, ask, close
    app = TestApp()
    app.connect("127.0.0.1", 7496, 12)
    ticker_id = 1

    # Desc: reqMarketDataType: 1 (default)- live data, 2- frozen live data, 3- delayed data, 4- delayed frozen
    app.reqMarketDataType(2)
    # Desc: reqMktData(tickerId, contract, genericTickList, snapshot, regulatorySnaphsot, mktDataOptions)
    app.reqMktData(ticker_id, contract, '', True, False, [])

    Timer(2, app.stop).start()
    app.run()

    return contract.symbol, bid, ask, close


def get_historical_data(contract, duration, size):
    # Historical data
    app = TestApp()
    app.connect("127.0.0.1", 7496, 12)
    ticker_id = 1

    # Desc: reqHistoricalData (tickerId, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions
    app.reqHistoricalData(ticker_id, contract, '', duration, size, 'TRADES', False, 1, False, [])

    Timer(2, app.stop).start()
    app.run()

    app.df.pop('barCount')
    app.df.pop('average')

    return app.df
