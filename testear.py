from Estructuras.Ordenador import Ordenador
from Estructuras.Lista import Lista, Vector
from random import randint

lista = Lista(int)
orden = Ordenador()

for i in range(10):
    lista.agregarFinal(randint(0,100))

print(lista)

orden.cocktailShakerSort(lista)

print(lista)