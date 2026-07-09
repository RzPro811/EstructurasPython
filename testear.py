from Estructuras.Vector import Vector, Matriz
from Estructuras.Lista import Lista
from Estructuras.NoLineales import Cola, Pila, Heap
from Estructuras.Grafo import Grafo, Digrafo
from Estructuras.Algebra import VectorAlgebraico, MatrizAlgebraica
from Estructuras.Ordenador import Ordenador
from random import randint

orden = Ordenador()

palabras = "crow reptile hyena panther parrot frog otter ferret marmoset mink monkey badger horse lizard canary aardvark hamster wildcat weasel cheetah".split(" ")
vector = Vector(float, len(palabras))
for i in range(len(palabras)):
    num = randint(0,100)
    den = randint(num, 100)
    
    vector[i] = num/den



print(vector)
orden.bucketSortVector(vector)
print(vector)

