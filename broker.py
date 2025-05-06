# broker.py
import threading
import random
import time

class Broker(threading.Thread):
    def __init__(self, broker_id, order_book, market):
        super().__init__()
        self.broker_id = broker_id
        self.order_book = order_book
        self.market = market  # reference to the Market for dynamic pricing
        self.running = True

    def run(self):
        while self.running:
            order = self.create_order()
            self.place_order(order)
            time.sleep(random.randint(1, 5))

    def create_order(self):
        stock = f"STOCK{random.randint(1, 5)}"
        base_price = self.market.get_price(stock)
        action = random.choice(['buy', 'sell'])

        # Simulate price bias: buyers may bid higher, sellers may undercut
        if action == 'buy':
            price = base_price + random.randint(0, 10)
        else:  # sell
            price = base_price - random.randint(0, 10)

        order = {
            'broker_id': self.broker_id,
            'action': action,
            'stock': stock,
            'price': max(1, price),
            'volume': random.randint(10, 100)
        }

        print(f"[Broker {self.broker_id}] Placing {action.upper()} order for {stock} at {order['price']} ({order['volume']} shares)")
        return order

    def place_order(self, order):
        self.order_book.add_order(order)

    def stop(self):
        self.running = False
