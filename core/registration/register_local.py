from core.database.database import Database
from core.utils.validations import Validations

class RegisterLocal:
    def __init__(self, user) -> None:
        self._user = user
        self.db = Database()
        self.validate = Validations()

    def register(self) -> bool:
        local_info = self._get_local_information()

        if local_info == {}:
            return False
        
        if self.db.insert_into_local(local_info):
            return True

        return False

    def _get_local_information(self) -> dict:
        try:
            local_info = {}

            local_info["active"] = self.validate.inputInt("Local ativo? [0/1] - Padrão [1]\n>>> ", "Valor inválido", allowRegex=r"^[0-1]$", blank=True)
            if local_info["active"] == None or local_info["active"] == "":
                local_info["active"] = 1
            
            local_info["description"] = self.validate.inputStr("Insira a descrição do local:\n>>> ", "Valor inválido")

            return local_info
        except KeyboardInterrupt:
            return {}