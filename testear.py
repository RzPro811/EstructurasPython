from src.Estructuras.Vector import Vector
from src.Estructuras.NoLineales import Heap
from random import randint

vector = Vector(int, 10)


for i in range(10):
    numero = randint(0,100)
    print(numero)
    vector.agregar(numero)

print(vector)

Heap.ordenarPorMaximo(vector)

print(vector)