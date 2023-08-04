from Library.Library import Library
from User.Admin import Admin
from User.SimpleUser import SimpleUser
from User.User import User
from User.UserManager import UserManager

library = Library()
user_mgr = UserManager(library)
isUserSignedIn = False
curr_user = User()
while not isUserSignedIn:
    print("Press 1 to Log In:")
    print("Press any other Number to Sign Up:")
    user_input = 0
    while True:
        try:
            user_input = int(input("Enter Your Option:"))
            break
        except ValueError:
            print("Input must be a proper Input")
    while not isUserSignedIn:
        if user_input == 1:
            isUserSignedIn, curr_user = user_mgr.sign_in()
        else:
            is_signed_up = user_mgr.sign_up()
            if is_signed_up:
                isUserSignedIn, curr_user = user_mgr.sign_in()

    user_input = 1
    while 1 <= user_input <= 8:
        try:
            curr_user = Admin() if curr_user.Username == "Admin" else SimpleUser()
            curr_user.print_options()
            user_input = int(input("Enter Your Option:"))
        except ValueError:
            print("Enter a Valid Integer")
        curr_user.handle_input(user_input, library)
