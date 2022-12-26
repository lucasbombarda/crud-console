from database.database import Database

class ListLocals():
    def __init__(self, user) -> None:
        self._user = user
        self.db = Database()

    def list_local(self) -> list:
        return self.db.get_local_info()