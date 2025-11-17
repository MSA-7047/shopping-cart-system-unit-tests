"""
- this files test cases are here but are not entirely necessary since the enums are static and do not change
- so unless the functionality becomes more complex i dont think its needed to write a whole test class
- but i wrote them anyway for consistency
"""


import unittest
from src.CustomerType import CustomerType

class CustomerTypeTest(unittest.TestCase):
    def test_enum_values(self):
        self.assertEqual(CustomerType.REGULAR.value, "Regular")
        self.assertEqual(CustomerType.PREMIUM.value, "Premium")
        self.assertEqual(CustomerType.VIP.value, "VIP")

    def test_enum_names(self):
        self.assertEqual(CustomerType.REGULAR.name, "REGULAR")
        self.assertEqual(CustomerType.PREMIUM.name, "PREMIUM")
        self.assertEqual(CustomerType.VIP.name, "VIP")