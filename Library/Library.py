import sys

from Book.book import Book
from Library.Decorator import decorator
from datetime import date, timedelta
import pickle

from User.UserManager import UserManager


class Library:
    def __init__(self):
        self.books = []
        self.book_pos = []
        self.read_books_pos_from_file()
        self.read_books_from_file()
        self.users = UserManager.read_users_file()

    # Book Handling

    @decorator
    def addbook(self, book):
        max_id = self.get_maximum_id_from_file()
        book.BookId = max_id + 1
        self.books.append(book)
        with open('Books.pkl', "ab") as f:
            self.book_pos.append(f.tell())
            pickle.dump(book, f)
        self.save_book_pos_to_file()

    @decorator
    def update_book(self, book_id, updated_book):
        with open('Books.pkl', "rb+") as f:
            book_pos = self.book_pos[book_id - 1]
            f.seek(book_pos)
            book = pickle.load(f)
            if not book.IsDeleted:
                book = updated_book
                book.BookId = book_id
                f.seek(book_pos)
                pickle.dump(book, f)

    @decorator
    def remove_book(self, book_id):
        with open('Books.pkl', "rb+") as f:
            book_pos = self.book_pos[book_id - 1]
            f.seek(book_pos)
            book = pickle.load(f)
            if not book.IsDeleted:
                book.IsDeleted = True
                f.seek(book_pos)
                pickle.dump(book, f)

    def assign_book(self, book, user):
        if book.Availability and not book.IsDeleted:
            today = date.today()
            book.Availability = False
            book.Borrowed_Date = today
            book.Returning_Date = today + timedelta(weeks=1)
            book.Borrower = user.Username
            with open('Books.pkl', "rb+") as f:
                book_pos = self.book_pos[book.BookId - 1]
                f.seek(book_pos)
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
            with open('Books.pkl', "rb+") as f:
                book_pos = self.book_pos[book.BookId - 1]
                f.seek(book_pos)
                pickle.dump(book, f)
        else:
            print("You can't return a book that is not borrowed")

    def read_books_from_file(self):
        with open('Books.pkl', "rb") as f:
            index = 0
            try:
                while f.tell() <= self.book_pos[len(self.book_pos) - 1]:
                    obj = pickle.load(f)
                    self.books.append(obj)
            except EOFError:
                # End of file reached
                pass
            except IndexError:
                self.books=[]


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
        print("Maximum Id", max_id)
        return max_id

    # Simple User Methods
    def search_book_by_id(self, book_id):
        with open('Books.pkl', "rb+") as f:
            for item in self.book_pos:
                print(item)
                book_pos = self.book_pos[book_id - 1]
                f.seek(book_pos)
                book = pickle.load(f)
                if not book.IsDeleted:
                    return book
        raise IndexError("Id is not correct")

    def search_books_by_title(self, title):
        books = []
        self.read_books_from_file()
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
        self.read_books_from_file()
        return list(filter(Library.isAssigned, self.books))

    def get_all_non_returned_books(self):
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
