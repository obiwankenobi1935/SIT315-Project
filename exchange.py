from multiprocessing import Process, Queue
import time
import random

EXCHANGE_NAMES = ["NYSE", "NASDAQ", "LSE", "JPX", "SSE"]

class Exchange(Process):
    def __init__(self, exchange_id, queue):
        super().__init__()
        self.exchange_id = exchange_id
        self.queue = queue
        self.name = EXCHANGE_NAMES[exchange_id % len(EXCHANGE_NAMES)]
        self.running = True

    def run(self):
        print(f"[{self.name}] Started")
        while self.running:
            if not self.queue.empty():
                message = self.queue.get()

                # 🛑 Check for shutdown command
                if message == "STOP":
                    print(f"\033[93m[{self.name}] Shutting down gracefully.\033[0m")
                    break

                # Simulate random network failure (for CAP)
                if random.random() < 0.2:
                    print(f"\033[91m[{self.name}] Network failure, unable to process trade.\033[0m")
                    time.sleep(2)
                    continue

                print(f"\033[94m[{self.name}] Executing Trade: {message}\033[0m")
                time.sleep(1)

    def stop(self):
        self.running = False
