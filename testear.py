from Estructuras.Ordenador import Ordenador

orden = Ordenador()

lista = orden.generarListaNumRandom(20)

print(lista)
orden.stalinSortLista(lista)
print(lista)