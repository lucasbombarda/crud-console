from core.database.database import Database
from core.utils.validations import Validations

class RegisterPriceList:
    def __init__(self, user) -> None:
        self._user = user
        self.db = Database()
        self.validate = Validations()

    def register(self) -> bool:
        price_list_info = self._get_price_list_information()

        if price_list_info == {}:
            return False
        
        if self.db.insert_into_price_list(price_list_info):
            return True

        return False

    def _get_price_list_information(self) -> dict:
        try:
            _price_list_info = {}

            _price_list_info["active"] = self.validate.inputInt("Tabela ativa? [0/1] - Padrão [1]\n>>> ", "Valor inválido", allowRegex=r"^[0-1]$", blank=True)
            if _price_list_info["active"] == None or _price_list_info["active"] == "":
                _price_list_info["active"] = 1
            
            _price_list_info["name"] = self.validate.inputStr("Insira a nome da tabela de preços:\n>>> ", "Valor inválido")

            return _price_list_info
            
        except KeyboardInterrupt:
            return {}