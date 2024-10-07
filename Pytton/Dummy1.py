lista = []
Numero = 1
UltimoNum2 = 1
lista2 = []
lista3 = []
for x in range(10):
    lista.append([[list(range(Numero,Numero + 25)) for z in range(2)]for i in range(5)])
    Numero = Numero + 25
print(lista)