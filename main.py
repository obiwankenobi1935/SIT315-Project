from orderbook import OrderBook
from broker import Broker
from exchange import Exchange
from multiprocessing import Queue
import time
from market import Market

# Create order book
order_book = OrderBook()

# Setup exchanges (add random failover behavior for simulating partition tolerance)
exchange_queues = [Queue() for _ in range(2)]
exchanges = [Exchange(i+1, exchange_queues[i]) for i in range(2)]

# Start exchanges
for ex in exchanges:
    ex.start()

# Tell the order book about exchange queues
order_book.set_exchanges(exchange_queues)

market = Market(stocks=[f"STOCK{i}" for i in range(1, 6)])
market.start()

# Start brokers
brokers = [Broker(i+1, order_book, market) for i in range(1, 4)]
for broker in brokers:
    broker.start()

# Let it run for a while
time.sleep(30)
print("Simulation complete.")
