from Estructuras.Ordenador import Ordenador
from Estructuras.Lista import Lista, Vector
from random import randint


orden = Ordenador()

lista1 = orden.generarListaNumeros("-20")
lista2 = orden.generarListaNumRandom(20)
vector1 = orden.generarVectorNumeros(20)
vector2 = orden.generarVectorNumRandom(20)

print(lista1)
print(lista2)
print(vector1)
print(vector2)