from .Vector import Vector, T, PRIMERA_POSCICION
from .NoLineales import Heap, Cola, Pila

DIGITOS = 10

class Ordenador:
    __metodo:function

    def __init__(self, metodoOrdenamiento:function = None):
        if not callable(metodoOrdenamiento) and (metodoOrdenamiento is not None):
            raise TypeError("Ingrese una funcion que retorne algo comparable")
        self.__metodo = metodoOrdenamiento

    def __funcion(self, item:T):
        return self.__metodo(item)

    def __hayMetodo(self) -> bool:
        return self.__metodo is not None

    def __mayor(self, item:T, jtem:T) -> bool:
        if item is None:
            return True
        if jtem is None:
            return False
        if self.__hayMetodo():
            return self.__funcion(item) > self.__funcion(jtem)
        return item > jtem

    def __menor(self, item:T, jtem:T) -> bool:
        if jtem is None:
            return True
        if item is None:
            return False
        if self.__hayMetodo():
            return self.__funcion(item) < self.__funcion(jtem)
        return item < jtem

    def __comparar(self, item:T, jtem:T, ascendente:bool) -> bool:
        if ascendente:
            return self.__mayor(item,jtem)
        return self.__menor(item,jtem)
    
    def __ultimaPoscicion(self,vector:Vector[T]) -> int:
        return vector.getLongitud() -1

    #BUBBLE SORT
    def bubbleSort(self, vector:Vector[T], ascendente:bool = True):
        i = 0
        ordenado = False

        while (not ordenado and (i <= vector.getLongitud() - 1)):
            ordenado = True
            for j in range(vector.getLongitud() - 1):
                if self.__comparar(vector[j], vector[j+1],ascendente):
                    vector.intercambiar(j,j+1)
                    ordenado = False

            i+=1

    #QUICK SORT
    def __seleccionarPivote(self, vector:Vector[T], inicio:int, fin:int, ascendente:bool) -> int:
        i = inicio
        j = fin -1
        piv = fin

        while (i <= j):
            if self.__comparar(vector[j], vector[piv], ascendente):
                vector.intercambiar(piv, j)
                j-=1
                piv -=1
            else:
                vector.intercambiar(j,i)
                i+=1
    
        return piv
    
    def __quicksort(self, vector:Vector[T], inicio:int, fin:int, ascendente:bool):
        if (fin - inicio) > 0:

            pivote = self.__seleccionarPivote(vector, inicio, fin, ascendente)
            
            self.__quicksort(vector,inicio, pivote-1, ascendente)
            self.__quicksort(vector,pivote+1, fin, ascendente)
    

    def quickSort(self, vector:Vector[T], ascendente:bool = True):
        self.__quicksort(vector, PRIMERA_POSCICION, self.__ultimaPoscicion(vector),ascendente)

    #RADIX SORT
    def __generarVectorColas(self, ascendente:bool) -> Vector[Cola[int]|Pila[int]]:
        if ascendente: 
            vectorColas = Vector(Cola, DIGITOS)
            for i in range(DIGITOS):
                vectorColas[i] = Cola(int)
        else: 
            vectorColas = Vector(Pila, DIGITOS)
            for i in range(DIGITOS):
                vectorColas[i] = Pila(int)

        return vectorColas

    def __colaDeDigitos(self, vectorColas:Vector[Cola[int]|Pila[int]], numero:int, diezPotencia:int):
        vectorColas[(numero//diezPotencia)%10].agregar(numero)
        
    def __pasarNumeros(self, vector:Vector[int], vectorColas:Vector[Cola[int]],ascendente:bool):
        i = 0
            
        if ascendente:
            j = 0
        else:
            j = self.__ultimaPoscicion(vector)
        
        while (j < vector.getLongitud()):
            if vectorColas[i].estaVacia():
                i+=1
            else: 
                vector[j] = vectorColas[i].quitar()
                if ascendente: j+=1
                else: j-=1

    def radixSort(self,vector:Vector[int],ascendente:bool = True):
        vectorColas = self.__generarVectorColas(ascendente)
        diezPotencia = 1

        while diezPotencia < max(vector):
            for numero in vector:
                self.__colaDeDigitos(vectorColas, numero, diezPotencia)

            self.__pasarNumeros(vector, vectorColas, ascendente)
            
            diezPotencia*=DIGITOS

    #HEAP SORT
    def heapMinSort(self, vector:Vector[T], ascendente:bool = True):
        if ascendente:
            Heap.ordenarPorMinimo(vector,self.__metodo)
        else:
            Heap.ordenarPorMaximo(vector,self.__metodo)