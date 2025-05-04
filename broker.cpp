#include <iostream>
#include <thread>
#include <vector>
#include <cstdlib>
#include <ctime>

class OrderBook {
public:
    void add_order(const std::string& broker_id, const std::string& action, const std::string& stock, int price, int volume) {
        // Simulate adding order to the order book
        std::cout << "Broker " << broker_id << " places order: " 
                  << action << " " << stock << " at " << price << " for " << volume << " shares.\n";
    }
};

class Broker {
public:
    Broker(int broker_id, OrderBook* order_book)
        : broker_id_(broker_id), order_book_(order_book) {}

    void place_order() {
        // Randomly generate an order
        std::string action = (rand() % 2 == 0) ? "buy" : "sell";
        std::string stock = "STOCK" + std::to_string(rand() % 10 + 1);
        int price = rand() % 500 + 10;
        int volume = rand() % 100 + 1;
        
        order_book_->add_order(std::to_string(broker_id_), action, stock, price, volume);
    }

    void operator()() {
        while (true) {
            place_order();
            std::this_thread::sleep_for(std::chrono::seconds(rand() % 5 + 1));  // Random delay for broker activity
        }
    }

private:
    int broker_id_;
    OrderBook* order_book_;
};

int main() {
    srand(time(0));  // Seed for random number generation
    OrderBook order_book;

    std::vector<std::thread> brokers;
    
    // Create and start 3 broker threads
    for (int i = 0; i < 3; ++i) {
        brokers.push_back(std::thread(Broker(i + 1, &order_book)));
    }

    // Let the threads run for 10 seconds
    std::this_thread::sleep_for(std::chrono::seconds(10));
    
    // Join all broker threads
    for (auto& broker : brokers) {
        broker.join();
    }

    return 0;
}
