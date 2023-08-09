from User.User import User


class SimpleUser(User):
    def __init__(self, username="", pwd="", phn_no=""):
        super().__init__(username, pwd, phn_no)

    def handle_input(self, user_input, library):
        match user_input:
            case 1:
                Id = int(input("Enter the Id of the Book you want to search"))
                book = library.search_book_by_id(Id)
                if book:
                    print(f"{book}")
                else:
                    print("Id of the Book is Incorrect")
            case 2:
                Title = input("Enter the Title of the Book(May or May not be Specific)")
                books = library.search_books_by_title(Title)
                if len(books) >= 1:
                    for book in books:
                        print(book)
                else:
                    print("No Book has the given keyword in their Title")

    def print_options(self):
        print(f"""
                 Hey {self.Username}
                -Enter 1 to Search the Book with the Id:
                -Enter 2 to Search the Book with the Title Name:
                """)
