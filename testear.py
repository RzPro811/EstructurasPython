from src.Estructuras.Grafo import Grafo
from src.Estructuras.Vector import validarTipoObjeto


grafo = Grafo(int,str)

grafo.agregarVertice(1)
grafo.agregarVertice(2)
grafo.agregarVertice(3)

grafo.conectarVertices(0,1,"Hola")

print(grafo)