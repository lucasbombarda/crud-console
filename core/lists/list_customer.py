from core.database.database import Database

class ListCustomer():
    def __init__(self, user) -> None:
        self._user = user
        self.db = Database()

    def list_customers(self) -> list:
        return self.db.get_customer_info()