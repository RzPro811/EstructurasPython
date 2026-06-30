from src.Estructuras.Ordenador import Ordenador
from src.Estructuras.Vector import Vector
from random import randint

LONGITUD = 50
vector = Vector(int, LONGITUD)
for i in range(LONGITUD):
    vector[i] = randint(1,1000)


orden = Ordenador()

print(vector)
orden.heapMinSort(vector)
print(vector)