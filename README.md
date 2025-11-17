# Shopping Cart System – Unit Testing Project

## Project Overview
This project implements a faulty shopping cart system designed as part of a software testing coursework. The focus of the assignment was to write comprehensive unit tests for the system and justify the test coverage for its functionality.  

The shopping cart system attemptes to simulate an online shopping platform where users can add products to a cart, apply discounts, and calculate totals. The system is structured to allow clear testing of different scenarios, including customer types, bundle discounts, promotions, and coupon codes.

## Key Features
The system provides the following functionality:

- **Total Calculation:** Calculates the total cost of items in the cart before and after discounts.
- **Bundle Discounts:** Supports product combination discounts (e.g., discounts on a mouse when a laptop is purchased).
- **Tiered Discounts:** Applies percentage-based discounts based on total cart value.
- **Customer-Specific Discounts:** Offers additional discounts for Premium and VIP customers.
- **Coupon Codes:** Supports single-use coupon codes with fixed or percentage discounts.
- **Time-Limited Promotions:** Can activate flat discounts for special events.
- **Discount Application Order:** Discounts are applied in a consistent, defined order to ensure predictable outcomes.
- **Error Handling:** Validates transactions, including credit card number length and non-zero, positive amounts.
- **Receipt Generation:** Prints a detailed summary showing items, initial totals, and final prices after all discounts.


## Running the Unit Tests

Clone the repository:

```bash
git clone https://github.com/MSA-7047/shopping-cart-system-unit-tests.git
cd shopping-cart-system-unit-tests
```
Run unit tests with coverage:
```bash
coverage run -m unittest discover -s test -p "*Test.py"
```
View coverage results in the terminal:
```bash
coverage report -m
```
Generate an HTML coverage report:
```bash
coverage html
```

> This will create an htmlcov folder containing index.html.
Open that file in any browser to view detailed coverage information.
