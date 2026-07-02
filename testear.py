from src.Estructuras.Algebra import VectorAlgebraico, MatrizAlgebraica
from src.Estructuras.Grafo import Grafo


grafo = Grafo(int, str)

grafo.agregarVertice(1)
grafo.agregarVertice(2)
grafo.conectarVertices(1,2,"camino")
grafo.agregarVertice(3)
grafo.conectarVertices(2,3)

grafo.visualizar()