from multiprocessing import Process, Queue
import time
import random

class Exchange(Process):
    def __init__(self, exchange_id, queue):
        super().__init__()
        self.exchange_id = exchange_id
        self.queue = queue

    def run(self):
        print(f"[Exchange {self.exchange_id}] Started")
        while True:
            if not self.queue.empty():
                # Simulate random network failure (for CAP)
                if random.random() < 0.2:  # 10% chance of failure
                    print(f"\033[91m[Exchange {self.exchange_id}] Network failure, unable to process trade.\033[0m")
                    time.sleep(2)  # Simulate recovery time after failure
                    continue

                trade = self.queue.get()
                print(f"\033[94m[Exchange {self.exchange_id}] Executing Trade: {trade}\033[0m")
                time.sleep(1)  # Simulate processing delay 
