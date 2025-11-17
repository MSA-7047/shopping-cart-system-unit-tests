import unittest
from src.PaymentService import PaymentService

class PaymentServiceTest(unittest.TestCase):

    def setUp(self):
        self.payment_service = PaymentService()
        self.valid_card_number = "1234567890123456"
        self.valid_amount = 100

    def test_process_payment_invalid_credit_card_and_invalid_amount(self):
        invalid_card_number = "12345"
        invalid_amount = 0
        with self.assertRaises(Exception):
            self.payment_service.process_payment(invalid_card_number, invalid_amount)

    def test_process_payment_invalid_credit_card_shorter_than_16(self):
        invalid_card_number = "123456789012345"
        with self.assertRaises(Exception):
            self.payment_service.process_payment(invalid_card_number, self.valid_amount)

    def test_process_payment_invalid_credit_card_longer_than_16(self):
        invalid_card_number = "12345678901234567"
        with self.assertRaises(Exception):
            self.payment_service.process_payment(invalid_card_number, self.valid_amount)

    def test_process_payment_invalid_credit_card_contains_letters(self):
        invalid_card_number = "123456789012345a"
        with self.assertRaises(Exception):
            self.payment_service.process_payment(invalid_card_number, self.valid_amount)

    def test_process_payment_invalid_credit_card_contains_symbol(self):
        invalid_card_number = "123456789012345!"
        with self.assertRaises(Exception):
            self.payment_service.process_payment(invalid_card_number, self.valid_amount)

    def test_process_payment_invalid_amount_zero(self):
        invalid_amount = 0
        with self.assertRaises(Exception):
            self.payment_service.process_payment(self.valid_card_number, invalid_amount)

    def test_process_payment_invalid_amount_negative_close_to_zero(self):
        invalid_amount = -0.01
        with self.assertRaises(Exception):
            self.payment_service.process_payment(self.valid_card_number, invalid_amount)

    def test_process_payment_invalid_amount_negative(self):
        invalid_amount = -1
        with self.assertRaises(Exception):
            self.payment_service.process_payment(self.valid_card_number, invalid_amount)

    def test_process_payment_valid_credit_card_length_and_amount(self):
        result = self.payment_service.process_payment(self.valid_card_number, self.valid_amount)
        self.assertTrue(result)

    def test_process_payment_valid_credit_card_length_and_amount_close_to_0(self):
        valid_amount = 0.01
        result = self.payment_service.process_payment(self.valid_card_number, valid_amount)
        self.assertTrue(result)

    def test_process_payment_with_large_amount(self):
        large_amount = 1000000
        result = self.payment_service.process_payment(self.valid_card_number, large_amount)
        self.assertTrue(result)
    

