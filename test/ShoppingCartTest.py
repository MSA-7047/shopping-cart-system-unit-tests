import unittest
from unittest.mock import Mock, patch
from src.ShoppingCart import ShoppingCart
from src.CartItem import CartItem
from src.Product import Product
from src.Customer import Customer
from src.CustomerType import CustomerType
from src.DiscountService import DiscountService


class ShoppingCartTest(unittest.TestCase):

    def setUp(self):
        self.mock_customer = Mock(spec=Customer)
        self.mock_discount_service = Mock(spec=DiscountService)
        self.cart = ShoppingCart(self.mock_customer, self.mock_discount_service)

    def test_add_item_to_cart(self):
        mock_item = Mock(spec=CartItem)
        self.cart.add_item(mock_item)
        self.assertIn(mock_item, self.cart.get_items())

    def test_remove_item_from_cart(self):
        mock_item = Mock(spec=CartItem)
        self.cart.add_item(mock_item)
        self.cart.remove_item(mock_item)
        self.assertNotIn(mock_item, self.cart.get_items())

    def test_apply_coupon_code(self):
        coupon_code = "DISCOUNT10"
        self.cart.apply_coupon_code(coupon_code)
        self.assertEqual(self.cart._coupon_code, coupon_code)

    def test_set_promotion_active_to_true(self):
        self.cart.set_promotion_active(True)
        self.assertTrue(self.cart._is_promotion_active)

    def test_set_promotion_active_to_false(self):
        self.cart.set_promotion_active(False)
        self.assertFalse(self.cart._is_promotion_active)

    def test_calculate_total_less_than_1000(self):
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem) 

        mock_item_1.get_product().get_price.return_value = 100
        mock_item_1.get_quantity.return_value = 2
        mock_item_2.get_product().get_price.return_value = 150
        mock_item_2.get_quantity.return_value = 1

        self.cart.add_item(mock_item_1)
        self.cart.add_item(mock_item_2)

        self.assertEqual(self.cart.calculate_total(), 350)

    def test_calculate_total_greater_than_1000_less_than_5000(self):
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem) 

        mock_item_1.get_product().get_price.return_value = 1000
        mock_item_1.get_quantity.return_value = 2
        mock_item_2.get_product().get_price.return_value = 1500
        mock_item_2.get_quantity.return_value = 1

        self.cart.add_item(mock_item_1)
        self.cart.add_item(mock_item_2)

        self.assertEqual(self.cart.calculate_total(), 3500)

    def test_calculate_total_greater_than_5000_less_than_10000(self):
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem) 

        mock_item_1.get_product().get_price.return_value = 2000
        mock_item_1.get_quantity.return_value = 2
        mock_item_2.get_product().get_price.return_value = 1500
        mock_item_2.get_quantity.return_value = 1

        self.cart.add_item(mock_item_1)
        self.cart.add_item(mock_item_2)

        self.assertEqual(self.cart.calculate_total(), 5500)

    def test_calculate_total_greater_than_10000(self):
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem) 

        mock_item_1.get_product().get_price.return_value = 7000
        mock_item_1.get_quantity.return_value = 2
        mock_item_2.get_product().get_price.return_value = 15000
        mock_item_2.get_quantity.return_value = 1

        self.cart.add_item(mock_item_1)
        self.cart.add_item(mock_item_2)

        self.assertEqual(self.cart.calculate_total(), 29000)

    def test_final_price_without_any_promotions(self):
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)

        mock_item_1.get_product.return_value.get_price.return_value = 100
        mock_item_1.get_quantity.return_value = 1
        mock_item_2.get_product.return_value.get_price.return_value = 50
        mock_item_2.get_quantity.return_value = 1

        self.cart.add_item(mock_item_1)
        self.cart.add_item(mock_item_2)

        self.mock_discount_service.apply_discount.return_value = 150

        final_price = self.cart.calculate_final_price()
        self.assertEqual(final_price, 150)

    def test_final_price_with_cart_value_discount_only(self):
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)

        mock_item_1.get_product.return_value.get_price.return_value = 1000
        mock_item_1.get_quantity.return_value = 1
        mock_item_2.get_product.return_value.get_price.return_value = 100
        mock_item_2.get_quantity.return_value = 1

        self.cart.add_item(mock_item_1)
        self.cart.add_item(mock_item_2)

        self.mock_discount_service.apply_discount.return_value = 990
        final_price = self.cart.calculate_final_price()
        self.assertEqual(final_price, 990)

    def test_final_price_with_cart_value_and_promotion_discounts(self):
        discount_service = DiscountService()
        cart = ShoppingCart(self.mock_customer, discount_service)
        
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)

        mock_item_1.get_product.return_value.get_price.return_value = 1000  #cart value 10%
        mock_item_1.get_quantity.return_value = 1
        mock_item_2.get_product.return_value.get_price.return_value = 100
        mock_item_2.get_quantity.return_value = 1

        cart.add_item(mock_item_1)
        cart.add_item(mock_item_2)

        self.mock_customer.get_customer_type.return_value = CustomerType.REGULAR    #customer type 0%
        cart.apply_coupon_code("")  #coupon code 0%
        cart.set_promotion_active(True) #promotion 25%

        final_price = cart.calculate_final_price()
        self.assertEqual(final_price, 715)

    def test_final_price_with_customer_type_discount_only(self):
        discount_service = DiscountService()
        cart = ShoppingCart(self.mock_customer, discount_service)
        
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)

        mock_item_1.get_product.return_value.get_price.return_value = 400 #cart value 0%
        mock_item_1.get_quantity.return_value = 1
        mock_item_2.get_product.return_value.get_price.return_value = 300
        mock_item_2.get_quantity.return_value = 1

        cart.add_item(mock_item_1)
        cart.add_item(mock_item_2)

        self.mock_customer.get_customer_type.return_value = CustomerType.PREMIUM    #customer type 5%
        cart.apply_coupon_code("")  #coupon 0%
        cart.set_promotion_active(False) #promotion 0%

        final_price = cart.calculate_final_price()
        self.assertEqual(final_price, 665)  # 5% total

    def test_final_price_with_customer_type_and_promotion_discounts(self):
        discount_service = DiscountService()
        cart = ShoppingCart(self.mock_customer, discount_service)
        
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)

        mock_item_1.get_product.return_value.get_price.return_value = 400 #cart value 0%
        mock_item_1.get_quantity.return_value = 1
        mock_item_2.get_product.return_value.get_price.return_value = 300
        mock_item_2.get_quantity.return_value = 1

        cart.add_item(mock_item_1)
        cart.add_item(mock_item_2)

        self.mock_customer.get_customer_type.return_value = CustomerType.PREMIUM    #customer type 5%
        cart.apply_coupon_code("")  #coupon 0%
        cart.set_promotion_active(True) #promotion 25%

        final_price = cart.calculate_final_price()
        self.assertEqual(final_price, 490)  #30% total

    def test_final_price_with_discount10_coupon_only(self):
        discount_service = DiscountService()
        cart = ShoppingCart(self.mock_customer, discount_service)
        
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)

        mock_item_1.get_product.return_value.get_price.return_value = 400 #cart value 0%
        mock_item_1.get_quantity.return_value = 1
        mock_item_2.get_product.return_value.get_price.return_value = 300
        mock_item_2.get_quantity.return_value = 1

        cart.add_item(mock_item_1)
        cart.add_item(mock_item_2)

        self.mock_customer.get_customer_type.return_value = CustomerType.REGULAR    #customer type 0%
        cart.apply_coupon_code("DISCOUNT10")  #coupon 10%
        cart.set_promotion_active(False) #promotion 0%

        final_price = cart.calculate_final_price()
        self.assertEqual(final_price, 630)  #10% total

    def test_final_price_with_discount10_coupon_and_promotion_discounts(self):
        discount_service = DiscountService()
        cart = ShoppingCart(self.mock_customer, discount_service)
        
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)

        mock_item_1.get_product.return_value.get_price.return_value = 400 #cart value 0%
        mock_item_1.get_quantity.return_value = 1
        mock_item_2.get_product.return_value.get_price.return_value = 300
        mock_item_2.get_quantity.return_value = 1

        cart.add_item(mock_item_1)
        cart.add_item(mock_item_2)

        self.mock_customer.get_customer_type.return_value = CustomerType.REGULAR    #customer type 0%
        cart.apply_coupon_code("DISCOUNT10")  #coupon 10%
        cart.set_promotion_active(True) #promotion 25%

        final_price = cart.calculate_final_price()
        self.assertEqual(final_price, 455)  #35% total

    def test_final_price_with_save50_coupon_only(self):
        discount_service = DiscountService()
        cart = ShoppingCart(self.mock_customer, discount_service)
        
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)

        mock_item_1.get_product.return_value.get_price.return_value = 400 #cart value 0%
        mock_item_1.get_quantity.return_value = 1
        mock_item_2.get_product.return_value.get_price.return_value = 300
        mock_item_2.get_quantity.return_value = 1

        cart.add_item(mock_item_1)
        cart.add_item(mock_item_2)

        self.mock_customer.get_customer_type.return_value = CustomerType.REGULAR    #customer type 0%
        cart.apply_coupon_code("SAVE50")  #coupon -50
        cart.set_promotion_active(False) #promotion 0%

        final_price = cart.calculate_final_price()
        self.assertEqual(final_price, 650)  # total-50

    def test_final_price_with_save50_coupon_and_promotion_discounts(self):
        discount_service = DiscountService()
        cart = ShoppingCart(self.mock_customer, discount_service)
        
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)

        mock_item_1.get_product.return_value.get_price.return_value = 400 #cart value 0%
        mock_item_1.get_quantity.return_value = 1
        mock_item_2.get_product.return_value.get_price.return_value = 300
        mock_item_2.get_quantity.return_value = 1

        cart.add_item(mock_item_1)
        cart.add_item(mock_item_2)

        self.mock_customer.get_customer_type.return_value = CustomerType.REGULAR    #customer type 0%
        cart.apply_coupon_code("SAVE50")  #coupon -50
        cart.set_promotion_active(True) #promotion 25%

        final_price = cart.calculate_final_price()
        self.assertEqual(final_price, 487.5)  #(total-50) *0.75

    def test_final_price_with_bundle_discount_only(self):
        discount_service = DiscountService()
        cart = ShoppingCart(self.mock_customer, discount_service)
        
        mock_item_1 = CartItem(Product("Laptop",400,10), 1)
        mock_item_2 = CartItem(Product("Mouse",300,10), 1)

        cart.add_item(mock_item_1)
        cart.add_item(mock_item_2)

        self.mock_customer.get_customer_type.return_value = CustomerType.REGULAR    #customer type 0%
        cart.apply_coupon_code("")  #coupon 0%
        cart.set_promotion_active(False) #promotion 0%

        final_price = cart.calculate_final_price()
        self.assertEqual(final_price, 685)  # mouse 5% only

    def test_final_price_with_all_discounts(self):
        discount_service = DiscountService()
        cart = ShoppingCart(self.mock_customer, discount_service)
        
        mock_item_1 = CartItem(Product("Laptop",1000,10), 1)
        mock_item_2 = CartItem(Product("Mouse",100,10), 1)

        cart.add_item(mock_item_1)
        cart.add_item(mock_item_2)

        self.mock_customer.get_customer_type.return_value = CustomerType.VIP    #customer type 10%
        cart.apply_coupon_code("SAVE50")  #coupon -50
        cart.set_promotion_active(True) #promotion 25%

        final_price = cart.calculate_final_price()
        self.assertEqual(final_price, 574.75)  # mouse 5% only and -50 and 45% total discount 


    @patch('builtins.print')
    def test_print_receipt(self, mock_print):
        discount_service = DiscountService()
        cart = ShoppingCart(self.mock_customer, discount_service)
        
        mock_item_1 = CartItem(Product("Laptop",4000,10), 1)    # cart value 10%
        mock_item_2 = CartItem(Product("Hat",1000,10), 1)

        cart.add_item(mock_item_1)
        cart.add_item(mock_item_2)

        self.mock_customer.get_customer_type.return_value = CustomerType.REGULAR    #customer type 0%
        cart.apply_coupon_code("")  #coupon 0%
        cart.set_promotion_active(False) #promotion %

        cart.print_receipt()
        expected_calls = [
            "----- Shopping Cart Receipt -----",
            "Laptop - 1 x $4000.00",
            "Hat - 1 x $1000.00",
            "---------------------------------",
            "Total before discount: $5000.00",
            "Final price after discounts: $4500.00"
        ]

        actual_calls = [call[0][0] for call in mock_print.call_args_list]
        self.assertEqual(actual_calls, expected_calls)

    def test_get_items_empty_cart(self):
        items_in_cart = self.cart.get_items()
        self.assertEqual(items_in_cart, [])

    def test_get_items_with_1_in_cart(self):
        mock_item_1 = Mock(spec=CartItem)
        self.cart.add_item(mock_item_1)

        items_in_cart = self.cart.get_items()
        self.assertEqual(items_in_cart, [mock_item_1])

    def test_get_items_with_2_in_cart(self):
        mock_item_1 = Mock(spec=CartItem)
        mock_item_2 = Mock(spec=CartItem)
        self.cart.add_item(mock_item_1)
        self.cart.add_item(mock_item_2)

        items_in_cart = self.cart.get_items()
        self.assertEqual(items_in_cart, [mock_item_1, mock_item_2])

    
    


    