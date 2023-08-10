import sys

from Book.book import Book
from Library.Decorator import decorator
from datetime import date, timedelta
import pickle

from User.UserManager import UserManager


class Library:
    def __init__(self):
        self.books = self.read_books_from_file()
        self.users = UserManager.read_users_file()

    # Book Handling

    @decorator
    def addbook(self, book):
        max_id = self.get_maximum_id_from_file()
        book.BookId = max_id + 1
        self.books.append(book)

    @decorator
    def update_book(self, book_id, updated_book):
        index = 0
        for book_ in self.books:
            if book_.BookId == book_id and not book_.IsDeleted:
                book_ = updated_book
                book_.BookId = book_id
                self.books[index] = book_
                break
            index = index + 1

    @decorator
    def remove_book(self, id):
        for book_ in self.books:
            if book_.BookId == id and not book_.IsDeleted:
                book_.IsDeleted = True

    def assign_book(self, book, user, index):
        if book.Availability and not book.IsDeleted:
            today = date.today()
            book.Availability = False
            book.Borrowed_Date = today
            book.Returning_Date = today + timedelta(weeks=1)
            book.Borrower = user.Username
            self.books[index] = book
            self.save_books_to_file()
            print(
                f"{book.BookTitle} is assigned to {user.Username}.Book must be returned book before {book.Returning_Date}")
        else:
            print(F"{book.BookTitle} is currently not available")

    def return_book(self, book, user, index):
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
            self.books[index] = book
            self.save_books_to_file()
        else:
            print("You can't return a book that is not borrowed")

    # File Handling

    def save_books_to_file(self):
        with open("Books.bin", 'wb') as f:
            pickle.dump(self.books, f, pickle.HIGHEST_PROTOCOL)

    def read_books_from_file(self):
        try:
            with open("Books.bin", 'rb') as f:
                self.books = pickle.load(f)
        except FileNotFoundError:
            self.books = []
        return self.books

    def get_updated_book_data(self, curr_book):
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
        books = self.read_books_from_file()
        max_id = 0
        for book in books:
            max_id = book.BookId if book.BookId > max_id else max_id
        return max_id

    # Simple User Methods
    def search_book_by_id(self, book_id):
        index = 0
        books = self.read_books_from_file()
        for book in books:
            print(sys.getsizeof(book))
            if book.BookId == book_id and not book.IsDeleted:
                return book, index
            index += 1
        print("No such book against this Id")
        return None, index

    def search_books_by_title(self, title):
        books = []
        self.books = self.read_books_from_file()
        for book in self.books:
            if title.lower() in book.BookTitle.lower() and not book.IsDeleted:
                books.append(book)
        return books

    # Assigning and Returning Books
    @staticmethod
    def isAssigned(book):
        return None if book.Availability or book.IsDeleted else book

    @staticmethod
    def is_not_returned(book):
        today = date.today()
        return book if book.Returning_Date != "" and book.Returning_Date < today and not book.IsDeleted else None

    def get_all_assigned_books(self):
        books = self.read_books_from_file()
        return list(filter(Library.isAssigned, books))

    def get_all_non_returned_books(self):
        books = self.read_books_from_file()
        return list(filter(Library.is_not_returned, books))
