# market_shock.py
import threading
import random
import time

class MarketShockManager(threading.Thread):
    def __init__(self, order_book, interval=10):
        super().__init__()
        self.order_book = order_book
        self.interval = interval  # Time between shocks
        self.stocks = [f"STOCK{i}" for i in range(1, 20)]
        self.running = True

    def run(self):
        while self.running:
            time.sleep(self.interval)
            shock_stock = random.choice(self.stocks)
            shock_type = random.choice(["crash", "boom"])
            print(f"\n🚨 [MARKET SHOCK] {shock_stock} experiences a {shock_type.upper()}!")

            # Apply effect to the order book (simplified)
            affected_orders = []
            for order in self.order_book.orders:
                if order["stock"] == shock_stock:
                    if shock_type == "crash" and order["action"] == "buy":
                        order["price"] = max(1, int(order["price"] * 0.5))  # drop price
                    elif shock_type == "boom" and order["action"] == "sell":
                        order["price"] = int(order["price"] * 1.5)  # raise price
                    affected_orders.append(order)

            if affected_orders:
                print(f"📈 Updated orders for {shock_stock}:")
                for order in affected_orders:
                    print(f"  ↪ {order}")
            else:
                print(f"⚠ No active orders for {shock_stock} affected.")

    def stop(self):
        self.running = False
