from core.login import Login
import os

if __name__ == "__main__":
    os.system('mode con: cols=250 lines=55')
    Login().user_login()