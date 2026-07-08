from Estructuras.Grafo import Grafo

grafo1 = Grafo.generarGrafoCircuito({1,2,3})
grafo2 = Grafo.generarGrafoPath({7,8,9})

gr = Grafo.union(grafo1,grafo2)

print(gr.esConexo())

gr.visualizar()