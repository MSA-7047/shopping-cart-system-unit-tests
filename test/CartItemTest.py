import unittest
from unittest.mock import Mock
from src.CartItem import CartItem

class CartItemTest(unittest.TestCase):
    def setUp(self):
        self.mock_product = Mock()
        self.mock_product.get_price.return_value = 100
        self.cart_item = CartItem(self.mock_product, 3)

    def test_get_product(self):
        self.assertEqual(self.cart_item.get_product(), self.mock_product)

    def test_get_quantity(self):
        self.assertEqual(self.cart_item.get_quantity(), 3)

    def test_get_total_price_of_3_items(self):
        total_price_calculated = self.cart_item.get_total_price()
        self.assertEqual(total_price_calculated, 300)

    def test_get_total_price_with_zero_quantity(self):
        cart_item_zero_quantity = CartItem(self.mock_product, 0)
        total_price = cart_item_zero_quantity.get_total_price()
        self.assertEqual(total_price, 0)

    def test_get_total_price_with_product_price_650(self):
        self.mock_product.get_price.return_value = 650
        cart_item = CartItem(self.mock_product, 4)
        total_price = cart_item.get_total_price()
        self.assertEqual(total_price, 650*4)

