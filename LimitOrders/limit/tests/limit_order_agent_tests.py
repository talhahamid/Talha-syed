import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

class MockExecutionClient:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def buy(self, product_id, amount, price):
        self.buy_orders.append((product_id, amount, price))

    def sell(self, product_id, amount, price):
        self.sell_orders.append((product_id, amount, price))

class LimitOrderAgent:
    def __init__(self, execution_client):
        self.execution_client = execution_client
        self.orders = []

    def price_tick(self, product_id, price):
        for order in self.orders:
            action, order_product_id, amount, limit = order
            if product_id == order_product_id:
                if action == 'BUY' and price <= limit:
                    self.execution_client.buy(product_id, amount, price)
                    self.orders.remove(order)
                elif action == 'SELL' and price >= limit:
                    self.execution_client.sell(product_id, amount, price)
                    self.orders.remove(order)

    def add_order(self, action, product_id, amount, limit):
        self.orders.append((action, product_id, amount, limit))

class LimitOrderAgentTest(unittest.TestCase):
    def setUp(self):
        self.execution_client = MockExecutionClient()
        self.agent = LimitOrderAgent(self.execution_client)

    def test_buy_order_execution(self):
        product_id = "IBM"
        amount = 1000
        limit = 100

        self.agent.add_order('BUY', product_id, amount, limit)
        self.agent.price_tick(product_id, 99)  

        self.assertEqual(len(self.execution_client.buy_orders), 1)
        executed_order = self.execution_client.buy_orders[0]
        self.assertEqual(executed_order[0], product_id)
        self.assertEqual(executed_order[1], amount)
        self.assertEqual(executed_order[2], 99)

    def test_sell_order_execution(self):
        product_id = "AAPL"
        amount = 500
        limit = 150

        self.agent.add_order('SELL', product_id, amount, limit)
        self.agent.price_tick(product_id, 151) 

        self.assertEqual(len(self.execution_client.sell_orders), 1)
        executed_order = self.execution_client.sell_orders[0]
        self.assertEqual(executed_order[0], product_id)
        self.assertEqual(executed_order[1], amount)
        self.assertEqual(executed_order[2], 151)

if __name__ == '__main__':
    unittest.main()
