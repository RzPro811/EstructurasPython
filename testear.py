from src.Estructuras.Vector import Heap, Vector
from random import randint

heap  = Heap(int)

for i in range(10):
    numero = randint(0,100)
    print(numero)
    heap.agregar(numero)

vector = Vector(int, heap.getCantidadElementos())

while not heap.estaVacio():
    vector.agregar(heap.quitar())

print(vector)