# import mysql.connector
from cart import Cart


class Book:
    def __init__(self, conn, cursor, book_store, cart, memberregister):
        self.conn = conn
        self.cursor = cursor
        self.book_store = book_store
        self.cart = Cart(conn, cursor, user_id=None, book_store=self.book_store, memberregister=memberregister)
        self.memberregister = memberregister

    def browse_by_subject(self):
        print("Browsing by subject....")
        subjects = self.get_all_subjects()
        subjects.sort()  # Sort subjects alphabetically

        for index, subject in enumerate(subjects, start=1):
            print(f"{index}. {subject}")

        chosen_subject_index = input("Enter your choice: ")

        try:
            chosen_subject_index = int(chosen_subject_index)
            chosen_subject = subjects[chosen_subject_index - 1]
            self.display_books_by_subject(chosen_subject)
        except (ValueError, IndexError):
            print("Invalid choice. Returning to the main menu.")

    def get_all_subjects(self):
        print(f"Before execute - conn: {self.conn}, cursor: {self.cursor}")
        query = "SELECT DISTINCT subject FROM books ORDER BY subject"
        self.cursor.execute(query)
        subjects = [row[0] for row in self.cursor.fetchall()]
        print(f"After execute - conn: {self.conn}, cursor: {self.cursor}")
        return subjects

    def display_books_by_subject(self, subject):
        query = "SELECT isbn, title, author, price FROM books WHERE subject = %s"
        self.cursor.execute(query, (subject,))
        books = self.cursor.fetchall()

        print(f"\n{len(books)} books available in this subject\n")

        index = 0
        while index < len(books):
            for i in range(2):
                if index + 1 < len(books):
                    book = books[index + i]
                    print(f"{index + i + 1}. Author: {book[2]}\nTitle: {book[1]}\nISBN: {book[0]}\nPrice: {book[3]}\nSubject: {subject}\n")
            print("Enter ISBN to add to the cart or 'n' to browse more or press ENTER to go back to the menu:")

            option = input("Your Choice: ")

            if option.lower() == 'n':
                index += 2
            elif option:
                quantity = input("Enter Quantity: ")
                self.add_from_cart(option, int(quantity))
            else:
                break

    def add_from_cart(self, isbn, qty):
        print(f"Adding book with ISBN {isbn} to the cart")
        user_id = self.book_store.get_logged_in_user()
        print(f"User ID: {user_id}, ISBN: {isbn}, Quantity: {qty}")
        if user_id is not None:
            self.cart.add_to_cart(user_id, isbn, qty)
            print("******************************************************")
            print(f"Added {qty} book(s) with ISBN {isbn} to the cart")
            print("******************************************************")
        else:
            print("You should log in first!")
