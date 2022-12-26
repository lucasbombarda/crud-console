from database.database import Database

class ListBooks():
    def __init__(self, user) -> None:
        self._user = user
        self.db = Database()

    def list_books(self) -> list:
        return self.db.get_books_info()