from src.Estructuras.Ordenador import Ordenador
from src.Estructuras.Lista import Lista, Vector
from random import randint

orden = Ordenador()
lista:Lista = orden.generarVectorNumeros(20)

print(lista)
lista.invertir()
print(lista)
