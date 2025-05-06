from orderbook import OrderBook
from broker import Broker
from exchange import Exchange
from multiprocessing import Queue
import time
from market import Market
import sys
from gui import AnalyticsGUI
from analytics import Analytics

analytics_queue = Queue()
analytics = Analytics(analytics_queue)

def run_simulation():
    
    order_book = OrderBook(analytics_queue)

    exchange_queues = [Queue() for _ in range(5)]
    exchanges = [Exchange(i, exchange_queues[i]) for i in range(5)]
    for ex in exchanges:
        ex.start()

    order_book.set_exchanges(exchange_queues)

    market = Market(stocks=[f"STOCK{i}" for i in range(1, 6)])
    market.start()

    brokers = [Broker(i + 1, order_book, market) for i in range(1, 4)]
    for broker in brokers:
        broker.start()

    time.sleep(50)

    for broker in brokers:
        broker.stop()
        broker.join()

    market.stop()
    market.join()

    for ex in exchanges:
        ex.stop()
        ex.join()

    analytics.collect()
    analytics.print_summary()

    print("\n✅ Simulation complete.")
    sys.exit(0)

if __name__ == "__main__":
    gui = AnalyticsGUI(analytics_queue=analytics_queue)
    gui.start()
    run_simulation()
