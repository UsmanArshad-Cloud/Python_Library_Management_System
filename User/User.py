from abc import ABC, abstractmethod


class User:
    def __init__(self, username="", pwd="", phn_no=""):
        self.Username = username
        self.Password = pwd
        self.PhoneNum = phn_no
        self.Fine = 0
        self.Borrowed = []

    def __str__(self):
        return f"Username:{self.Username},Password:{self.Password},PhoneNum:{self.PhoneNum},Fine:{self.Fine}"

    @abstractmethod
    def handle_input(self, user_input, library):
        pass

    @abstractmethod
    def print_options(self):
        pass
