import threading
import random 
import time

class Market(threading.Thread):
    def __init__(self, stocks):
        super().__init__()
        self.stocks = {stock: random.randint(50, 100) for stock in stocks}
        self.lock = threading.Lock()
        self.running = True
        self.shock_chance = 0.2  # 20% chance to trigger a shock every cycle

    def run(self):
        while self.running:
            time.sleep(3)
            with self.lock:
                for stock in self.stocks:
                    change = random.randint(-2, 2)
                    self.stocks[stock] = max(1, self.stocks[stock] + change)

                # Simulate a shock
                if random.random() < self.shock_chance:
                    self.apply_market_shock()

    def get_price(self, stock):
        with self.lock:
            return self.stocks.get(stock, 100)

    def apply_market_shock(self):
        stock = random.choice(list(self.stocks.keys()))
        boom = random.choice([True, False])
        magnitude = random.randint(5, 15)

        if boom:
            self.stocks[stock] += magnitude
            print(f"\n🚨 [MARKET SHOCK] {stock} experiences a {self.color_text('BOOM', 'green')}! 📈 (+{magnitude})")
        else:
            self.stocks[stock] = max(1, self.stocks[stock] - magnitude)
            print(f"\n🚨 [MARKET SHOCK] {stock} experiences a {self.color_text('CRASH', 'red')}! 📉 (-{magnitude})")

    def color_text(self, text, color):
        colors = {
            'green': "\033[92m",
            'red': "\033[91m",
            'reset': "\033[0m"
        }
        return f"{colors[color]}{text}{colors['reset']}"

    def stop(self):
        self.running = False
