import mysql.connector
from getpass import getpass

class MemberRegister:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.logged_in_user = None

    def new_member_registration(self):
        # Get input from the user  for new member data
        print("\nwelcome to the online Book Store\nNew Member Registration")
        first_name = input("Enter first name: ")
        last_name  = input("Enter last name:  ")
        address= input("Enter street address: ")
        city = input("Enter City: ")
        zip = input("Enter zip code: ")
        phone= input("Enter phone number: ")
        email = input("Enter email address: ")
        password = input("Enter password: ")

        # Simulate storing member details in the database
        new_member = {
            'fname': first_name,
            'lname': last_name,
            'address': address,
            'city': city,
            'zip': zip,
            'phone': phone,
            'email': email,
            'password': password,
        }

        #Insert the new member into the database
    
        self.cursor.execute("""
            INSERT INTO members 
            (fname, lname, address, city, zip, phone, email, password) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            new_member['fname'],
            new_member['lname'],
            new_member['address'],
            new_member['city'],
            new_member['zip'],
            new_member['phone'],
            new_member['email'],
            new_member['password'],
        ))
        self.conn.commit()

        print("\nYou have registered successfully!")
        input("Press Enter to return to main menu")

    
    
    
    def set_logged_in_user(self, user_id):
        #self.set_logged_in_user = user_id
        self.logged_in_user = user_id

    def get_logged_in_user(self):
        return self.logged_in_user