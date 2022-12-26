from database.database import Database

class RegisterPriceList:
    def __init__(self, user) -> None:
        self._user = user
        self.db = Database()