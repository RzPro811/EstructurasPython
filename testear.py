from Estructuras.Ordenador import Ordenador
from Estructuras.Lista import Lista, Vector
from matplotlib import pyplot as plt, animation
from random import randint
import numpy as np

orden = Ordenador()
lista:Lista = orden.generarListaNumRandom(15)

print(lista)
orden.stalinSortLista(lista)
print(lista)
