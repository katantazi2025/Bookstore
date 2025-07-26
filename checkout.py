import datetime
from memberregister import MemberRegister

class Checkout:
    def __init__(self, user_id, cart):
        self.member_reg = MemberRegister
        self.user_id = user_id
        self.cart = cart
        self.conn = cart.conn
        self.cursor = cart.cursor

    def display_invoice(self):
        # Displaying current cart contents
        self.cart.display_cart()
        print("Current Cart Contents: ")
        print("{:<12} {:<40} {:<6} {:<10}".format("ISBN", "Title", "$", "Qty", "Total"))
        print("-" * 80)

        for book in self.cart.display_cart():
            isbn, title, price, quantity = book
            total_price = price * quantity
            print("{:<12} {:<40} {:6.2f} {:<6} {:10.2f}".format(isbn, title, price, quantity, total_price))

        print("-" * 80)
        total_cart_price = sum(price * quantity for _, _, price, quantity in self.cart)
        print("{:<70} {:<10.2f}".format("Total =", total_cart_price))

        proceed_checkout = input("Proceed to check out (Y/N)?: ").strip().lower()
        if proceed_checkout == 'y':
            

            # Save order details to the database
            order_number = self.generate_order_number()
            received_date = datetime.datetime.now()
            shipment_date = received_date + datetime.timedelta(days=7)

            # Retrieve user Id from Cart
            user_id = self.cart.get_user_id()

            # Save order details to the order table
            self.save_order_to_database(order_number, received_date, shipment_date, user_id)

            # Save books, their quantity, and amount to the odetail table
            for isbn, _, price, quantity in self.cart:
                amount = price * quantity
                self.save_order_detail_to_database(order_number, isbn, quantity, amount)

            # Displaying the invoice
            self.display_final_invoice(order_number, total_cart_price, shipment_date)
            self.cart.clear_cart()
            input("\nPress enter to go back to Menu")
        else:
            print("Checkout is canceled!")

    def generate_order_number(self):
        #Generate a unique order number based on the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        order_number = f"{timestamp}{self.user_id}"
        return int(order_number)

    def save_order_to_database(self, order_number, received_date, shipment_date, user_id):
        try:
            # Fetch address details from members table
            address_query = "SELECT address, city, zip FROM members WHERE userid = %s"
            self.cart.cursor.execute(address_query, (self.user_id,))
            address_details = self.cart.fetchone()

            if address_details:
                # upack the fetched details
                ship_address, ship_city, ship_zip = address_details
                # Excute an SQL INSERT query to save order details to ordertable
                order_query = """
                    INSERT INTO `orders` (userid, ono, created, shipAddress, shipcity, shipzip)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                self.cart.cursor.execute(order_query, (self.user_id, order_number, received_date, ship_address, ship_city, ship_zip))
                self.cart.conn.commit()
            else:
                print("Error: Member details not found.")
        except Exception as e:
            print(f"Error saving order details to the database: {e}")

    def save_order_detail_to_database(self, order_number, isbn, quantity, price):
        try:
            # Calculate the amount based on the fetched price and quantity
            # amount = price * quantity
            
            # Excute an SQL INSERT query to save order details to odetail table
            odetail_query = """
                INSERT INTO `odetails` (ono, isbn, qty, amount)
                SELECT %s, isbn, qty, price * qty
                FROM cart
                Join books ON cart.isbn = books.isbn
                WHERE userid = %s
            """
            amount = price * quantity
            
            self.cursor.execute(odetail_query, (order_number, isbn, quantity, amount))
            self.conn.commit()
            
            # Calculate the amount base on the price  and quantity 
            # price = self.
            #self.cart.cursor.execute(query, (order_number, isbn, quantity, amount))
            #self.cart.conn.commit()
        except Exception as e:
            print(f"Error saving order details to the database: {e}")

    def display_final_invoice(self, order_number, shipment_address, total_cart_price, shipment_date):
        cart_items = self.cart.display_cart()
        print("\nInvoice for Order No. {}".format(order_number))
        print("\nShipping Address")
        print("Name: {}".format(self.user.full_name))
        print("Address: {}".format(shipment_address))
        print("-" * 50)
        print("{:<12} {:<40} {:<6} {:<10}".format("ISBN", "Title", "$", "Qty"))
        print("_" * 80)

        for book in self.cart:
            isbn, title, price, quantity = book
            total_price = price * quantity
            print("{:<12} {:<40} {:<6.2f} {:<6} {:<10.2f}".format(isbn, title, price, quantity, total_price))

        print("-" * 80)
        print("{:<70} {:<10.2f}".format("Total =", total_cart_price))

        # Calculating the estimated delivery date
        estimated_delivery_date = shipment_date + datetime.timedelta(days=7)
        print("\nEstimated Delivery Date: {}".format(estimated_delivery_date))

    def checkout_process(self, user_id):
         # Generate a unique order number based on the current timestamp and user ID
        order_number = self.generate_order_number()

        # Get current date and shipment date
        received_date = datetime.datetime.now()
        shipment_date = received_date + datetime.timedelta(days=7)

        # Save order details to the orders table
        self.save_order_to_database(order_number, received_date, shipment_date, user_id)

        # Save items from the cart to the odetail table
        cart_items = self.cart.get_cart_items()
        for isbn, _, price, quantity in cart_items:
            amount = price * quantity
            self.save_order_detail_to_database(order_number, isbn, quantity, amount)

        # Display the final invoice
        self.display_final_invoice(order_number, shipment_date)

        # Clear the cart
        self.cart.clear_cart()

    
        