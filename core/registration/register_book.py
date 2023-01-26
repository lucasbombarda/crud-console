from core.database.database import Database
from core.utils.validations import Validations
from core.utils.cls import cls

class RegisterBook:
    def __init__(self, user:str) -> None:
        self._user = user
        self.db = Database()
        self.validate = Validations()

    def register(self) -> bool:
        _book_info = self._get_book_information()

        if _book_info == {}:
            return False

        if self.db.insert_into_book(_book_info):
            return True
        return False

    def _get_book_information(self) -> dict:
        try:
            _book_info = {}
            _book_info["active"] = self.validate.inputInt("Livro ativo? [0/1] - Padrão [1]\n>>> ", "Valor inválido", allowRegex=r"^[0-1]$", blank=True)
            if _book_info["active"] == None or _book_info["active"] == "":
                _book_info["active"] = 1
            
            _book_info["title"] = self.validate.inputStr("Insira o título do livro:\n>>> ", "Valor inválido", blank=False)
            _book_info["author"] = self.validate.inputStr("Insira o autor do livro:\n>>> ", "Valor inválido", blank=False)
            
            _book_info["buy"] = self.validate.inputInt("Compra? [0/1] - Padrão [1]\n>>> ", "Valor inválido", allowRegex=r"^[0-1]$", blank=True)
            if _book_info["buy"] == None or _book_info["buy"] == "":
                _book_info["buy"] = 1

            _book_info["sell"] = self.validate.inputInt("Vende? [0/1] - Padrão [1]\n>>> ", "Valor inválido", allowRegex=r"^[0-1]$", blank=True)
            if _book_info["sell"] == None or _book_info["sell"] == "":
                _book_info["sell"] = 1
            
            _book_info["publisher_id"] = self._get_publisher()

            return _book_info

        except KeyboardInterrupt:
            return {}

    def _get_publisher(self) -> int:
        while True:
            _publisher_id = self.validate.inputInt("Insira o código da editora:\n>>> ", "Valor inválido")

            if self.db.verify_publisher_exists_by_id(_publisher_id):
                if self._confirm_publisher(_publisher_id):
                    return _publisher_id
            else:
                input("Editora não existe.")

    def _confirm_publisher(self, publisher_id) -> bool:
        cls()
        _info = self.db._publisher_info(publisher_id)
        print(f"Código: {_info[0]}\nEditora: {_info[1]}\n\n")
        _res = self.validate.inputStr("Confirma editora? [S/N]\n>>> ", "Valor inválido", allowRegex=r"^(S|N)|(s|n)$")
        
        if _res.upper() == "S":
            cls()
            return True
        return False