from core.database.database import Database
from core.utils.validations import Validations
from core.utils.cls import cls

class SearchCustomer:
    def __init__(self, user) -> None:
        self._user = user

    def search(self, columns_to_filter) -> list:
        db = Database()
        _filters_values = self.get_search_info(columns_to_filter)
        _customers, _cols = db.search_customer_with_filters(_filters_values)

        return _customers, _cols
    
    def get_search_info(self, columns_to_filter=[]) -> dict:
        columns = []
        for _column_name in columns_to_filter:
            columns.append(_column_name[1])

        customer_id = active = name = email = registration_id = street_name = number = city = state = street_id = reference = contact_type = ddd = tel_number = active_number = ""
        val = Validations()
        info = {}

        cls()

        if "customer_id" in columns:
            customer_id = val.inputStr("Insira o filtro código do cliente:\n>>> ", "Valor incorreto.", blank=True)
        if "active" in columns:
            active = val.inputStr("Insira o filtro cliente ativo:\n>>> ", "Valor incorreto.", blank=True)
        if "name" in columns:
            name = val.inputStr("Insira o filtro nome do cliente:\n>>> ", "Valor incorreto.", blank=True)
        if "email" in columns:
            email = val.inputStr("Insira o filtro e-mail:\n>>> ", "Valor incorreto.", blank=True)
        if "registration_id" in columns:
            registration_id = val.inputStr("Insira o filtro CPF:\n>>> ", "Valor incorreto.", blank=True)
        if "street_name" in columns:
            street_name = val.inputStr("Insira o filtro nome da rua:\n>>> ", "Valor incorreto.", blank=True)
        if "number" in columns:
            number = val.inputStr("Insira o filtro número da residência:\n>>> ", "Valor incorreto.", blank=True)
        if "city" in columns:
            city = val.inputStr("Insira o filtro cidade:\n>>> ", "Valor incorreto.", blank=True)
        if "state" in columns:
            state = val.inputStr("Insira o filtro estado:\n>>> ", "Valor incorreto.", blank=True)
        if "street_id" in columns:
            street_id = val.inputStr("Insira o filtro CEP:\n>>> ", "Valor incorreto.", blank=True)
        if "reference" in columns:
            reference = val.inputStr("Insira o filtro complemento:\n>>> ", "Valor incorreto.", blank=True)
        if "contact_type" in columns:
            contact_type = val.inputStr("Insira o filtro tipo de contato [CO/RE]:\n>>> ", "Valor incorreto.", blank=True)
        if "ddd" in columns:
            ddd = val.inputStr("Insira o filtro DDD:\n>>> ", "Valor incorreto.", blank=True)
        if "tel_number" in columns:
            tel_number = val.inputStr("Insira o filtro número do contato:\n>>> ", "Valor incorreto.", blank=True)
        if "active_number" in columns:
            active_number = val.inputStr("Insira o filtro contato ativo:\n>>> ", "Valor incorreto.", blank=True)


        info["customer_id"] = customer_id
        info["active"] = active
        info["name"] = name
        info["email"] = email
        info["registration_id"] = registration_id
        info["street_name"] = street_name
        info["number"] = number
        info["city"] = city
        info["state"] = state
        info["street_id"] = street_id
        info["reference"] = reference
        info["contact_type"] = contact_type
        info["ddd"] = ddd
        info["tel_number"] = tel_number
        info["active_number"] = active_number

        return info