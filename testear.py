from src.Estructuras.Grafo import Grafo

grafo = Grafo.generarGrafoCompleto({1,2,3,4})
grafo.agregarVertice(0)
grafo.conectarVertices(0,1)
grafo.conectarVertices(0,2)

grafo.visualizar()