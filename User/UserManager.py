from User.User import User
import pickle
import re


class UserManager:
    def __init__(self, library):
        self.library = library

    @staticmethod
    def sign_in():
        print("______Sign In_______")
        username = input("Enter Username:")
        pwd = input("Enter Password:")
        if UserManager.is_username_exists(username) and UserManager.checking_pwd_from_db(username, pwd):
            print("Welcome to the gateway to the Knowledge")
            user = UserManager.get_user_from_db(username)
            return True, user
        else:
            print("Wrong UserName or Password Try Again")
            return False, None

    def sign_up(self):
        print("______Sign Up_______")
        user = User()
        user = UserManager.get_user_info(user)
        check = UserManager.validate_user_info(user)
        self.library.users = UserManager.read_users_file()
        if check:
            self.library.users.append(user)
            with open("Users.bin", 'wb') as f:
                pickle.dump(self.library.users, f, pickle.HIGHEST_PROTOCOL)
            return True
        else:
            print("User not Validated Properly")
        return False

    @staticmethod
    def read_users_file():
        try:
            with open("Users.bin", 'rb') as f:
                users = pickle.load(f)
            return users
        except FileNotFoundError:
            with open("Users.bin", 'wb') as f:
                pickle.dump([], f, pickle.HIGHEST_PROTOCOL)
            with open("Users.bin", 'rb') as f:
                users = pickle.load(f)
            return users

    @staticmethod
    def is_username_exists(username):
        users = UserManager.read_users_file()
        for user in users:
            if user.Username == username:
                return True
        return False

    @staticmethod
    def checking_pwd_from_db(username, pwd):
        users = UserManager.read_users_file()
        for user in users:
            if user.Username == username and user.Password == pwd:
                return True
        return False

    @staticmethod
    def is_pwd_strong(pwd):
        regex_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        return re.search(regex_pattern, pwd)

    @staticmethod
    def get_user_from_db(username):
        users_list = UserManager.read_users_file()
        for user in users_list:
            if user.Username == username:
                return user
        raise LookupError("User not found")
    @staticmethod
    def get_user_info(user):
        user.Username = input("Username:")
        user.Password = input("Password:")
        user.PhoneNum = input("Phone Number:")
        return user

    @staticmethod
    def validate_user_info(user):
        User_existed = UserManager.is_username_exists(user.Username)
        if User_existed:
            print("Username already exists")
            return False
        if not UserManager.is_pwd_strong(user.Password):
            print("""
    Your Password must has minimum 8 characters in length,at least one uppercase English letter,at least one lowercase
    English letter,at least one digit and at least one special character
                """)
            return False
        else:
            print("User Validated")
        return True

    @staticmethod
    def add_fine_to_user(user_arg):
        users = UserManager.read_users_file()
        for user in users:
            if user.Username == user_arg:
                user.fine += 200
                break
        with open("Users.bin", 'wb') as f:
            pickle.dump(users, f, pickle.HIGHEST_PROTOCOL)
        return user_arg

