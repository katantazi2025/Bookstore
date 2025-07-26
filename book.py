# Import necessary modules
# from mysql.connector import connect  # Uncomment if needed
from cart import Cart  # Import Cart class to handle cart-related operations


class Book:
    def __init__(self, conn, cursor, book_store, cart, memberregister):
        """
        Initialize the Book class with database connection, cursor,
        store instance, cart instance, and member registration handler.
        """
        self.conn = conn
        self.cursor = cursor
        self.book_store = book_store
        self.cart = Cart(conn, cursor, user_id=None, book_store=self.book_store, memberregister=memberregister)
        self.memberregister = memberregister

    def browse_by_subject(self):
        """
        Allow users to browse books categorized by subject.
        Display a sorted list of subjects and prompt user to select one.
        """
        print("Browsing by subject....")
        subjects = self.get_all_subjects()
        subjects.sort()  # Sort subjects alphabetically

        # Display subjects with indices
        for index, subject in enumerate(subjects, start=1):
            print(f"{index}. {subject}")

        chosen_subject_index = input("Enter your choice: ")

        try:
            # Get subject name based on user's index choice
            chosen_subject_index = int(chosen_subject_index)
            chosen_subject = subjects[chosen_subject_index - 1]
            self.display_books_by_subject(chosen_subject)
        except (ValueError, IndexError):
            print("Invalid choice. Returning to the main menu.")

    def get_all_subjects(self):
        """
        Fetch all unique subjects from the books table.
        """
        print(f"Before execute - conn: {self.conn}, cursor: {self.cursor}")
        query = "SELECT DISTINCT subject FROM books ORDER BY subject"
        self.cursor.execute(query)
        subjects = [row[0] for row in self.cursor.fetchall()]
        print(f"After execute - conn: {self.conn}, cursor: {self.cursor}")
        return subjects

    def display_books_by_subject(self, subject):
        """
        Display all books for a given subject.
        Allows the user to navigate through pages of books and add books to the cart.
        """
        query = "SELECT isbn, title, author, price FROM books WHERE subject = %s"
        self.cursor.execute(query, (subject,))
        books = self.cursor.fetchall()

        print(f"\n{len(books)} books available in this subject\n")

        index = 0
        while index < len(books):
            # Display 2 books at a time
            for i in range(2):
                if index + i < len(books):
                    book = books[index + i]
                    print(f"{index + i + 1}. Author: {book[2]}\nTitle: {book[1]}\nISBN: {book[0]}\nPrice: {book[3]}\nSubject: {subject}\n")

            # Prompt user to take action
            print("Enter ISBN to add to the cart or 'n' to browse more or press ENTER to go back to the menu:")
            option = input("Your Choice: ")

            if option.lower() == 'n':
                index += 2  # Go to the next pair of books
            elif option:
                quantity = input("Enter Quantity: ")
                self.add_from_cart(option, int(quantity))  # Add book to cart
            else:
                break  # Return to menu

    def add_from_cart(self, isbn, qty):
        """
        Add selected book to the user's cart.
        """
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
