from src.Estructuras.Grafo import Grafo
from src.Estructuras.Vector import Vector

grafo:Grafo[int] = Grafo(int)

grafo.agregarVertice(1)
grafo.agregarVertice(2)
grafo.agregarVertice(3)
grafo.agregarVertice(4)
grafo.agregarVertice(5)

grafo.conectarVertices(1,2)
grafo.conectarVertices(1,3)
grafo.conectarVertices(1,4)
grafo.conectarVertices(2,3)
grafo.conectarVertices(2,4)
grafo.conectarVertices(3,4)

print(grafo.esEuleriano(), grafo.esSemiEuleriano())