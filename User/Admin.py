from User.User import User
from User.UserManager import UserManager
from Library.Library import Library


class Admin(User):
    def __init__(self, username="Admin", pwd="", phn_no=""):
        super().__init__(username, pwd, phn_no)

    def print_options(self):
        print("""
        -Enter 1 to Add a Book
        -Enter 2 to Update an Existing Book
        -Enter 3 to Read a Book
        -Enter 4 to Delete an Existing Book
        -Enter 5 to Assign a Book to the User
        -Enter 6 to Return a Book
        -Enter 7 to View All Assigned Books
        -Enter 8 to View All Books that are not returned
        -Enter Press Any Other key to exit
        """)

    def handle_input(self, admin_input, library):
        try:
            match admin_input:
                case 1:
                    book = library.input_book()
                    library.addbook(book)
                case 2:
                    Id = library.input_book_id("Update")
                    book = library.search_book_by_id(Id)
                    updated_user = library.get_updated_book_data(book)
                    library.update_book(Id, updated_user)
                case 3:
                    Id = Library.input_book_id("Read")
                    book = library.search_book_by_id(Id)
                    print(book) if book else print("No Book against this id")
                case 4:
                    Id = Library.input_book_id("Delete")
                    library.remove_book(Id)
                case 5:
                    Borrower_Username, Book_Id = Library.input_borrower()
                    book = library.search_book_by_id(Book_Id)
                    user = UserManager.get_user_from_db(Borrower_Username)
                    library.assign_book(book, user)
                case 6:
                    Borrower_Username, Book_Id = Library.input_borrower()
                    book = library.search_book_by_id(Book_Id)
                    user = UserManager.get_user_from_db(Borrower_Username)
                    library.return_book(book, user)
                case 7:
                    assigned_books = library.get_all_assigned_books()
                    for book in assigned_books:
                        print(book)
                case 8:
                    not_returned_book = library.get_all_non_returned_books()
                    for book in not_returned_book:
                        print(book)
                case _:
                    print("Good Bye!!! Admin")
                    return
        except Exception as e:
            print("Error Occurred:", e)
