from memberregister import MemberRegister
from bookstore import OnlineBookStore
#from getpass import getpass
from book import Book
from menu import Menu
from cart import Cart

class Main:
    def __init__(self,  book_store, cart):
        self.book_store = book_store
        self.cart = cart
        self.cart = Cart(self.book_store.conn, self.book_store.cursor, user_id=None, book_store= self.book_store, memberregister=self.book_store.memberregister)
        self.book = Book(self.book_store.conn, self.book_store.cursor, self.book_store, self.cart, self.book_store.memberregister)
        self.menu = Menu(self.book_store, self.cart)
    
    def run_program(self):
        #with OnlineBookStore() as book_store:
            while True:
                self.menu.main_menu()
            
if __name__ == "__main__":
    book_store_instance = OnlineBookStore()
    book_store_instance.establish_database_connection()
    member_register_instance = MemberRegister(book_store_instance.conn, book_store_instance.cursor)
    main_instance = Main(book_store_instance, book_store_instance.cart)
    menu_instance = Menu(book_store_instance, book_store_instance.cart)
    main_instance.run_program()

