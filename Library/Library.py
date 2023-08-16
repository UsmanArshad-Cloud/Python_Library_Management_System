import sys

from Book.book import Book
from Library.Decorator import decorator
from datetime import date, timedelta
import pickle

from User.UserManager import UserManager


class Library:
    def __init__(self):
        self.books = []  # For holding All the Books
        self.book_pos = []  # For holding Books Position
        self.read_books_pos_from_file()  # Read All Books Positions from File
        self.read_books_from_file()  # Read All Books from File
        self.users = UserManager.read_users_file()  # Read All Users

    # Book Handling

    @decorator
    def addbook(self, book):
        max_id = self.get_maximum_id_from_file()  # Get MAX id from the Books List
        book.BookId = max_id + 1
        self.books.append(book)  # Update the Books List Locally
        with open('Books.bin', "ab") as f:
            self.book_pos.append(max_id * 500)
            pickled_book = pickle.dumps(book)  # Serialize the Book Object
            padding_size = 500 - len(pickled_book)
            if padding_size > 0:
                pickled_book += b'\x00' * padding_size  # Padding with null bytes

            f.write(pickled_book)  # Add the new Book into File
        self.save_book_pos_to_file()

    @decorator
    def update_book(self, book_id, updated_book):
        with open('Books.bin', "rb+") as f:
            book_pos = self.book_pos[book_id - 1]  # Get the Book based on the id
            f.seek(book_pos)
            book = pickle.load(f)  # Load the object from that specific position
            if not book.IsDeleted:
                book = updated_book
                book.BookId = book_id
                f.seek(book_pos)
                pickle.dump(book, f)  # Update the Book in the File

    @decorator
    def remove_book(self, book_id):
        with open('Books.bin', "rb+") as f:
            book_pos = self.book_pos[book_id - 1]  # Get Position of the object in the file
            f.seek(book_pos)
            book = pickle.load(f)
            if not book.IsDeleted:
                book.IsDeleted = True  # UnCheck the IsDeleted to ensure the Safe Delete
                f.seek(book_pos)
                pickle.dump(book, f)

    def assign_book(self, book, user):
        if book.Availability and not book.IsDeleted:
            today = date.today()
            book.Availability = False
            book.Borrowed_Date = today  # Update Book Data
            book.Returning_Date = today + timedelta(weeks=1)
            book.Borrower = user.Username
            with open('Books.bin', "rb+") as f:
                book_pos = self.book_pos[book.BookId - 1]
                f.seek(book_pos)  # Update the File
                pickle.dump(book, f)
            print(
                f"{book.BookTitle} is assigned to {user.Username}.Book must be returned book before {book.Returning_Date}")
        else:
            print(F"{book.BookTitle} is currently not available")

    def return_book(self, book, user):
        if not book.Availability and not book.IsDeleted:
            today = date.today()
            book.Availability = True
            book.Borrower = ""
            book.Borrowed_Date = ""
            if book.Returning_Date < today:
                print(f"{user.Username} was late in returning the book.Adding fine to his account")
                UserManager.add_fine_to_user(user)
            else:
                print(f"{book.BookTitle} returned successfully")
            with open('Books.bin', "rb+") as f:
                book_pos = self.book_pos[book.BookId - 1]
                f.seek(book_pos)
                pickle.dump(book, f)
        else:
            print("You can't return a book that is not borrowed")

    def read_books_from_file(self):
        with open('Books.bin', "rb") as f:
            index = 0
            try:
                while f.tell() <= self.book_pos[len(self.book_pos) - 1]:
                    f.seek(index * 500)
                    obj = pickle.load(f)
                    self.books.append(obj)
                    index += 1
            except EOFError:
                # End of file reached
                pass
            except IndexError:
                self.books = []

    @staticmethod
    def get_updated_book_data(curr_book):
        updated_book = curr_book
        print("Book You selected to update is:", curr_book)
        Title = input("Update Book Title/or Just Press Enter")
        Author = input("Update Book Author/or Just Press Enter")
        updated_book.BookTitle = Title if Title else curr_book.BookTitle
        updated_book.BookAuthor = Author if Author else curr_book.BookAuthor
        return updated_book

    def input_book(self):
        book = Book()
        book.BookTitle = input("Enter Book Title:")
        book.BookAuthor = input("Enter Book Author:")
        book.Category = input("Enter Book Category(Fiction/Non-Fiction/Science/Arts/History:)")
        return book

    def get_maximum_id_from_file(self):
        max_id = len(self.book_pos)
        return max_id

    # Simple User Methods
    def search_book_by_id(self, book_id):
        with open('Books.bin', "rb+") as f:
            try:
                book_pos = (book_id - 1) * 500
                f.seek(book_pos)
                record = f.read(500)
                book = pickle.loads(record.strip(b'\x00'))  # Evacuating the null bytes
                if not book.IsDeleted:
                    return book
            except pickle.PickleError:
                print("There is an error in loading the object")

    def search_books_by_title(self, title):
        books = []
        self.books = []
        self.read_books_from_file()
        for book in self.books:
            if title.lower() in book.BookTitle.lower() and not book.IsDeleted:
                books.append(book)
        return books

    # Assigning and Returning Books
    @staticmethod
    def isAssigned(book):
        return not book.IsDeleted and not book.Availability

    @staticmethod
    def is_not_returned(book):
        today = date.today()
        return book if book.Returning_Date != "" and book.Returning_Date < today and not book.IsDeleted else None

    def get_all_assigned_books(self):
        self.books = []
        self.read_books_from_file()
        return list(filter(Library.isAssigned, self.books))

    def get_all_non_returned_books(self):
        self.books = []
        self.read_books_from_file()
        return list(filter(Library.is_not_returned, self.books))

    def save_book_pos_to_file(self):
        with open("Position.txt", "w") as file:
            positions = ','.join(map(str, self.book_pos))
            file.write(positions + "\n")

    def read_books_pos_from_file(self):
        with open("Position.txt", "r") as file:
            for line in file:
                positions = line.strip().split(',')
                self.book_pos = [int(pos) for pos in positions]

    @staticmethod
    def input_book_id(option):
        id_input = int(input(f"Enter the Id of the Book you want to {option}:"))
        return id_input

    @staticmethod
    def input_borrower():
        Borrower_Username = input("Enter the Borrower's UserName:")
        Book_Id = int(input("Enter the Book's Id:"))
        return Borrower_Username, Book_Id
