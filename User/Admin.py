from User.User import User
from User.UserManager import UserManager


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
                    Id = int(input("Enter the Id of the Book you want to update:"))
                    book = library.search_book_by_id(Id)
                    updated_user = library.get_updated_book_data(book)
                    library.update_book(Id, updated_user)
                case 3:
                    Id = int(input("Enter the Id of the Book you want to know about:"))
                    book = library.search_book_by_id(Id)
                    print(book) if book else print("No Book against this id")
                case 4:
                    Id = int(input("Enter the Id of the Book you want to delete:"))
                    book = library.search_book_by_id(Id)
                    library.remove_book(Id)
                case 5:
                    Borrower_Username = input("Enter the Borrower's UserName:")
                    Book_Id = int(input("Enter the Book's Id:"))
                    curr_lib = library
                    book = curr_lib.search_book_by_id(Book_Id)
                    user = UserManager.get_user_from_db(Borrower_Username)
                    if book and user:
                        curr_lib.assign_book(book, user)
                    else:
                        print("Entered Book or User doesn't exists")
                case 6:
                    Borrower_Username = input("Enter the Borrower's UserName:")
                    Book_Id = int(input("Enter the Book's Id:"))
                    curr_lib = library
                    book = curr_lib.search_book_by_id(Book_Id)
                    user = UserManager.get_user_from_db(Borrower_Username)
                    curr_lib.return_book(book, user)
                case 7:
                    curr_lib = library
                    assigned_books = curr_lib.get_all_assigned_books()
                    for book in assigned_books:
                        print(book)
                case 8:
                    curr_lib = library
                    not_returned_book = curr_lib.get_all_non_returned_books()
                    for book in not_returned_book:
                        print(book)
                    pass
                case _:
                    print("Good Bye!!! Admin")
                    return
        except Exception as e:
            print("Error Occurred", e)

