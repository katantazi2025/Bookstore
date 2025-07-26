

class SearchBooks:
    def __init__(self, conn, cursor, book_store, cart):
        self.conn = conn
        self.cursor = cursor
        self.book_store = book_store
        self.cart = cart
    
    def author_search(self, search_author):
        query = "SELECT isbn, title, author, price, subject FROM books WHERE author LIKE %s"
        self.cursor.execute(query, ('%' + search_author + '%',))
        bookslist = self.cursor.fetchall()

        if bookslist:
            print(f"\n{len(bookslist)} books found\n")
            self.display_books(bookslist)
            #self.handle_book_selection(bookslist)
        
        else:
            print("No books found with the given author. \n")

    def display_books(self, booklist):
        #for index, book in enumerate(booklist, start=1):
        books_per_page = 3
        total_books = len(booklist)
        start_index = 0

        while start_index < total_books:
            end_index = min(start_index + books_per_page, total_books)

           # print(f"\n{end_index - books_per_page} books found:")
            for index, book in enumerate(booklist[start_index:end_index], start=start_index + 1):

            #print(f"\n{end_index - start_index} books")
                print(f"{index}. Author: {book[2]}\nTitle: {book[1]}\nISBN: {book[0]}\nPrice: {book[3]}\nSubject: {book[4]}\n")
            option = input(f"Enter ISBN to add to cart or 'n' to browse more or press ENTER to return to main menu: ")
            if option.lower() == 'n':
                start_index += books_per_page
                
            
            elif option:   
                 quantity = input("Enter Quantity: ")
                 selectec_book = next((book for book in booklist[start_index:end_index] if book[0] == option), None)
                 #selectec_book = next((book for book in booklist if book[1] == option), None )
                 if selectec_book:
                    user_id = self.book_store.get_logged_in_user()
                    isbn = selectec_book[0]
                    qty =int(quantity)
                    print("Debug Messages:")
                    print(f"User ID: {user_id}")
                    print(f"Selected ISBN: {isbn}")
                    print(f"Quantity: {qty}")
                    self.cart.add_to_cart(user_id, isbn, qty)
                    #self.cart.add_to_cart(self.book_store.get_logged_in_user(), selectec_book[0], int(quantity))
                     #cart.add_to_cart(self.book_store.get_logged_in_user(), *selectec_book, int(quantity))
                     #cart.add_to_cart(selectec_book + (int(quantity),))
                    #self.book_store.cart.add_to_cart(self.book_store.get_logged_in_user(), option, int(quantity))
                    print("****************************************************************************")
                    print(f"Added {quantity} book(s) with ISBN {option} to cart")
                    print("*****************************************************************************")
            else:
                break
                print("The books are displayed successfully")

            
           

    def title_search(self, search_title):
        query = "SELECT isbn, title, author, price, subject FROM books WHERE title LIKE %s"
        self.cursor.execute(query, ('%' + search_title + '%',))
        bookslist = self.cursor.fetchall()

        if bookslist:
            print(f"\n{len(bookslist)} books found\n")
            self.display_books(bookslist)
            #self.handle_book_selection(bookslist)
        
        else:
            print("No books found with the given title. \n")
    
    