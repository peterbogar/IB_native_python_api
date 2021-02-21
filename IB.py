# Native IB API
# Based from https://cdcdyn.interactivebrokers.com/webinars/TA-2018-TWS-Python-Receiving-Market-Data-Study-Notes.pdf
# Market data and historical data
# Stock and forex


from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum


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


def create_contract(symbol, sec_type='STK', exchange='SMART', currency='USD'):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.exchange = exchange
    contract.currency = currency
    return contract


def main():
    app = TestApp()
    app.connect("127.0.0.1", 7496, 12)
    ticker_id = 1

    # Create contract
    contract_aapl = create_contract('AAPL')
    contract_eurusd = create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')

    # Market data
    # reqMarketDataType: 1 (default)- live data, 2- frozen live data, 3- delayed data, 4- delayed frozen
    app.reqMarketDataType(2)
    # reqMktData(tickerId, contract, genericTickList, snapshot, regulatorySnaphsot, mktDataOptions)
    app.reqMktData(ticker_id, contract_aapl, '', True, False, [])

    # Historical data
    # reqHistoricalData (tickerId, contract, endDateTime, durationStr, barSizeSetting, whatToShow, useRTH, formatDate, keepUpToDate, chartOptions
    # app.reqHistoricalData(ticker_id, contract_aapl, '', '2 D', '1 hour', 'TRADES', False, 1, False, [])

    app.run()


if __name__ == "__main__":
    main()
