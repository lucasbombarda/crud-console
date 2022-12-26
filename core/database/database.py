import sqlite3
from utils.constants import DATABASE_NAME
from datetime import datetime
from utils.now import date_now
import base64 as en

class Database():
    def __init__(self) -> None:
        self._initialize_database()

    def _connect(self) -> None:
        try:
            self._conn = sqlite3.connect(f"{DATABASE_NAME}")
            self.cursor = self._conn.cursor()
        except Exception as e:
            print("Falha ao conectar no banco de dados: ", e)

    def _disconnect(self) -> None:
        try:
            self.cursor.close()
            self._conn.close()
        except Exception as e:
            print("Falha ao desconectar no banco de dados: ", e)

    def _initialize_database(self):
        self._connect()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS customer( customer_id INTEGER PRIMARY KEY AUTOINCREMENT, active INTEGER NOT NULL DEFAULT 1, name VARCHAR NOT NULL, email VARCHAR NOT NULL, registration_id VARCHAR NOT NULL UNIQUE, date_last_buy DATETIME DEFAULT NULL, update_date DATETIME NOT NULL, registration_date DATETIME NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS customer_address ( address_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL, address_type VARCHAR NOT NULL, street_name VARCHAR NOT NULL, number INTEGER NOT NULL, city VARCHAR NOT NULL, state VARCHAR(2) NOT NULL, street_id VARCHAR NOT NULL, reference VARCHAR, registration_date DATETIME NOT NULL, update_date DATETIME NOT NULL, FOREIGN KEY(customer_id) REFERENCES customer(customer_id) )")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS customer_contact ( contact_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL, contact_type VARCHAR NOT NULL, ddd INTEGER NOT NULL, tel_number INTEGER NOT NULL, registration_date DATETIME NOT NULL, update_date DATETIME NOT NULL, active INTEGER NOT NULL DEFAULT 1, FOREIGN KEY(customer_id) REFERENCES customer(customer_id) )")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS book ( book_id INTEGER PRIMARY KEY AUTOINCREMENT, active INTEGER NOT NULL DEFAULT 1, title VARCHAR, author VARCHAR, buy INTEGER NOT NULL DEFAULT 1, sell INTEGER NOT NULL DEFAULT 1, registration_date DATETIME NOT NULL, update_date DATETIME NOT NULL, publisher_id INTEGER NOT NULL, FOREIGN KEY(publisher_id) REFERENCES publisher(publisher_id) )")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS publisher ( publisher_id INTEGER PRIMARY KEY AUTOINCREMENT, active INTEGER NOT NULL DEFAULT 1, name VARCHAR NOT NULL, registration_date DATETIME NOT NULL, update_date DATETIME NOT NULL )")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sell_order ( sell_id INTEGER PRIMARY KEY AUTOINCREMENT, total FLOAT NOT NULL, situation VARCHAR NOT NULL, registration_date DATETIME NOT NULL, customer_id INTEGER NOT NULL, user_id INTEGER NOT NULL, price_list_id INTEGER NOT NULL, FOREIGN KEY(customer_id) REFERENCES customer(customer_id), FOREIGN KEY(user_id) REFERENCES user(user_id), FOREIGN KEY(price_list_id) REFERENCES price_list(price_list_id) )")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS user ( user_id INTEGER PRIMARY KEY AUTOINCREMENT, active INTEGER NOT NULL DEFAULT 1, login VARCHAR NOT NULL UNIQUE, password VARCHAR NOT NULL, name VARCHAR NOT NULL, email VARCHAR NOT NULL, registration_id VARCHAR NOT NULL, registration_date DATETIME NOT NULL, update_date DATETIME NOT NULL )")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS price_list ( price_list_id INTEGER PRIMARY KEY AUTOINCREMENT, active INTEGER NOT NULL DEFAULT 1, name VARCHAR NOT NULL, registration_date DATETIME NOT NULL, update_date DATETIME NOT NULL )")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS stock ( stock_id INTEGER PRIMARY KEY AUTOINCREMENT, quantity FLOAT NOT NULL DEFAULT 0, quantity_pend FLOAT NOT NULL DEFAULT 0, book_id INTEGER NOT NULL, local_id INTEGER NOT NULL, FOREIGN KEY(book_id) REFERENCES book(book_id), FOREIGN KEY(local_id) REFERENCES local(local_id) )")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS local ( local_id INTEGER PRIMARY KEY AUTOINCREMENT, description VARCHAR NOT NULL, active INTEGER NOT NULL DEFAULT 1 )")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS order_items ( order_item_id INTEGER PRIMARY KEY AUTOINCREMENT, book_id INTEGER NOT NULL, sell_id INTEGER NOT NULL, seq INTEGER NOT NULL, quantity FLOAT NOT NULL, discount FLOAT DEFAULT 0, price_un FLOAT NOT NULL, additional_value FLOAT DEFAULT 0, final_price_un FLOAT, final_price_item FLOAT, FOREIGN KEY(book_id) references book(book_id), FOREIGN KEY(sell_id) REFERENCES sell_order(sell_id) )")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS price ( price_id INTEGER PRIMARY KEY AUTOINCREMENT, price FLOAT NOT NULL, price_list_id INTEGER NOT NULL, book_id INTEGER NOT NULL, FOREIGN KEY(price_list_id) REFERENCES price_list(price_list_id), FOREIGN KEY(book_id) REFERENCES book(book_id) )")
        self._conn.commit()

        if not self.cursor.execute("SELECT * FROM user WHERE user_id = 1").fetchall():
            self.cursor.execute(f"INSERT INTO user (login, password, name, email, registration_id, registration_date, update_date) VALUES ('admin','R1FZREdRSlZIQVpUSU5SWUdRMkRHUlE9','Administrator','@','0','{datetime.now()}','{datetime.now()}')")
            self._conn.commit()
        
        self._disconnect()

    def _encode_password(self, password) -> str:
        _en_pwd = bytes(password, "utf-8")
        _en_pwd = en.a85encode(_en_pwd)
        _en_pwd = en.b16encode(_en_pwd)
        _en_pwd = en.b32encode(_en_pwd)
        _en_pwd = en.b64encode(_en_pwd)
        _en_pwd = _en_pwd.decode('utf-8')
        return _en_pwd

    def validate_login(self, login:str="", password:str="") -> str:
        self._connect()
        if not login.isalnum() or not password.isalnum():
            return ""

        _en_pwd = self._encode_password(password)

        __name = self.cursor.execute(f"SELECT login FROM user WHERE login = '{login}' AND password = '{_en_pwd}' AND active = '1'").fetchone()
        if __name:
            return str(__name[0])
        
        self._disconnect()

        return ""

    def insert_into_user(self, user_info) -> bool:
        try:
            self._connect()

            _active = user_info["active"]
            _login = user_info["login"]
            _password = self._encode_password(user_info["password"])
            _name = user_info["name"]
            _email = user_info["email"]
            _reg_id = user_info["registration_id"]
            _now = date_now()

            self.cursor.execute(f"INSERT INTO user (active, login, password, name, email, registration_id, registration_date, update_date) VALUES ('{_active}', '{_login}', '{_password}', '{_name}', '{_email}', '{_reg_id}', '{_now}', '{_now}')")
            self._conn.commit()

            self._disconnect()
            return True

        except Exception:
            self._disconnect()
            return False

    def insert_into_customer(self, customer_info:dict, address_info:dict, contact_info:dict) -> bool:
        try:
            self._connect()
            _now = date_now()
            _active = customer_info["active"]
            _name = customer_info["name"].upper()
            _email = customer_info["email"].lower()
            _reg_id = customer_info["registration_id"]
            self.cursor.execute(f"INSERT INTO customer (active, name, email, registration_id, registration_date, update_date) VALUES ('{_active}', '{_name}', '{_email}', '{_reg_id}', '{_now}', '{_now}')")
            self._conn.commit()

            _customer_id = self.cursor.execute(f"SELECT customer_id FROM customer WHERE name = '{_name}' AND email = '{_email}' AND registration_id = {_reg_id}").fetchone()
            _customer_id = _customer_id[0]

            _street_name = address_info["street_name"].upper()
            _number = address_info["number"]
            _city = address_info["city"].upper()
            _state = address_info["state"].upper()
            _street_id = address_info["street_id"]
            _reference = address_info["reference"].upper()
            
            self.cursor.execute(f"INSERT INTO customer_address (customer_id, address_type, street_name, number, city, state, street_id, reference, registration_date, update_date) VALUES ('{_customer_id}', 'CO', '{_street_name}', '{_number}', '{_city}', '{_state}', '{_street_id}', '{_reference}', '{_now}', '{_now}')")
            self.cursor.execute(f"INSERT INTO customer_address (customer_id, address_type, street_name, number, city, state, street_id, reference, registration_date, update_date) VALUES ('{_customer_id}', 'EN', '{_street_name}', '{_number}', '{_city}', '{_state}', '{_street_id}', '{_reference}', '{_now}', '{_now}')")
            self.cursor.execute(f"INSERT INTO customer_address (customer_id, address_type, street_name, number, city, state, street_id, reference, registration_date, update_date) VALUES ('{_customer_id}', 'FA', '{_street_name}', '{_number}', '{_city}', '{_state}', '{_street_id}', '{_reference}', '{_now}', '{_now}')")
            self._conn.commit()
            self._disconnect()
            
            self.insert_contact_info(_customer_id, contact_info)
            return True

        except Exception as e:
            print("ERRO", e)
            self._disconnect()
            return False

    def insert_contact_info(self, customer_id, contact_info:dict) -> bool:
        self._connect()

        _now = date_now()
        try:
            _active_number = contact_info["active_number"]
            _contact_type = contact_info["contact_type"].upper()
            _ddd = contact_info["ddd"]
            _tel_number = contact_info["tel_number"]

            self.cursor.execute(f"INSERT INTO customer_contact (customer_id, contact_type, ddd, tel_number, registration_date, update_date, active) VALUES ('{customer_id}', '{_contact_type}', '{_ddd}', '{_tel_number}', '{_now}', '{_now}', '{_active_number}')")
            self._conn.commit()
            self._disconnect()

            return True
        except Exception as e:
            input(f"ERRO! Contate o administrador - {e} ")
            self._disconnect()
            return False

    def insert_into_publisher(self, publisher_info:dict) -> bool:
        try:
            self._connect()

            _now = date_now()
            _active = publisher_info["active"]
            _name = publisher_info["name"]

            self.cursor.execute(f"INSERT INTO publisher (active, name, registration_date, update_date) VALUES ('{_active}', '{_name}', '{_now}', '{_now}')")
            self._conn.commit()
            self._disconnect()
            return True
        except Exception as e:
            input(f"ERRO - Contate o administrador! {e}")
            self._disconnect()
            return False

    def insert_into_book(self, book_info) -> bool:
        try:
            self._connect()

            _now = date_now()
            _active = book_info["active"]
            _title = book_info["title"]
            _author = book_info["author"]
            _buy = book_info["buy"]
            _sell = book_info["sell"]
            _publisher_id = book_info["publisher_id"]

            self.cursor.execute(f"INSERT INTO book (active, title, author, buy, sell, registration_date, update_date, publisher_id) VALUES ('{_active}', '{_title}', '{_author}', '{_buy}', '{_sell}', '{_now}', '{_now}', '{_publisher_id}')")
            self._conn.commit()
            self._disconnect()
            return True
        except Exception as e:
            input(f"ERRO - Contate o administrador - {e}")
            self._disconnect()
            return False

    def verify_customer_exists_by_id(self, customer_id) -> bool:
        self._connect()
        
        if self.cursor.execute(f"SELECT customer_id FROM customer WHERE customer_id = '{customer_id}'").fetchone():
            self._disconnect()
            return True

        self._disconnect()
        return False

    def verify_publisher_exists_by_id(self, publisher_id) -> bool:
        self._connect()
        
        if self.cursor.execute(f"SELECT publisher_id FROM publisher WHERE publisher_id = '{publisher_id}'").fetchone():
            self._disconnect()
            return True

        self._disconnect()
        return False

    def _customer_info(self, customer_id) -> list:
        self._connect()

        _info = self.cursor.execute(f"SELECT customer_id, name, registration_id FROM customer WHERE customer_id = '{customer_id}'").fetchone()

        self._disconnect()

        return _info

    def _publisher_info(self, publisher_id) -> list:

        self._connect()

        _info = self.cursor.execute(f"SELECT publisher_id, name FROM publisher WHERE publisher_id = '{publisher_id}'").fetchone()

        self._disconnect()

        return _info

    def get_customer_info(self) -> list:
        self._connect()
        _query = f"""SELECT customer_id AS 'CÓDIGO',
                active AS 'ATIVO',
                name AS 'NOME',
                email AS 'E-MAIL',
                Registration_id AS 'CPF',
                date_last_buy AS 'DATA ÚLT. COMPRA',
                registration_date AS 'DATA CADASTRADO',
                update_date AS 'DATA ÚLT. ALTERAÇÃO'
            FROM customer
        """
        _res = self.cursor.execute(_query).fetchall()
        _cols = [col[0] for col in self.cursor.description]
        self._disconnect()
        return _res, _cols

    def get_books_info(self) -> list:
        self._connect()
        _query = """SELECT b.active AS 'ATIVO',
            b.book_id AS 'CÓD. LIVRO',
            b.title AS 'TÍTULO',
            b.author AS 'AUTOR',
            p.publisher_id AS 'CÓD. EDITORA',
            p.name AS 'EDITORA',
            b.buy AS 'COMPRA',
            b.sell AS 'VENDA',
            b.registration_date AS 'DATA CADASTRO'
        FROM book b LEFT JOIN publisher p ON p.publisher_id = b.publisher_id
        """

        _res = self.cursor.execute(_query).fetchall()
        _cols = [col[0] for col in self.cursor.description]
        self._disconnect()
        return _res, _cols
