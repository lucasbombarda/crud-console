from art import tprint
from tabulate import tabulate
from utils.constants import LIBRARY_NAME
from registration import register_user, register_book, register_customer, register_local, register_order, register_price_list, register_publisher
from lists import list_books, list_customers, list_local
from utils.cls import cls

class Menus:
    def __init__(self, user:str) -> None:
        self._user = user

        self.redirect_to_action()

    def _main_header(self, name):
        cls()
        tprint(name)    
        print(f"Usuário: {self._user}\n")

    def _menu_header(self):
        self._main_header(LIBRARY_NAME)

        _headers = ["Opção", "Ação"]
        _menu = [
            [1, "Cadastros"],
            [2, "Listas"],
            [3, "Pedidos"],
            [4, "Estoque"],
            [0, "Sair"]]

        print(tabulate(_menu, _headers, tablefmt="psql"))

    def _sub_menu_1(self):
        self._main_header("Cadastros")

        _headers = ["Opção", "Ação"]
        _menu = [
            [1, "Cliente"],
            [2, "Contato do cliente"],
            [3, "Editora"],
            [4, "Livro"],
            [5, "Pedido"],
            [6, "Local de Estoque"],
            [7, "Tabela de preços"],
            [9, "Usuário do sistema"],
            [0, "Voltar ao menu anterior"],
        ]
        print(tabulate(_menu, _headers, tablefmt="psql"))

    def _answer_sub_menu_1(self):
        while True:
            cls()

            self._sub_menu_1()
            _answer_sub_menu = self._collect_answer()

            match _answer_sub_menu:
                case 1:
                    cls()
                    customer = register_customer.RegisterCustomer(self._user)
                    if customer.register():
                        cls()
                        input("Contato cadastrado com sucesso!")
                    else:
                        cls()
                        input("Erro ao cadastrar contato")
                    cls()
                case 2:
                    cls()
                    contact = register_customer.RegisterCustomerContact(self._user)
                    if contact.register():
                        cls()
                        input("Contato cadastrado com sucesso!")
                    else:
                        cls()
                        input("Erro ao cadastrar contato.")
                    cls()
                case 3:
                    cls()
                    publisher = register_publisher.RegisterPublisher(self._user)
                    if publisher.register():
                        cls()
                        input("Editora cadastrada com sucesso!")
                    else:
                        cls()
                        input("Erro ao cadastrar editora.")
                    cls()
                case 4:
                    cls()
                    book = register_book.RegisterBook(self._user)
                    if book.register():
                        cls()
                        input("Livro cadastrado com sucesso!")
                    else:
                        cls()
                        input("Erro ao cadastrar livro.")
                    cls()
                case 5:
                    register_order.RegisterOrder(self._user)
                case 6:
                    cls()
                    local = register_local.RegisterLocal(self._user)
                    if local.register():
                        cls()
                        input("Local cadastrado com sucesso!")
                    else:
                        cls()
                        input("Erro ao cadastrar local!")
                    cls()
                case 7:
                    register_price_list.RegisterPriceList(self._user)
                case 9:
                    cls()
                    user = register_user.RegisterUser(self._user)
                    if user.register():
                        cls()
                        input("Usuário cadastrado com sucesso!")
                    else:
                        cls()
                        input("Erro ao cadastrar usuário.")
                    cls()
                case 0:
                    break
                case _:
                    input("Valor inválido, insira uma opção da lista")

    def _sub_menu_2(self):
        self._main_header("Listas")

        _headers = ["Opção", "Ação"]
        _menu = [
            [1, "Listar todos os clientes"],
            [2, "Pesquisa detalhada cliente"],
            [3, "Listar todos os livros"],
            [4, "Pesquisa detalhada livro"],
            [5, "Listar locais de estoque"],
            [0, "Voltar ao menu anterior"],
        ]
        print(tabulate(_menu, _headers, tablefmt="psql"))

    def _answer_sub_menu_2(self):
        while True:
            self._sub_menu_2()

            _answer = self._collect_answer()

            match _answer:
                case 1:
                    cls()
                    print("Lista de todos os clientes:\n\n")
                    _customer = list_customers.ListCustomer(self._user)
                    _info = _customer.list_customers()
                    print(tabulate(_info[0], headers=_info[1]))
                    input("\n\nAperte ENTER para voltar.")
                case 2:
                    ...
                case 3:
                    cls()
                    print("Lista de todos os livros:\n\n")
                    _books = list_books.ListBooks(self._user)
                    _info = _books.list_books()
                    print(tabulate(_info[0], headers=_info[1]))
                    input("\n\nAperte ENTER para voltar.")
                case 4:
                    ...
                case 5:
                    cls()
                    print("Lista de todos os locais de estoque:\n\n")
                    _local = list_local.ListLocals(self._user)
                    _info = _local.list_local()
                    print(tabulate(_info[0], headers=_info[1]))
                    input("\n\nAperte ENTER para voltar.")
                case 0:
                    break
                case _:
                    input("Valor inválido, insira uma opção da lista.")

    def _collect_answer(self) -> int:
        try:
            _res = input("\nEscolha uma opção:\n>>> ")
            return int(_res)

        except ValueError:
            return -1

        except KeyboardInterrupt:
            return 0

    def redirect_to_action(self):
        while True:
            cls()
            self._menu_header()
            _answer = self._collect_answer()

            match _answer:
                case 1:
                    self._answer_sub_menu_1()
                case 2:
                    self._answer_sub_menu_2()
                case 3:
                    input("Usuário escolheu 3")
                case 0:
                    cls()
                    input("Saindo do sistema...")
                    break
                case _:
                    input("Valor inválido, insira uma opção da lista")
