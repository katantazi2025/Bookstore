from memberregister import MemberRegister
import mysql.connector
from mysql.connector import connect, Error
from getpass import getpass
from cart import Cart


class OnlineBookStore:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.logged_in = False
        self.current_user = None
        self.book_store = []
        self.memberregister = MemberRegister(self.conn, self.cursor)
        self.cart = Cart(self.conn, self.cursor, user_id=None, book_store=self, memberregister=self.memberregister)

    def establish_database_connection(self):
        try:
            # Prompt for database login credentials
            db_user = input("Enter database username: ")
            db_password = getpass("Enter database password: ")

            # Establish database connection 
            self.conn = mysql.connector.connect(
                host='localhost',
                user=db_user,
                password=db_password,
                database='book_store',
            )
            self.cursor = self.conn.cursor()
            self.logged_in = True
            print("Succesfully logged in to the database. ")
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        #close the database connection when the object is deleted
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")

   

            #print("Member Login logic goes here")
    def authenticaticate_admin(self, username, password):
        if not self.logged_in:
            print("You need to login first.")
            self.establish_database_connection()
        #else:
        query = "SELECT * FROM members  WHERE Username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        admin = self.cursor.fetchone()

        if admin:
                self.logged_in = True
                self.current_user = admin
                print("Admim Login successful!")
                return True
        else:
                print("Invalid username or password. please try again.")
                return False
    
    def authenticate_member(self, email, password):
        query = "SELECT * FROM members WHERE email = %s AND password = %s"
        self.cursor.execute(query, (email, password))
        member = self.cursor.fetchone()

        if member:
            user_id = member[7]  #Assume User ID is in the first column
            self.memberregister.set_logged_in_user(user_id) # setting the logged in user ID
            self.logged_in = True
            self.current_user = member
            print("Member Login successful!\n")
            return True
        else:
            print("Invalid email or password. please try again. \n")
            return False

    def get_logged_in_user(self):
        return self.current_user[7] if self.current_user else None
        #return self.logged_in_user

    def logout(self):
        self.logged_in = False
        self.current_user = None
        print("Logout successful!\n")
        