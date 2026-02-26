import re
import database
from PyQt6.QtCore import QDateTime


class UserController:
    def __init__(self, view, user_id, username, full_name):
        self.view = view
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.cart = []

        # Pagination
        self.orders_page = 0
        self.orders_per_page = 10
        self.bookings_page = 0
        self.bookings_per_page = 10

    # --- PRODUCT OPERATIONS ---
    def get_all_products(self, category=None, search=None):
        """Returns all available products with filtering"""
        return database.get_products(category, search)

    def get_categories(self):
        """Returns all product categories"""
        return database.get_categories()

    # --- CART OPERATIONS ---
    def add_to_cart(self, code, name, price, max_stock, qty):
        """Adds items to cart with stock validation"""
        if qty <= 0:
            return False, "Invalid quantity"

        # Check if item already in cart
        for item in self.cart:
            if item['code'] == code:
                if item['qty'] + qty > max_stock:
                    return False, f"Stock limit reached. You have {item['qty']} in cart."
                item['qty'] += qty
                item['total'] = item['qty'] * item['price']
                return True, f"Updated quantity to {item['qty']}"

        # Add new item
        self.cart.append({
            "code": code,
            "name": name,
            "price": price,
            "qty": qty,
            "total": price * qty
        })
        return True, f"Added {qty} x {name} to Cart"

    def update_cart_quantity(self, code, new_qty, max_stock):
        """Updates quantity of an item in cart"""
        if new_qty <= 0:
            return self.remove_from_cart(code)

        if new_qty > max_stock:
            return False, f"Cannot exceed stock limit of {max_stock}"

        for item in self.cart:
            if item['code'] == code:
                item['qty'] = new_qty
                item['total'] = item['qty'] * item['price']
                return True, "Quantity updated"

        return False, "Item not found in cart"

    def remove_from_cart(self, code):
        """Removes an item from cart"""
        self.cart = [item for item in self.cart if item['code'] != code]
        return True, "Item removed"

    def get_cart_items(self):
        """Returns current cart items"""
        return self.cart

    def get_cart_total(self):
        """Calculates total cart value"""
        return sum(item['total'] for item in self.cart)

    def clear_cart(self):
        """Empties the shopping cart"""
        self.cart = []
        return True, "Cart cleared"

    # --- CHECKOUT ---
    def process_checkout(self, payment_method, bank_name=None, account_number=None):
        """Processes cart checkout and generates receipt"""
        if not self.cart:
            return False, "Cart is empty", None

        # Validate payment info
        if payment_method == "Bank Transfer":
            if not bank_name or not account_number:
                return False, "Please provide bank details", None

        receipt_items = list(self.cart)
        grand_total = sum(i['total'] for i in receipt_items)

        result = database.checkout_cart(self.username, self.cart, payment_method, bank_name, account_number)

        if result == "Success":
            timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm AP")

            line = "-" * 40
            dbl_line = "=" * 40

            receipt_text = f"""
{dbl_line}
            OFFICIAL RECEIPT
{dbl_line}
Date:     {timestamp}
Customer: {self.full_name}
Payment:  {payment_method}
"""

            if payment_method == "Bank Transfer":
                receipt_text += f"Bank:     {bank_name}\nAccount:  {account_number}\n"

            receipt_text += f"""
{line}
{'ITEM':<18} {'QTY':>3} {'PRICE':>7} {'TOTAL':>8}
{line}
"""
            for item in receipt_items:
                name = item['name'][:16] + ".." if len(item['name']) > 18 else item['name']
                qty = item['qty']
                price = item['price']
                total = item['total']
                receipt_text += f"{name:<18} {qty:>3} {price:>7.0f} {total:>8.0f}\n"

            receipt_text += f"""
{line}
GRAND TOTAL: {'₱' + f'{grand_total:,.2f}':>24}
{dbl_line}
       THANK YOU FOR SHOPPING!
{dbl_line}
"""
            self.cart = []
            return True, "Checkout successful", receipt_text
        else:
            return False, f"Checkout Failed: {result}", None

    # --- ORDER HISTORY ---
    def get_order_history(self):
        """Returns user's purchase history"""
        return database.get_user_sales(self.username)

    def get_order_history_page(self):
        """Returns paginated orders for current page"""
        all_orders = database.get_user_sales(self.username)
        start = self.orders_page * self.orders_per_page
        return all_orders[start:start + self.orders_per_page]

    def get_total_order_pages(self):
        total = len(database.get_user_sales(self.username))
        return max(1, (total + self.orders_per_page - 1) // self.orders_per_page)

    # --- SERVICE BOOKING ---
    def book_service(self, service_type, scheduled_date, description):
        """Books a service appointment"""
        try:
            # Service pricing
            service_prices = {
                "System Reformat": 500.00,
                "Deep Cleaning / Dust Removal": 350.00,
                "Hardware Installation": 300.00,
                "Troubleshooting / Diagnostics": 250.00,
                "Thermal Paste Repasting": 200.00,
                "Software Installation": 150.00,
                "Others (Custom Request)": 500.00  # Will be quoted later
            }

            price = service_prices.get(service_type, 0.00)
            full_desc = f"[Scheduled: {scheduled_date}] {description}"

            database.book_service(self.username, service_type, full_desc, price)

            if service_type == "Others":
                return True, f"Service request submitted!\nOur team will contact you with a quote."
            else:
                return True, f"Service booked for {scheduled_date}!\nEstimated Cost: ₱{price:,.2f}"
        except Exception as e:
            return False, str(e)

    def get_my_bookings(self):
        """Returns user's service bookings"""
        return database.get_user_services(self.username)

    def get_my_bookings_page(self):
        """Returns paginated bookings for current page"""
        all_bookings = database.get_user_services(self.username)
        start = self.bookings_page * self.bookings_per_page
        return all_bookings[start:start + self.bookings_per_page]

    def get_total_bookings_pages(self):
        total = len(database.get_user_services(self.username))
        return max(1, (total + self.bookings_per_page - 1) // self.bookings_per_page)

    def cancel_booking(self, service_id):
        """Cancels a service booking"""
        database.delete_service(service_id)
        return True, "Booking cancelled"

    # --- LOGOUT ---
    def logout(self):
        """Returns to login screen"""
        # Will be handled by view
        pass