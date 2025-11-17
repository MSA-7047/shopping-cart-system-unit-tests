import unittest
from unittest.mock import Mock, call
from src.OrderService import OrderService
from src.ShoppingCart import ShoppingCart
from src.PaymentService import PaymentService
from src.InventoryService import InventoryService
from src.CartItem import CartItem

class OrderServiceTest(unittest.TestCase):
    def setUp(self):
        self.mock_payment_service = Mock(spec=PaymentService)
        self.mock_inventory_service = Mock(spec=InventoryService)
        self.order_service = OrderService(self.mock_payment_service, self.mock_inventory_service)
        self.cart = Mock(spec=ShoppingCart)

    def test_place_order_with_4_items_success(self):
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)
        mock_item_3 = Mock(spec=CartItem)
        mock_item_4 = Mock(spec=CartItem)
        self.cart.calculate_total.return_value = 650
        self.cart.get_items.return_value = [mock_item_1, mock_item_2, mock_item_3, mock_item_4]
        self.mock_payment_service.process_payment.return_value = True

        result = self.order_service.place_order(self.cart, "1234567890123456")
        self.assertTrue(result)
        self.mock_payment_service.process_payment.assert_called_with("1234567890123456", 650)
        calls = [call(mock_item_1), call(mock_item_2), call(mock_item_3), call(mock_item_4)]
        self.mock_inventory_service.update_stock.assert_has_calls(calls)

    def test_place_order_invalid_when_payment_fails(self):
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)
        self.cart.get_items.return_value = [mock_item_1, mock_item_2]
        self.cart.calculate_total.return_value = 300
        self.mock_payment_service.process_payment.side_effect = Exception("Payment failed: Invalid card or amount.")

        result = self.order_service.place_order(self.cart, "1234567890123456")
        self.mock_payment_service.process_payment.assert_called_with("1234567890123456", 300)
        self.assertFalse(result)

    def test_place_order_when_inventory_update_fails(self):
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)
        self.cart.get_items.return_value = [mock_item_1, mock_item_2]
        self.cart.calculate_total.return_value = 300
        self.mock_inventory_service.update_stock.side_effect = Exception("Inventory update failed.")
        self.mock_payment_service.process_payment.return_value = True
        result = self.order_service.place_order(self.cart, "1234567890123456")
        self.assertFalse(result)