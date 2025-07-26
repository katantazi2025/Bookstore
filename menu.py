from memberregister import MemberRegister
from bookstore import OnlineBookStore
from getpass import getpass
from book import Book
import sys
from searchbooks import SearchBooks
from checkout import Checkout


class Menu:
    
    def __init__(self, book_store, cart):
        
        self.book_store =book_store
        self.cart = cart
        self.book = Book(self.book_store.conn, self.book_store.cursor, self.book_store, self.cart, self.book_store.memberregister )
        self.memberreg = MemberRegister(self.book_store.conn, self.book_store.cursor)
        self.logged_in = False
        self.search_books = SearchBooks(book_store.conn, book_store.cursor, book_store,cart)
       
       
        

    def main_menu(self):
        with OnlineBookStore() as book_store:
            while True:
                print("****************************************************************")
                print("***                                                          ***")
                print("***             Welcome to the Online Book Store             ***")
                print("***                                                          ***")
                print("****************************************************************")
                print(                   "1. Member Login"                              )
                print(                   "2. New Member Registration"                   )
                print(                   "Q. Quit"                                      )

                option = input("Type in your option: ")

                if option == '1':
                    self.access_to_submenu(self.book_store)
                
                elif option == '2':
                         member_register = self.memberreg
                         member_register.new_member_registration()
                    
                elif option.lower() == 'q':
                    print("Thank you for visiting the Online Book Store!")
                    sys.exit()
                    
                   
    def access_to_submenu(self, book_store):
        print("Choose login type: ")
        print("1. Admin Login (Database credentials)")
        print("2. Members Login (Member crendetials)")
        
        login_type = input("Type your option:")

        if login_type == '1':
            self.admin_login()
        elif login_type == '2':
            if not self.book_store.cursor:
                print("Please you need to establish a databes connection first.")
                self.book_store.establish_database_connection()
            self.member_credentials_login()
            
            
        else:
            print("Invalid option. please selt the valid option.")
    
    def member_login(self):
        if not self.logged_in:
            self.book_store.establish_database_connection()
            username = input("Enter Username: ")
            password = getpass("Enter password: ")
            if self.book_store.authenticate_member(username, password):
                self.logged_in = True
                self.member_menu()
            #print("you need to login in first. ")
           
            else:
                print("Invalid username or password. please try again.")
        else:
            print("You are already logged in.")
    
    def admin_login(self):
        #using the database credential for admin login
        if not self.logged_in:
            print("You need to login first.")
            self.book_store.establish_database_connection()
            if self.logged_in:
                print("Admin login successful!\n")
        else:
            print("you are already logged in.\n")

    def member_credentials_login(self):
        #Check if OnlineBookStore has a valid cursor
        if not self.book_store.cursor:
            print("You need to establish a database connection first.")
            self.book_store.establish_database_connection()
        #checking if the cursor is valid  before proceeding
        if self.book_store.cursor:
        #using members credentials to login
            email = input("Enter your email: ")
            password = getpass("Enter your password: ")
            if self.book_store.authenticate_member(email, password):
               # print("Login in successful!\n")
                self.member_menu()
        else:
            print("Failed to establish a valid database connection!")
        
    def member_menu(self):
        while True:
             print("****************************************************************")
             print("***                                                          ***")
             print("***             Welcome to the Online Book Store             ***")
             print("***                    Member Menu                           ***")
             print("****************************************************************")
             print(                   "1. Browse by subject"                         )
             print(                   "2. Search by Author/Title"                    )
             print(                   "3. Check out"                                 )
             print(                    "4. Logout"                                   )
             
             option = input("Enter your choice: ")

             if option == '1':
                 self.book.browse_by_subject()
                 #print("Browsing by Subject.....")
             elif option == '2':
                 self.search_menu()
                 #print("Seaching by Author/Title....")
             elif option == '3':
                 self.checkout_option()
             elif option == '4':
                self.logout()
                break
             else:
                 print("Invalid Option. please select a valid option.")

    
    def search_menu(self):
        while True:
            print("*********************************************************************")
            print("****               Welcome to the online Book Store              ****")
            print("****                Seach by Author/Title Menu                   ****")
            print("*********************************************************************")
            print("1. Author Search")
            print("2. Title Search")
            print("3. Go Back to Member Menu")
            search_option = input("Type in your option: ")

            if search_option == '1':
                self.search_books.author_search(self.get_search_term())
            elif search_option =='2':
                self.search_books.title_search(self.get_search_term())
            elif search_option == '3':
                break
            else:
                print("Invalid option. please check the valid option.")

    def checkout_option(self):
        print("checking out..........")
        if self.logged_in:
            user_id = self.cart.get_user_id()
        #if self.cart.has_items():
            self.checkout.checkout()
        else:
            print("Currently you have no orders in your orders  and odetail table to to checkout")
    
    
    def search_by_title(self):
        search_term = input("Enter  the title or part of the title: ")
        self.search_books.title_search(search_term)

    def get_search_term(self):
        return input("Enter author/title or part of the author's/ title's name: ")
    
    # Inside your Menu class or wherever you handle the checkout option
    def checkout_menu_option(self):
        user_id = self.book_store.get_logged_in_user()
        self.cart.checkout(user_id)

                

    def logout(self):
        print("Logout successful!")


        