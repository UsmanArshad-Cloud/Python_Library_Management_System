import pickle


class Book:
    def __init__(self, title="", author="", category=""):
        self.BookId = 0
        self.BookTitle = title
        self.BookAuthor = author
        self.Availability = True
        self.Category = category
        self.Borrower = ""
        self.Borrowed_Date = ""
        self.Returning_Date = ""
        self.IsDeleted = False

    def __str__(self):
        return f"Book's Id is {self.BookId} ,Book's Title:{self.BookTitle},Book's Author:{self.BookAuthor}," \
               f" Book's Category:{self.Category}, Book's Availability:{self.Availability},Borrower:{self.Borrower}"

