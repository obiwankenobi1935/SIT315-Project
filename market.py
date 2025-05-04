import threading
import random 
import time

class Market(threading.Thread):
    def __init__(self, stocks):
        super().__init__()
        self.stocks = {stock: random.randint(50, 100) for stock in stocks}
        self.lock = threading.Lock()

    def run(self):
        while True: 
            time.sleep(3)
            with self.lock:
                for stock in self.stocks:
                    change = random.randint(-5, 5)
                    self.stocks[stock] = max(1, self.stocks[stock] + change)
                    if abs(change) >= 4:
                        print(f"💥 Market Shock: {stock} {'↑' if change > 0 else '↓'} by {change} → {self.stocks[stock]}")

    def get_price(self, stock):
        with self.lock:
            return self.stocks.get(stock, 100)