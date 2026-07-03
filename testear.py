from Estructuras.Lista import Nodo, Lista
from random import randint

lista = Lista(int)

for i in range(50):
    lista.agregarFinal(i)

print(lista)