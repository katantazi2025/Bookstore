import mysql.connector
from memberregister import MemberRegister


class Cart:
    def __init__(self, conn, cursor, user_id, book_store, memberregister ):
        self.conn = conn
        self.cursor = cursor
        self.memberregister = memberregister
        self.user_id = user_id
        self.book_store = book_store

    
    def add_to_cart(self, user_id, isbn, qty):
        print("Inside add_to_cart method")
        print(f"User ID: {user_id}, ISBN: {isbn}, Quantity: {qty}")
        user_id = int(user_id)
        print(f"Validate userid: {user_id}")
        if user_id is not None:
        #Check if the book with the given ISBN exist.
            book_exists = self.check_book_exists(isbn)
            print(f"Book exists: {book_exists}")
            if book_exists:
            #Add the book to the cart table
                print("Before INSERT query")
                self.cursor.execute(""" 
                    INSERT INTO cart (userid, isbn, qty)
                    VALUES (%s, %s, %s)
                """,  (user_id, isbn, qty))
                print("After INSERT query")
                self.conn.commit()    

            else:
                print(f"Book with ISBN {isbn} does not exist.")
        else:
            print("Invalid user ID.")


    def check_book_exists(self, isbn):
        print(f"Checking if book with ISBN {isbn} exists")
        #check if the book with the given ISBN exists in the books table
        query = "SELECT COUNT(*) FROM books WHERE isbn = %s"
        self.cursor.execute(query, (isbn,)) 
        result = self.cursor.fetchone()
        print(f"Result of query: {result}")
        return result[0] > 0
    
    
    def display_cart(self):
        try:
         # Display the contents of the cart for the current user
            print("Inside dispaly cart method")
            query = """
                SELECT b.isbn, b.title, b.author, b.price, c.qty
                FROM cart c
                JOIN books b ON c.isbn = b.isbn
                WHERE c.userid = %s
            """ 
            self.cursor.execute(query, (self.user_id,))
            cart_items = self.cursor.fetchall()

            print("\nYour Cart:")
            for item in cart_items:
                print(f"ISBN: {item[0]}, Title: {item[1]}, Author: {item[2]}, Price: {item[3]}, Quantity: {item[4]}")
        except Exception as e:
            print(f"Error in the dispaly cart: {e}")

    def get_user_id(self):
        return self.user_id


    def clear_cart(self):
        try:
            #Excuting and  sql Delete  the query  to remove all items  from the cart   for the current user
            query = "DELETE FROM cart WHERE userid = %s"
            self.cursor.execute(query, (self.user_id,))
            self.conn.commit()
            print("Cart cleared successfuly!")
        except Exception as e:
            print(f"Error clearing the cart: {e}")    



    def get_cart_items(self):
        # Query the database to retrieve cart items for the current user
        if self.user_id:
            query = "SELECT isbn, quantity FROM cart WHERE userid = %s"
            self.cursor.execute(query, (self.user_id,))
            return self.cursor.fetchall()
        else:
            print("User is not logged in.")
            return []
        
    
    def has_items(self):
        # Implement logic to check if the cart has items
        # For example, you can check if there are any items associated with the user_id
        query = "SELECT COUNT(*) FROM cart WHERE userid = %s"
        self.cursor.execute(query, (self.user_id,))
        result = self.cursor.fetchone()
        if result and result[0] > 0:
            return True
        else:
            return False

                 
            # Assuming you have a Cart object initialized somewhere in your code
