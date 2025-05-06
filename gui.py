import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from queue import Empty
from collections import defaultdict
import datetime
import threading

class AnalyticsGUI(threading.Thread):
    def __init__(self, analytics_queue):
        super().__init__(daemon=True)  # Makes the thread stop with main program
        self.analytics_queue = analytics_queue
        self.trade_count = 0
        self.volume_by_stock = defaultdict(int)
        self.trade_log = []

    def run(self):
        self.root = tk.Tk()
        self.root.title("📊 MarketSim - Real-time Analytics")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e1e")

        self.setup_widgets()
        self.update_gui()
        self.root.mainloop()

    def setup_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Arial", 12))
        style.configure("Header.TLabel", font=("Arial", 16, "bold"), foreground="#00ffcc")

        self.header = ttk.Label(self.root, text="📈 MarketSim Real-Time Dashboard", style="Header.TLabel")
        self.header.pack(pady=10)

        self.trade_label = ttk.Label(self.root, text="Total Trades: 0")
        self.trade_label.pack()

        # Set up Matplotlib Figure
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.fig.patch.set_facecolor('#1e1e1e')
        self.ax.set_facecolor('#2e2e2e')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        # Trade history
        self.log_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.log_frame.pack(pady=10)
        self.log_label = ttk.Label(self.log_frame, text="Trade Log:")
        self.log_label.pack()
        self.trade_history = tk.Text(self.log_frame, height=8, width=80, bg="#111", fg="white")
        self.trade_history.pack()

    def update_gui(self):
        try:
            while True:
                trade = self.analytics_queue.get_nowait()
                self.trade_count += 1
                self.volume_by_stock[trade['stock']] += trade['volume']
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                self.trade_log.append(f"[{timestamp}] {trade['stock']} x {trade['volume']}")
        except Empty:
            pass

        self.trade_label.config(text=f"Total Trades: {self.trade_count}")

        # Update Matplotlib bar chart
        self.ax.clear()
        stocks = list(self.volume_by_stock.keys())
        volumes = list(self.volume_by_stock.values())
        self.ax.bar(stocks, volumes, color="#00ffcc")
        self.ax.set_title("Volume Traded per Stock", color="white")
        self.ax.tick_params(colors="white")
        self.canvas.draw()

        # Update trade history
        self.trade_history.delete(1.0, tk.END)
        for line in self.trade_log[-10:]:
            self.trade_history.insert(tk.END, line + "\n")

        self.root.after(1000, self.update_gui)
