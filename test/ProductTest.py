import unittest
from src.Product import Product

class ProductTest(unittest.TestCase):
    def setUp(self):
        self.product = Product(name="Laptop", price=1500, stock=10)

    def test_get_name(self):
        self.assertEqual(self.product.get_name(), "Laptop")

    def test_get_price(self):
        self.assertEqual(self.product.get_price(), 1500)

    def test_get_stock(self):
        self.assertEqual(self.product.get_stock(), 10)

    def test_set_stock_to_larger_number_100(self):
        self.product.set_stock(100)
        self.assertEqual(self.product.get_stock(), 100)

    def test_set_stock_to_smaller_number_4(self):
        self.product.set_stock(4)
        self.assertEqual(self.product.get_stock(), 4)

    def test_reduce_all_stock_from_ten_to_zero(self):
        self.product.reduce_stock(10)
        self.assertEqual(self.product.get_stock(), 0)

    def test_reduce_stock_by_5(self):
        self.product.reduce_stock(5) 
        self.assertEqual(self.product.get_stock(), 5)

    def test_reduce_stock_by_1(self):
        self.product.reduce_stock(1) 
        self.assertEqual(self.product.get_stock(), 9)

    def test_reduce_stock_by_0(self):
        self.product.reduce_stock(0) 
        self.assertEqual(self.product.get_stock(), 10)

    def test_reduce_stock_by_more_than_current_stock(self):
        with self.assertRaises(ValueError):
            self.product.reduce_stock(self.product.get_stock() + 1)

    def test_reduce_stock_from_one_to_zero(self):
        self.product.set_stock(1)
        self.product.reduce_stock(1)
        self.assertEqual(self.product.get_stock(), 0)

    def test_reduce_stock_when_stock_is_zero(self):
        self.product.set_stock(0)
        with self.assertRaises(ValueError):
            self.product.reduce_stock(1)

    
    def test_reduce_stock_by_negative_number_invalid(self):
        with self.assertRaises(ValueError):
            self.product.reduce_stock(-5)

    def test_set_stock_to_negative_invalid(self):
        with self.assertRaises(ValueError):
            self.product.set_stock(-5)
        
 


    
