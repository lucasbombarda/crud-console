from database.database import Database
from utils.validations import Validations

class RegisterPublisher:
    def __init__(self, user) -> None:
        self._user = user
        self.db = Database()
        self.validate = Validations()

    def register(self) -> bool:
        _publisher_info = self._get_publisher_info()

        if _publisher_info == {}:
            return False

        if self.db.insert_into_publisher(_publisher_info):
            return True
        return False

    def _get_publisher_info(self) -> dict:
        try:
            _publisher_info = {}

            _publisher_info["active"] = self.validate.inputInt("Editora ativa? [0/1] - Padrão [1]\n>>> ", "Valor inválido", allowRegex=r"^[0-1]$", blank=True)
            if _publisher_info["active"] == None or _publisher_info["active"] == "":
                _publisher_info["active"] = 1
            
            _publisher_info["name"] = self.validate.inputStr("Insira o nome da editora:\n>>> ", "Valor inválido")

            return _publisher_info
        except KeyboardInterrupt:
            return {}
