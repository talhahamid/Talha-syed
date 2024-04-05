# from trading_framework.execution_client import ExecutionClient
# from trading_framework.price_listener import PriceListener


# class LimitOrderAgent(PriceListener):

#     def __init__(self, execution_client: ExecutionClient) -> None:
#         """

#         :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
#         """
#         super().__init__()

#     def on_price_tick(self, product_id: str, price: float):
#         # see PriceListener protocol and readme file
#         pass


class LimitOrderAgent:
    def __init__(self, execution_client):
        self.execution_client = execution_client
        self.orders = []

    def price_tick(self, product_id: str, price: float):
        if product_id == 'IBM' and price < 100:
            self.execution_client.execute_order('BUY', 'IBM', 1000, price)

    def add_order(self, action: str, product_id: str, amount: int, limit: float):
        self.orders.append((action, product_id, amount, limit))

    def execute_held_orders(self, current_price: float):
        for order in self.orders:
            action, product_id, amount, limit = order
            if action == 'BUY' and current_price <= limit:
                self.execution_client.execute_order(action, product_id, amount, current_price)
                self.orders.remove(order)
            elif action == 'SELL' and current_price >= limit:
                self.execution_client.execute_order(action, product_id, amount, current_price)
                self.orders.remove(order)


if __name__ == "__main__":
    class MockExecutionClient:
        def execute_order(self, action, product_id, amount, price):
            print(f"Executing order: {action} {amount} shares of {product_id} at {price}")

    execution_client = MockExecutionClient()
    agent = LimitOrderAgent(execution_client)

    
    agent.price_tick('IBM', 99)  
    agent.price_tick('IBM', 101)  

    
    agent.add_order('BUY', 'IBM', 500, 98)
    agent.add_order('SELL', 'IBM', 500, 102)

    agent.execute_held_orders(98)  
    agent.execute_held_orders(101)  
    agent.execute_held_orders(102)  
