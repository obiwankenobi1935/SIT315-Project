from collections import defaultdict

class Analytics:
    def __init__(self, queue):
        self.queue = queue
        self.trades = []

    def collect(self):
        print("📊 [Analytics] Started collecting trade data...")
        while not self.queue.empty():
            trade = self.queue.get()
            self.trades.append(trade)

    def print_summary(self):
        summary = defaultdict(int)
        for trade in self.trades:
            summary[trade['stock']] += trade['volume']
        print("\n📈 Analytics Summary")
        print("-" * 30)
        for stock, volume in summary.items():
            print(f"{stock}: {volume} shares traded")
        print(f"Total trades: {len(self.trades)}")
