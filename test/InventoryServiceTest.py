import unittest
from src.InventoryService import InventoryService
from src.CartItem import CartItem
from src.Product import Product

class InventoryServiceTest(unittest.TestCase):

    def setUp(self):
        self.inventory_service = InventoryService()

    def create_product(self, stock):
        return Product("Laptop", 100, stock)

    def create_cart_item(self, product, quantity):
        return CartItem(product, quantity)

    def test_update_stock_from_10_with_quantity_4(self):
        product = self.create_product(10)
        cart_item = self.create_cart_item(product, 4)
        self.inventory_service.update_stock(cart_item)
        self.assertEqual(product.get_stock(), 6)

    def test_update_stock_from_20_with_quantity_12(self):
        product = self.create_product(20)
        cart_item = self.create_cart_item(product, 12)
        self.inventory_service.update_stock(cart_item)
        self.assertEqual(product.get_stock(), 8)

    def test_update_stock_from_5_with_quantity_0(self):
        product = self.create_product(5)
        cart_item = self.create_cart_item(product, 0)
        self.inventory_service.update_stock(cart_item)
        self.assertEqual(product.get_stock(), 5)

    def test_update_stock_from_1_with_quantity_1(self):
        product = self.create_product(1)
        cart_item = self.create_cart_item(product, 1)
        self.inventory_service.update_stock(cart_item)
        self.assertEqual(product.get_stock(), 0)

    def test_update_stock_with_quantity_exceeding_stock(self):
        product = self.create_product(5)
        cart_item = self.create_cart_item(product, 6)
        
        with self.assertRaises(RuntimeError):
            self.inventory_service.update_stock(cart_item)
        
        self.assertEqual(product.get_stock(), 5)

    def test_update_stock_when_stock_is_zero(self):
        product = self.create_product(0)
        cart_item = self.create_cart_item(product, 1)
        
        with self.assertRaises(RuntimeError):
            self.inventory_service.update_stock(cart_item)
        
        self.assertEqual(product.get_stock(), 0)
