from core.database.database import Database

class TestDatabaseConnection:
    def test_database_connection(self):
        db = Database()
        assert db._connect() == None

    def test_database_disconnection(self):
        db = Database()
        db._connect()
        assert db._disconnect() == None

class TestDatabaseMethods:
    def test_admin_login_right_credentials(self):
        db = Database()
        res = db.validate_login("admin", "admin")
        expected = "admin"
        assert res == expected

    def test_admin_login_wrong_credentials(self):
        db = Database()
        res = db.validate_login("admin", "wrong")
        expected = ""
        assert res == expected