import unittest
from src.Customer import Customer
from src.CustomerType import CustomerType

class CustomerTest(unittest.TestCase):
    def setUp(self):
        self.customer_type = CustomerType.REGULAR
        self.customer = Customer("Sameen Ahmed", self.customer_type)
    
    def test_get_name(self):    
        self.assertEqual(self.customer.get_name(), "Sameen Ahmed")

    def test_get_customer_type(self):
        self.assertEqual(self.customer.get_customer_type(), self.customer_type)

    def test_set_name_to_John_Doe(self):
        new_name = "John Doe"
        self.customer.set_name(new_name)
        self.assertEqual(self.customer.get_name(), new_name)

    def test_set_name_to_empty_string(self):
        new_name = ""
        self.customer.set_name(new_name)
        self.assertEqual(self.customer.get_name(), new_name)

    def test_set_name_to_number(self):
        new_name = 100
        self.customer.set_name(new_name)
        with self.assertRaises(ValueError):
            Customer(new_name, self.customer_type)

    def test_set_customer_type_to_premium(self):
        new_customer_type = CustomerType.PREMIUM
        self.customer.set_customer_type(new_customer_type)
        self.assertEqual(self.customer.get_customer_type(), new_customer_type)
    
    def test_set_customer_type_to_vip(self):
        new_customer_type = CustomerType.VIP
        self.customer.set_customer_type(new_customer_type)
        self.assertEqual(self.customer.get_customer_type(), new_customer_type)

    def test_set_customer_type_from_regular_to_regular(self):
        new_customer_type = CustomerType.REGULAR
        self.customer.set_customer_type(new_customer_type)
        self.assertEqual(self.customer.get_customer_type(), new_customer_type)

    def test_set_invalid_customer_type_integer(self):
        with self.assertRaises(ValueError):
            Customer("Sameen Ahmed", 1)

    def test_set_invalid_customer_type_string(self):
        with self.assertRaises(ValueError):
            Customer("Sameen Ahmed", "")
    
    def test_set_invalid_customer_type_bool(self):
        with self.assertRaises(ValueError):
            Customer("Sameen Ahmed", True)

    def test_set_invalid_customer_type_float(self):
        with self.assertRaises(ValueError):
            Customer("Sameen Ahmed", 0.05)

