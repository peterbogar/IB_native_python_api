from ibapi.wrapper import *
from ibapi.client import *
from ibapi.contract import *
from ibapi.order import *
from threading import Thread
import queue
import datetime
import time
# import math


availableFunds = 0
buyingPower = 0
positionsDict = {}
stockPrice = 1000000


class TestWrapper(EWrapper):

    # error handling methods
    def init_error(self):
        error_queue = queue.Queue()
        self.my_errors_queue = error_queue

    def is_error(self):
        error_exist = not self.my_errors_queue.empty()
        return error_exist

    def get_error(self, timeout=6):
        if self.is_error():
            try:
                return self.my_errors_queue.get(timeout=timeout)
            except queue.Empty:
                return None
        return None

    def error(self, id, errorCode, errorString):
        # Overrides the native method
        errormessage = "IB returns an error with %d errorcode %d that says %s" % (id, errorCode, errorString)
        self.my_errors_queue.put(errormessage)

    # time handling methods
    def init_time(self):
        time_queue = queue.Queue()
        self.my_time_queue = time_queue
        return time_queue

    def currentTime(self, server_time):
        # Overriden method
        self.my_time_queue.put(server_time)

    # ID handling methods
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        logging.debug("setting nextValidOrderId: %d", orderId)
        self.nextValidOrderId = orderId

    def nextOrderId(self):
        oid = self.nextValidOrderId
        self.nextValidOrderId += 1
        return oid

    # Account details handling methods
    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency:str):
        super().accountSummary(reqId, account, tag, value, currency)
        print("Acct Summary. ReqId:", reqId, "Acct:", account, "Tag: ", tag, "Value:", value, "Currency:", currency)
        if tag == "AvailableFunds":
            global availableFunds
            availableFunds = value
        if tag == "BuyingPower":
            global buyingPower
            buyingPower = value

    def accountSummaryEnd(self, reqId: int):
        super().accountSummaryEnd(reqId)
        print("AccountSummaryEnd. Req Id: ", reqId)

    def account_update(self):
        self.reqAccountSummary(9001, "All", "TotalCashValue, BuyingPower, AvailableFunds")

    # Position handling methods
    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        super().position(account, contract, position, avgCost)
        positionsDict[contract.symbol] = {'positions' : position, 'avgCost' : avgCost}
        print("Position.", account, "Symbol:", contract.symbol, "SecType:", contract.secType, "Currency:", contract.currency,"Position:", position, "Avg cost:", avgCost)

    def position_update(self):
        self.reqPositions()



    # Market Price handling methods
    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("Tick Price. Ticker Id:", reqId, "tickType:", tickType, "Price:", price, "CanAutoExecute:", attrib.canAutoExecute, "PastLimit:", attrib.pastLimit, end=' ')
        global stockPrice

        # Declares that we want stockPrice to be treated as a global global stockPriceBool
        # A boolean flag that signals if the price has been updated
        # Use tickType 4 (Last Price) if you are running during the market day
        if tickType == 4:
            print("\nParsed Tick Price: " + str(price))
            stockPrice = price
            stockPriceBool = True

        # Uses tickType 9 (Close Price) if after market hours
        elif tickType == 9:
            print("\nParsed Tick Price: " + str(price))
            stockPrice = price
            stockPriceBool = True

    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        super().tickSize(reqId, tickType, size)
        print("Tick Size. Ticker Id:", reqId, "tickType:", tickType, "Size:", size)

    def tickString(self, reqId: TickerId, tickType: TickType, value: str):
        super().tickString(reqId, tickType, value)
        print("Tick string. Ticker Id:", reqId, "Typxe:", tickType, "Value:", value)

    def tickGeneric(self, reqId: TickerId, tickType: TickType, value: float):
        super().tickGeneric(reqId, tickType, value)
        print("Tick Generic. Ticker Id:", reqId, "tickType:", tickType, "Value:", value)

    def price_update(self, Contract, tickerid):
        self.reqMktData(tickerid, Contract, "", False, False, [])
        return tickerid







class TestClient(EClient):

    def __init__(self, wrapper):
        # Set up with a wrapper inside
        EClient.__init__(self, wrapper)

    def server_clock(self):
        # print("Asking server for Unix time")
        # Creates a queue to store the time
        time_storage = self.wrapper.init_time()
        # Sets up a request for unix time from the Eclient
        self.reqCurrentTime()
        # Specifies a max wait time if there is no connection
        max_wait_time = 10

        try:
            requested_time = time_storage.get(timeout=max_wait_time)
        except queue.Empty:
            print("The queue was empty or max time reached")
            requested_time = None

        while self.wrapper.is_error():
            # print("Error:")
            print(self.get_error(timeout=5))
        return requested_time


class TestApp(TestWrapper, TestClient):

    #Intializes our main classes
    def __init__(self, ipaddress, portid, clientid):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)
        # Connects to the server with the ipaddress, portid, and clientId specified in the program
        self.connect(ipaddress, portid, clientid)
        #Initializes the threading
        thread = Thread(target = self.run)
        thread.start()
        setattr(self, "_thread", thread)
        #Starts listening for errors
        self.init_error()



def contractCreate():
    # Fills out the contract object
    contract1 = Contract()
    contract1.symbol = "AAPL"
    contract1.secType = "STK"
    contract1.currency = "USD"
    # In the API side, NASDAQ is always defined as ISLAND in the exchange field
    contract1.exchange = "SMART"
    contract1.PrimaryExch = "NYSE"
    return contract1


if __name__ == '__main__':
    app = TestApp("127.0.0.1", 7496, 12)

    print("Server time: ", app.server_clock())
    print('Next ID: ', app.nextOrderId())
    print()
    app.account_update()
    time.sleep(3)
    print()
    app.position_update()
    time.sleep(3)
    print()

    # Call client methods to gather most recent information
    contractObject = contractCreate()
    # orderObject = orderCreate()
    app.price_update(contractObject, app.nextOrderId())
    nextID = app.nextOrderId()
    time.sleep(2)
    print("Global Tick Price" + str(stockPrice))
    # Print statement to confirm correct values
    print("Next valid id: " + str(nextID))
    print("Buying Power: " + str(buyingPower))
    print("Available Funds: " + str(availableFunds))
    # Place order
    # app.placeOrder(nextID, contractObject, orderObject)

    time.sleep(3)
    app.disconnect()
