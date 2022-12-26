import re
from validate_email import validate_email

class Validations:
    def inputStr(self, question, error_msg, allowRegex=None, blank=False) -> str:
        while True:

            print(question, end="")
            _answer = input()

            if blank and not _answer:
                return ""
            
            elif not blank and not _answer:
                print(error_msg)

            else:
                try:
                    if allowRegex:
                        if re.match(allowRegex, _answer):
                            return _answer
                        else:
                            print(error_msg)
                    else:
                        return str(_answer)
                        
                except ValueError:
                    print(error_msg)

    def inputInt(self, question, error_msg, allowRegex=None, blank=False) -> int:
        while True:
            print(question, end="")
            _answer = input()

            if blank and not _answer:
                return

            elif not blank and not _answer:
                print(error_msg)

            else:
                try:
                    _answer = int(_answer)

                    if allowRegex:
                        if re.match(allowRegex, str(_answer)):
                            return _answer
                        else:
                            print(error_msg)
                    else:
                        return _answer
                        
                except ValueError:
                    print(error_msg)

    def inputEmail(self, question, error_msg, blank=False) -> str:
        while True:
            print(question, end="")
            _answer = input()

            if blank and not _answer:
                return

            elif not blank and not _answer:
                print(error_msg)

            else:
                if validate_email(_answer):
                    return _answer
                print(error_msg)
                    