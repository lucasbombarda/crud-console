from database.database import Database

class ListPriceList:
    def __init__(self, user) -> None:
        self._user = user
        self.db = Database()

    def list_price_list(self) -> list:
        return self.db.get_price_list_info()