import unittest
from unittest.mock import Mock
from src.DiscountService import DiscountService
from src.CartItem import CartItem
from src.Product import Product
from src.CustomerType import CustomerType

class DiscountServiceTest(unittest.TestCase):
    
    def setUp(self):
        self.discount_service = DiscountService()
    
    def calculate_discount(self, price, customer_type, expected_total, coupon_code):
        """Helper function to apply discount on a single product and assert the result"""
        mock_product = Mock()
        mock_product.get_price.return_value = price
        mock_product.get_name.return_value = "Mock Product"  # not a mouse or a laptop
        
        cart_item = Mock()
        cart_item.get_product.return_value = mock_product
        cart_items = [cart_item]

        initial_total = mock_product.get_price()
        final_total = self.discount_service.apply_discount(initial_total, customer_type, cart_items, coupon_code)
        self.assertEqual(final_total, expected_total)

    def create_cart_item(self, product_name, quantity, price):
        """Helper function to create a mocked CartItem."""
        product = Mock(spec=Product)
        product.get_name.return_value = product_name
        product.get_price.return_value = price
        cart_item = Mock(spec=CartItem)
        cart_item.get_product.return_value = product
        cart_item.get_quantity.return_value = quantity
        return cart_item

    def test_apply_promotion_discount_only(self):
        total_before_promotion = 1000
        total_after_promotion = self.discount_service.apply_promotion_discount(total_before_promotion)
        self.assertEqual(total_after_promotion, 750)

    def test_cart_value_discounts_only(self):
        customer_type = CustomerType.REGULAR
        coupon_code = ""
        test_cases = [
            (1, 1),           # lower bound 0% discount
            (1000, 1000),     # upper bound 0% discount
            (1001, 900.9),    # lower bound 10% discount
            (5000, 4500),     # upper bound 10% discount
            (5001, 4250.85),  # lower bound 15% discount
            (10000, 8500),    # upper bound 15% discount
            (10001, 8000.80), # lower bound 20% discount
        ]
        for price, expected_total in test_cases:
            with self.subTest(price=price, customer_type=customer_type, expected_total=expected_total):
                self.calculate_discount(price, customer_type, expected_total, coupon_code)

    def test_customer_type_discounts_only(self):
        price = 500
        coupon_code = ""
        test_cases = [
            (CustomerType.REGULAR, 500),    # 100% of 500 is 500
            (CustomerType.PREMIUM, 475),    # 95% of 500 is 475
            (CustomerType.VIP, 450)         # 90% of 500 is 450
        ]

        for customer_type, expected_total in test_cases:
             with self.subTest(customer_type=customer_type, price=price, expected_total=expected_total):
                 self.calculate_discount(price, customer_type, expected_total, coupon_code)
                 
    def test_coupon_discounts_only(self):
        price = 800
        customer_type = CustomerType.REGULAR
        test_cases = [
            ("", 800),            # no coupon code
            ("DISCOUNT10", 720),  # 90% of 800 is 720
            ("SAVE50", 750),      # reduces $50 from 800 (800 - 50 = 750)
            ("INVALIDCODE", 800)  # invalid coupon, price remains the same
        ]
        
        for coupon_code, expected_total in test_cases:
            with self.subTest(coupon_code=coupon_code, price=price, expected_total=expected_total):
                self.calculate_discount(price, customer_type, expected_total, coupon_code)

    def test_apply_bundle_discount_with_zero_laptops_and_one_mouse(self):
        mouse_item = self.create_cart_item("Mouse", 1, 10)
        cart_items = [mouse_item]
        final_total = self.discount_service.apply_discount(10, CustomerType.REGULAR, cart_items, "")
        self.assertEqual(final_total, 10)
    
    def test_apply_bundle_discount_with_one_laptop_and_zero_mice(self):
        laptop_item = self.create_cart_item("Laptop", 1, 100)
        cart_items = [laptop_item]
        final_total = self.discount_service.apply_discount(100, CustomerType.REGULAR, cart_items, "")
        self.assertEqual(final_total, 100)

    def test_apply_bundle_discount_with_one_laptop_and_one_mouse(self):
        laptop_item = self.create_cart_item("Laptop", 1, 100)
        mouse_item = self.create_cart_item("Mouse", 1, 10)
        cart_items = [laptop_item, mouse_item]
        final_total = self.discount_service.apply_discount(110, CustomerType.REGULAR, cart_items, "")
        self.assertEqual(final_total, 109.5)

    def test_apply_bundle_discount_with_one_laptop_and_two_mice(self):
        laptop_item = self.create_cart_item("Laptop", 1, 100)
        mouse_item = self.create_cart_item("Mouse", 2, 10)
        cart_items = [laptop_item, mouse_item]
        final_total = self.discount_service.apply_discount(120, CustomerType.REGULAR, cart_items, "")
        self.assertEqual(final_total, 119.5)

    def test_apply_bundle_discount_with_two_laptops_and_one_mouse(self):
        laptop_item = self.create_cart_item("Laptop", 2, 100)
        mouse_item = self.create_cart_item("Mouse", 1, 10)
        cart_items = [laptop_item, mouse_item]
        final_total = self.discount_service.apply_discount(210, CustomerType.REGULAR, cart_items, "")
        self.assertEqual(final_total, 209.5)

    def test_apply_bundle_discount_with_two_laptops_and_two_mice(self):
        laptop_item = self.create_cart_item("Laptop", 2, 100)
        mouse_item = self.create_cart_item("Mouse", 2, 10)
        cart_items = [laptop_item, mouse_item]
        final_total = self.discount_service.apply_discount(220, CustomerType.REGULAR, cart_items, "")
        self.assertEqual(final_total, 219)