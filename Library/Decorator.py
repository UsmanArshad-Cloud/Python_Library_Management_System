def decorator(func):
    def wrapper(*args, **kwargs):
        #args[0].book_list = args[0].read_books_from_file()
        func(*args, **kwargs)
        # args[0].save_books_to_file()

    return wrapper
