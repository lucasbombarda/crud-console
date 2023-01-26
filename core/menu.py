from art import tprint
from tabulate import tabulate
from core.utils.constants import LIBRARY_NAME
from core.registration import register_user, register_book, register_customer, register_local, register_order, register_price_list, register_publisher
from core.lists import list_local, list_book, list_customer, list_price_list
from core.utils.cls import cls
from core.search import search_customer

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

    def _customer_filter_menu(self):
        self._main_header("Filtros")
        _headers = ["Opção", "Filtro"]
        _menu = {
            1: ["Código Cliente", "customer_id"],
            2: ["Situação", "active"],
            3: ["Nome", "name"],
            4: ["E-mail", "email"],
            5: ["CPF", "registration_id"],
            6: ["Nome da rua", "street_name"],
            7: ["Número da casa","number"],
            8: ["Cidade", "city"],
            9: ["Estado", "state"],
            10: ["CEP", "street_id"],
            11: ["Complemento", "reference"],
            12: ["Tipo de contato", "contact_type"],
            13: ["DDD", "ddd"],
            14: ["Número do contato", "tel_number"],
            15: ["Situação número", "active_number"]
        }

        _menu_user = []
        self._menu_db = []

        for _item in _menu.items():
            _menu_user.append([_item[0], _item[1][0]])
            self._menu_db.append([_item[0], _item[1][1]])

        _menu_user.append([0, "FINALIZAR"])

        print(tabulate(_menu_user, _headers, tablefmt="psql"))

    def _mount_customer_filter(self):
        _collected_answers = []
        while True:
            cls()

            self._customer_filter_menu()

            if _collected_answers:
                print("\nFiltros escolhidos:", _collected_answers)

            _answer = self._collect_answer()
            if _answer in range(1, len(self._menu_db)+1) and _answer not in _collected_answers:
                _collected_answers.append(_answer)
            elif _answer in _collected_answers:
                input("Valor já está inserido, escolha outro filtro ou finalize.")
            elif _answer == 0:
                break
            else:
                input("Valor inválido, insira uma opção da lista")

        return _collected_answers

    def _apply_customer_filters(self) -> list:
        _filters = self._mount_customer_filter()
        _column_names = []
        for _filter in _filters:
            _column_names.append(self._menu_db[_filter-1])

        _search = search_customer.SearchCustomer(self._user)
        _info = _search.search(_column_names)
        
        return _info

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
                    cls()
                    _price_list = register_price_list.RegisterPriceList(self._user)
                    if _price_list.register():
                        cls()
                        input("Tabela de preços cadastrada com sucesso!")
                    else:
                        cls()
                        input("Erro ao cadastrar tabela de preços!")
                    cls()
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
            [6, "Listar todas as tabelas de preços"],
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
                    _customer = list_customer.ListCustomer(self._user)
                    _info = _customer.list_customers()
                    print(tabulate(_info[0], headers=_info[1]))
                    input("\n\nAperte ENTER para voltar.")
                case 2:
                    cls()
                    _info = self._apply_customer_filters()
                    print(tabulate(_info[0], headers=_info[1]))
                    input("\n\nAperte ENTER para voltar.")
                case 3:
                    cls()
                    print("Lista de todos os livros:\n\n")
                    _books = list_book.ListBooks(self._user)
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
                case 6:
                    cls()
                    print("Lista com todas as tabelas de preços:\n\n")
                    _price_list = list_price_list.ListPriceList(self._user)
                    _info = _price_list.list_price_list()
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
