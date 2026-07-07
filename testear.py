from src.Estructuras.Ordenador import Ordenador
from src.Estructuras.Lista import Lista, Vector
from random import randint

orden = Ordenador()
lista:Lista = orden.generarListaNumRandom(40)

print(lista)
orden.radixSortLista(lista)
print(lista)
