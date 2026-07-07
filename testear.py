from Estructuras.Ordenador import Ordenador
from Estructuras.Lista import Lista, Vector
from matplotlib import pyplot as plt, animation
from random import randint
import numpy as np

orden = Ordenador()
lista:Vector = orden.generarVectorNumRandom(40)

print(lista)
orden.quickSort(lista)
print(lista)
