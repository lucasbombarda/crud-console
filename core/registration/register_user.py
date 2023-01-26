from core.database.database import Database
from core.utils.validations import Validations

class RegisterUser:
    def __init__(self, user) -> None:
        self._user = user
        self.db = Database()
        self.validate = Validations()

    def register(self) -> bool:
        _user_info = self._get_user_info()
        
        if self.db.insert_into_user(_user_info):
            return True
            
        return False

    def _get_user_info(self) -> dict:
        try:
            _user_info = {}
            _user_info["active"] = self.validate.inputInt("Usuário ativo? [0/1] - Padrão [1]\n>>> ", "Valor inválido", allowRegex=r"^[0-1]$", blank=True)
            if _user_info["active"] == None or _user_info["active"] == "":
                _user_info["active"] = 1
            
            _user_info["login"] = self.validate.inputStr("Insira o login do usuário:\n>>> ", "Valor inválido, apenas letras e números são válidos", allowRegex=r"^[\w\d]*$")
            _user_info["password"] = self.validate.inputStr("Insira a senha do usuário:\n>>> ", "Valor inválido, apenas letras e números são válidos", allowRegex=r"^[\w\d]*$")
            
            _user_info["name"] = self.validate.inputStr("Insira o nome do usuário:\n>>> ", "Valor inválido")
            _user_info["email"] = self.validate.inputEmail("Insira o email do usuário:\n>>> ", "Valor inválido")
            _user_info["registration_id"] = self.validate.inputStr("Insira o CPF do usuário:\n>>> ", "Valor inválido")

            return _user_info

        except Exception:
            return {}