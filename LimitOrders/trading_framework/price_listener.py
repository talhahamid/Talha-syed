from typing import Protocol

class PriceListener(Protocol):

    def on_price_tick(self, product_id: str, price: float):
        """
        invoked on market data change
        :param product_id: id of the product that has a price change
        :param price: the current market price of the product
        :return: None
        """
        ...

class LimitOrderAgent(PriceListener):
    def __init__(self):
        self.orders = []

    def on_price_tick(self, product_id: str, price: float):
        if product_id == 'IBM' and price < 100:
            print(f"Buying 1000 shares of IBM at {price}")

    def add_order(self, action: str, product_id: str, amount: int, limit: float):
        self.orders.append((action, product_id, amount, limit))

    def execute_held_orders(self, current_price: float):
        for order in self.orders:
            action, product_id, amount, limit = order
            if action == 'BUY' and current_price <= limit:
                print(f"Executing BUY order: {amount} shares of {product_id} at {current_price}")
                self.orders.remove(order)
            elif action == 'SELL' and current_price >= limit:
                print(f"Executing SELL order: {amount} shares of {product_id} at {current_price}")
                self.orders.remove(order)


if __name__ == "__main__":
    agent = LimitOrderAgent()

    agent.on_price_tick('IBM', 99) 
    agent.on_price_tick('IBM', 101) 

    agent.add_order('BUY', 'IBM', 500, 98)
    agent.add_order('SELL', 'IBM', 500, 102)

    agent.execute_held_orders(98)  
    agent.execute_held_orders(101)  
    agent.execute_held_orders(102) 
