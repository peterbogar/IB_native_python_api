# Native IB API
# Based from https://cdcdyn.interactivebrokers.com/webinars/TA-2018-TWS-Python-Receiving-Market-Data-Study-Notes.pdf

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
        print("Tick Price. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price, end=' ')

    def tickSize(self, reqId, tickType, size):
        print("Tick Size. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Size:", size)

    def historicalData(self, reqId, bar):
        print("HistoricalData. ", reqId, " Date:", bar.date, "Open:", bar.open, "High:", bar.high, "Low:", bar.low, "Close:", bar.close, "Volume:", bar.volume, "Count:", bar.barCount, "WAP:", bar.average)


def main():
    app = TestApp()
    app.connect("127.0.0.1", 7496, 12)
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NASDAQ"
    app.reqMarketDataType(2)
    app.reqMktData(1, contract, "", False, False, [])

    # contract.symbol = "EUR"
    # contract.secType = "CASH"
    # contract.exchange = "IDEALPRO"
    # contract.currency = "USD"
    # app.reqHistoricalData(1, contract, "", "1 D", "1 min", "MIDPOINT", 0, 1, False, [])

    app.run()


if __name__ == "__main__":
    main()
