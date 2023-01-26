from core.utils.constants import LIBRARY_NAME
from core.database.database import Database
from getpass import getpass
from art import tprint
from core.menu import Menus
from core.utils.cls import cls

class Login:
    def __init__(self) -> None:
        self.db = Database()

    def user_login(self) -> str:
        while True:
            try:
                cls()
                tprint(LIBRARY_NAME)
                __login = input("Login: ")
                __passwd = getpass("Senha: ")

                __user = self.db.validate_login(__login, __passwd)
                if __user:
                    return Menus(__user)

                input("Usuário ou senha incorretos.")

            except KeyboardInterrupt:
                cls()
                input("Saindo do sistema...")
                break
