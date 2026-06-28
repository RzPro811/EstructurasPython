from src.Estructuras.Grafo import Grafo


grafo1 = Grafo(int)
grafo2 = Grafo(int)

for i in range(10):
    if i < 5:
        grafo1.agregarVertice(i)
    else:
        grafo2.agregarVertice(i)

grafo1.conectarVertices(0,1)
grafo1.conectarVertices(0,2)
grafo1.conectarVertices(1,2)
grafo1.conectarVertices(1,3)
grafo1.conectarVertices(1,4)
grafo1.conectarVertices(2,3)
grafo1.conectarVertices(2,4)
grafo1.conectarVertices(4,3)

grafo2.conectarVertices(5,7)
grafo2.conectarVertices(9,7)
grafo2.conectarVertices(9,6)
grafo2.conectarVertices(8,6)
grafo2.conectarVertices(8,5)

grafo3 = Grafo.union(grafo1,grafo2)

grafo3.visualizar()