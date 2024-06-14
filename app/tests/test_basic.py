import unittest
from app import create_app, db
from app.models.order import Order
from datetime import time


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_class='app.test_config.TestConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello, World!")

    def test_database_insertion(self):
        new_order = Order(order_id='12345', order_time=time(12, 30, 0), district='Test District', city='Test City',
                          amount=100.0, currency='USD', quantity=1)
        db.session.add(new_order)
        db.session.commit()
        order = Order.query.filter_by(order_id='12345').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.order_id, '12345')
        self.assertEqual(order.city, 'Test City')

    def test_test_db_route(self):
        response = self.client.get('/test_db')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['order_id'], '12345')
        self.assertEqual(data['city'], 'Test City')


if __name__ == "__main__":
    unittest.main()
