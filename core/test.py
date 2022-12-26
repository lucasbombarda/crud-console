from utils.validations import Validations

val = Validations()
teste = val.inputStr("TESTE", "TESTE", blank=True)
print(teste)