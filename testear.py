from Estructuras.Ordenador import Ordenador
from Estructuras.Lista import Lista, Vector
from random import randint


orden = Ordenador()

lista2 = orden.generarListaNumRandom(20)
vector2 = orden.generarVectorNumRandom(20)

print(lista2)
print(vector2)

orden.heapSortLista(lista2)
orden.heapSortVector(vector2)

print(lista2)
print(vector2)