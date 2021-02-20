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

    time.sleep(2)
    app.disconnect()
