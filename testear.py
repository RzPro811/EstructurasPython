from src.Estructuras.Vector import Vector
from src.Estructuras.NoLineales import Heap
from random import randint

heap  = Heap(int)

print(heap.estaVacio())

for i in range(10):
    numero = randint(0,100)
    print(numero)
    heap.agregar(numero)

vector = Vector(int,10)

while not heap.estaVacio():
    print(vector)
    vector.agregar(heap.quitar())

print(vector)