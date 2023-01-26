from core.database.database import Database
from core.utils.validations import Validations
from core.utils.cls import cls

class RegisterCustomer:
    def __init__(self, user) -> None:
        self._user = user
        self.db = Database()
        self.validate = Validations()

    def register(self) -> bool:
        _customer_info = self._get_customer_info()
        _address_info = self._get_address_info()
        _contact_info = self._get_contact_info()

        if {} in (_customer_info, _address_info, _contact_info):
            return False

        if self.db.insert_into_customer(_customer_info, _address_info, _contact_info):
            return True
            
        return False

    def _get_customer_info(self) -> dict:
        try:
            _customer_info = {}
            
            _customer_info["active"] = self.validate.inputInt("Cliente ativo? [0/1] - Padrão [1]\n>>> ", "Valor inválido", allowRegex=r"^[0-1]$", blank=True)
            if _customer_info["active"] == None or _customer_info["active"] == "":
                _customer_info["active"] = 1
            
            _customer_info["name"] = self.validate.inputStr("Insira o nome do cliente:\n>>> ", "Valor inválido")
            _customer_info["email"] = self.validate.inputEmail("Insira o email do cliente:\n>>> ", "Valor inválido")
            _customer_info["registration_id"] = self.validate.inputStr("Insira o CPF do cliente:\n>>> ", "Valor inválido", allowRegex=r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})")
        
            return _customer_info
        except Exception:
            return {}

    def _get_address_info(self) -> dict:
        try:
            _address_info = {}
            _address_info["street_name"] = self.validate.inputStr("Insira o nome da rua:\n>>> ", "Valor inválido")
            _address_info["number"] = self.validate.inputInt("Insira o número:\n>>> ", "Valor inválido")
            _address_info["city"] = self.validate.inputStr("Insira a cidade:\n>>> ", "Valor inválido")
            _address_info["state"] = self.validate.inputStr("Insira a sigla do estado:\n>>> ", "Valor inválido", allowRegex=r"^(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)|(ac|al|ap|am|ba|ce|df|es|go|ma|mt|ms|mg|pa|pb|pr|pe|pi|rj|rn|rs|ro|rr|sc|sp|se|to)$")
            _address_info["street_id"] = self.validate.inputStr("Insira o CEP:\n>>> ", "Valor inválido", allowRegex=r"\d{8}$")
            _address_info["reference"] = self.validate.inputStr("Insira o complemento:\n>>> ", "Valor inválido", blank=True)

            return _address_info
        except Exception:
            return {}

    def _get_contact_info(self) -> dict:
        try:
            _contact_info = {}
            _contact_info["contact_type"] = self.validate.inputStr("Insira o tipo do contato [CO/PE]:\n>>> ", "Valor inválido", allowRegex=r"^(CO|PE)|(co|pe)$")
            _contact_info["ddd"] = self.validate.inputInt("Insira o DDD:\n>>> ", "Valor inválido", allowRegex=r"\d{2}$")
            _contact_info["tel_number"] = self.validate.inputInt("Insira o número do telefone/celular:\n>>> ", "Valor inválido", allowRegex=r"\d{8}$|\d{9}$")
            
            _contact_info["active_number"] = self.validate.inputInt("Número ativo? [0/1] - Padrão [1]\n>>> ", "Valor inválido", allowRegex=r"[0-1]$", blank=True)
            if _contact_info["active_number"] == None or _contact_info["active_number"] == "":
                _contact_info["active_number"] = 1

            return _contact_info
        except Exception:
            return {}

class RegisterCustomerContact:
    def __init__(self, user) -> None:
        self._user = user
        self.db = Database()
        self.validate = Validations()

    def register(self) -> bool:
        _customer_id = self._get_customer_id()

        _registration = RegisterCustomer(self._user)
        _contact_info = _registration._get_contact_info()

        if self.db.insert_contact_info(_customer_id, _contact_info):
            return True
        return False

    def _get_customer_id(self) -> int:
        while True:
            cls()
            _customer_id = self.validate.inputInt("Insira o código do cliente que deseja adicionar um contato:\n>>>", "Valor inválido")

            if self.db.verify_customer_exists_by_id(_customer_id):
                if self._confirm_customer(_customer_id):
                    return _customer_id
            else:
                input("Cliente não existe!")

    def _confirm_customer(self, customer_id) -> bool:
        cls()
        _info = self.db._customer_info(customer_id)
        print(f"Código: {_info[0]}\nCliente: {_info[1]}\nCPF: {_info[2]}\n\n")
        _res = self.validate.inputStr("Confirma cliente? [S/N]\n>>> ", "Valor inválido", allowRegex=r"^(S|N)|(s|n)$")
        
        if _res.upper() == "S":
            cls()
            return True
        return False