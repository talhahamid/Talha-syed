from typing import Protocol


class ExecutionException(Exception):
    pass


class ExecutionClient(Protocol):

    def buy(self, product_id: str, amount: int):
        """
        Execute a buy order, throws ExecutionException on failure
        :param product_id: the product to buy
        :param amount: the amount to buy
        :return: None
        """
        ...

    def sell(self, product_id: str, amount: int):
        """
        Execute a sell order, throws ExecutionException on failure
        :param product_id: the product to sell
        :param amount: the amount to sell
        :return: None
        """
        ...


class LimitOrderAgent:
    def __init__(self, execution_client: ExecutionClient):
        self.execution_client = execution_client
        self.orders = []

    def on_price_tick(self, product_id: str, price: float):
        if product_id == 'IBM' and price < 100:
            try:
                self.execution_client.buy('IBM', 1000)
            except ExecutionException as e:
                print(f"Failed to execute buy order: {e}")

    def add_order(self, action: str, product_id: str, amount: int, limit: float):
        self.orders.append((action, product_id, amount, limit))

    def execute_held_orders(self, current_price: float):
        for order in self.orders:
            action, product_id, amount, limit = order
            if action == 'BUY' and current_price <= limit:
                try:
                    self.execution_client.buy(product_id, amount)
                    print(f"Executing BUY order: {amount} shares of {product_id} at {current_price}")
                    self.orders.remove(order)
                except ExecutionException as e:
                    print(f"Failed to execute buy order: {e}")
            elif action == 'SELL' and current_price >= limit:
                try:
                    self.execution_client.sell(product_id, amount)
                    print(f"Executing SELL order: {amount} shares of {product_id} at {current_price}")
                    self.orders.remove(order)
                except ExecutionException as e:
                    print(f"Failed to execute sell order: {e}")


if __name__ == "__main__":
    class MockExecutionClient:
        def buy(self, product_id: str, amount: int):
            print(f"Mock executing buy: {amount} shares of {product_id}")

        def sell(self, product_id: str, amount: int):
            print(f"Mock executing sell: {amount} shares of {product_id}")

    agent = LimitOrderAgent(MockExecutionClient())

    agent.on_price_tick('IBM', 99) 
    agent.on_price_tick('IBM', 101)  

    agent.add_order('BUY', 'IBM', 500, 98)
    agent.add_order('SELL', 'IBM', 500, 102)

    agent.execute_held_orders(98)  
    agent.execute_held_orders(101) 
    agent.execute_held_orders(102) 
