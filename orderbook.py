import threading

# ANSI color codes
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"

class OrderBook:
    def __init__(self):
        self.orders = []
        self.exchanges = []
        self.lock = threading.Lock()

    def set_exchanges(self, exchange_queues):
        self.exchanges = exchange_queues

    def add_order(self, order):
        with self.lock:
            action_color = GREEN if order['action'] == 'buy' else RED
            print(f"\n{BOLD}📥 [NEW ORDER] Broker {order['broker_id']} placed a {action_color}{order['action'].upper()}{RESET}{BOLD} order:{RESET}")
            print(f"   🧾 {order['volume']} shares of {order['stock']} @ ${order['price']}")
            self.orders.append(order)
            self.match_orders()

    def match_orders(self):
        matched = False
        i = 0
        while i < len(self.orders):
            j = i + 1
            while j < len(self.orders):
                buy = self.orders[i]
                sell = self.orders[j]

                if buy['action'] == 'buy' and sell['action'] == 'sell':
                    if buy['stock'] == sell['stock'] and buy['price'] >= sell['price']:
                        print(f"\n{GREEN}{BOLD}🟢 [TRADE EXECUTED]{RESET}")
                        print(f"  {CYAN}📈 BUYER : Broker {buy['broker_id']} -> {buy['volume']} shares of {buy['stock']} @ ₹{buy['price']}{RESET}")
                        print(f"  {MAGENTA}📉 SELLER: Broker {sell['broker_id']} -> {sell['volume']} shares of {sell['stock']} @ ₹{sell['price']}{RESET}")
                        print(f"  ✅ Volume Traded: {min(buy['volume'], sell['volume'])} shares\n")

                        trade_info = {
                            'stock': buy['stock'],
                            'price': sell['price'],
                            'volume': min(buy['volume'], sell['volume']),
                            'buyer': buy['broker_id'],
                            'seller': sell['broker_id']
                        }

                        if self.exchanges:
                            from random import choice
                            choice(self.exchanges).put(trade_info)
                            print(f"  📤 Sent trade info to exchange.\n")

                        self.orders.remove(buy)
                        self.orders.remove(sell)
                        matched = True
                        i = -1  # Restart after match
                        break
                j += 1
            i += 1

        if not matched:
            print(f"{YELLOW}🔍 [MATCHING] No matching orders found at this time.{RESET}")
