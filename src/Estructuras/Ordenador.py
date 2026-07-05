from .Lista import Vector, Lista, T
from .NoLineales import Heap, Cola, PRIMERA_POSCICION
from .Validaciones import validarTipoObjeto



DIGITOS = 10

class Incomparable(RuntimeError):
    def __init__(self, *args):
        """Usar si el objeto en una lista o vector, el tipo de objeto es incomparable"""
        super().__init__(*args)

class Ordenador:
    __metodo:function

    #CONSTRUCTOR
    def __init__(self, metodoOrdenamiento:function = None):
        if not callable(metodoOrdenamiento) and (metodoOrdenamiento is not None):
            raise TypeError("Ingrese una funcion que retorne algo comparable")
        self.__metodo = metodoOrdenamiento

    #METODOS INTERNOS
    def __funcion(self, item:T):
        return self.__metodo(item)

    def __hayMetodo(self) -> bool:
        return self.__metodo is not None

    def __esMayor(self, item:T, jtem:T) -> bool:
        if item is None:
            return True
        if jtem is None:
            return False
        if self.__hayMetodo():
            return self.__funcion(item) > self.__funcion(jtem)
        return item > jtem

    def __esMenor(self, item:T, jtem:T) -> bool:
        if jtem is None:
            return True
        if item is None:
            return False
        if self.__hayMetodo():
            return self.__funcion(item) < self.__funcion(jtem)
        return item < jtem
    
    def maxVector(self, vector:Vector[T]) -> T:
        maximo = vector[PRIMERA_POSCICION]

        for i in range(PRIMERA_POSCICION+1, vector.getLongitud()):
            if self.__esMayor(vector[i],maximo) and (vector[i] is not None):
                maximo = vector[i]

        return maximo


    #VALIDACIONES
    def __validarVector(self, vector:Vector[T]):
        validarTipoObjeto(Vector, vector, "Este ordenamiento necesita un vector")
    
    def __validarLista(self, lista:Lista[T]):
        validarTipoObjeto(Lista, lista, "Este ordenamiento necesita una lista")
        lista.apagarTodosLosCursores()

    def __validarVectorYContenido(self, tipo:type, vector:Vector[T]):
        self.__validarVector(vector)
        if self.__hayMetodo():
            validarTipoObjeto(tipo, self.__funcion(vector[0]), 
                              """El metodo ingresado por parametro no sirve para este tipo de ordenamiento, ya que no retorna """+tipo.__name__)
        else:   
            validarTipoObjeto(tipo, vector[0], 
                          "Este tipo de ordenamiento no es compatible con datos "+vector.getTypeName())
    
    def __validarListaYContenido(self, tipo:type, lista:Lista[T]):
        self.__validarLista(lista)
        lista.iniciarCursorInicio()

        if self.__hayMetodo():
            validarTipoObjeto(tipo, self.__funcion(lista.getDatoCursor()), 
                              """El metodo ingresado por parametro no sirve para este tipo de ordenamiento, ya que no retorna """+tipo.__name__)
        else:   
            validarTipoObjeto(tipo, lista.getDatoCursor(), 
                          "Este tipo de ordenamiento no es compatible con datos "+lista.getTypeName())
        
        lista.desactivarCursor()

    #MISCELANEOS
    def vectorOrdenado(self, vector:Vector[T]) -> bool:
        ordenado = True
        i = 0

        while ordenado and (i < vector.getLongitud()-1):
            ordenado = self.__esMenor(vector[i], vector[i+1])
            i+=1

        return ordenado
    
    def listaOrdenada(self, lista:Lista[T]) -> bool:
        self.__validarLista(lista)
        ordenado = True

        lista.activarCursorInicio()
        while not lista.llegoAlFin() and ordenado:
            ordenado = self.__esMenor(lista.getDatoCursor(), lista.getSiguienteCursor())
            lista.avanzarCursor()

        lista.desactivarCursor()
        return ordenado

    #BUBBLE SORT
    def bubbleSortVector(self, vector:Vector[T]):
        self.__validarVector(vector)

        i = 0
        terminado = False

        while not terminado and (i < vector.getLongitud() - 1):
            terminado = True
            for j in range(vector.getLongitud() - 1 - i):
                if self.__esMayor(vector[j], vector[j+1]):
                    terminado = False
                    vector.intercambiar(j, j+1)

            i+=1
    
    def bubbleSortLista(self, lista:Lista[T]):
        self.__validarLista(lista)

        i = 0
        terminado = False

        while not terminado and (i < lista.getLongitud() - 1):
            lista.iniciarCursorInicio()
            terminado = True
            for j in range(lista.getLongitud() -1 - i):
                if self.__esMayor(lista.getDatoCursor(),lista.getSiguienteCursor()):
                    terminado = False
                    lista.intercambiarCursorSiguiente()
                
                lista.avanzarCursor()

            i+=1
            lista.desactivarCursor()

    #SELECTION SORT
    def selectionSortVector(self, vector:Vector[T]):
        self.__validarVector(vector)

        for i in range(vector.getLongitud()):
            menor = i
            for j in range(i, vector.getLongitud()):
                if self.__esMenor(vector[j], vector[menor]):
                    menor = j

            vector.intercambiar(i, menor)

    #INSERTION SORT
    def insertionSortVector(self, vector:Vector[T]):
        self.__validarVector(vector)

        for i in range(1,vector.getLongitud()):
            j = i - 1
            aux = vector[i]

            while (j >= 0) and self.__esMayor(vector[j], aux): 
                vector[j+1] = vector[j]
                j-=1

            vector[j+1] = aux
            

    #COCKTAIL SHAKER SORT
    def __repasoDelantero(self, lista:Lista[T], inicio:int, fin:int) -> bool:
        terminado = True

        while inicio < fin:
            if self.__esMayor(lista.getDatoCursor(),lista.getSiguienteCursor()):
                terminado = False
                lista.intercambiarCursorSiguiente()
            print(lista)
            inicio+=1
            lista.avanzarCursor()

        return terminado
    
    def __repasoTrasero(self, lista:Lista[T], inicio:int, fin:int) -> bool:
        terminado = True

        while inicio < fin:
            if self.__esMenor(lista.getDatoCursor(), lista.getAnteriorCursor()):
                terminado = False
                lista.intercambiarCursorAnterior()
            print(lista)
            fin -=1
            lista.retrocederCursor()

        return terminado

    def cocktailShakerSort(self, lista:Lista[T]):
        self.__validarLista(lista)
        terminado = False
        inicio, fin = PRIMERA_POSCICION, lista.getLongitud() -1

        lista.activarCursorInicio()
        while not terminado and (inicio < fin):
            terminado = self.__repasoDelantero(lista, inicio, fin)
            inicio +=1
            
            if not terminado:
                self.__repasoTrasero(lista, inicio, fin)
                fin-=1
        lista.desactivarCursor()




    #GNOME SORT
    #SHELL SORT
    #MERGE SORT
    #QUICK SORT
    def __elegirPivote(self, vector:Vector, inicio:int, final:int):
        i = inicio
        j = final - 1
        piv = final

        while (i <= j):
            if self.__esMenor(vector[piv], vector[j]):
                vector.intercambiar(piv, j)
                j-=1
                piv -= 1
            else:
                vector.intercambiar(i,j)
                i+=1

        return piv

    def __quick(self, vector:Vector, inicio:int, fin:int):
        if (fin - inicio > 0):
            pivote = self.__elegirPivote(vector, PRIMERA_POSCICION, vector.getLongitud() - 1)

            self.__quick(vector, inicio, pivote - 1)
            self.__quick(vector, pivote + 1, fin)

    def quickSort(self, vector:Vector[T]):
        self.__validarVector(vector)

    #HEAP SORT
    #COUNTING SORT
    #RADIX SORT
    def __armarColas(self) -> Vector[Cola[int]]:
        colas = Vector(Cola, DIGITOS)

        for i in range(DIGITOS):
            colas[i] = Cola(int)

        return colas

    def __calcularIndiceRadix(self, numero:int, diezPotencia:int):
        if self.__hayMetodo():
            return (self.__funcion(numero) // diezPotencia) %DIGITOS
        else:
            return (numero // diezPotencia) %DIGITOS

    def __colaNumeros(self,vector:Vector[int], colasDigitos:Vector[Cola[int]], diezPotencia:int):
        for numero in vector:
            colasDigitos[self.__calcularIndiceRadix(numero,diezPotencia)].agregar(numero)

    def __reorganizarVectorRadix(self, vector:Vector[int], colasDigitos:Vector[Cola[int]]):
        i = 0
        j = 0

        while i < vector.getLongitud():
            if j >= DIGITOS:
                vector[i] = None
                i+=1 
            elif colasDigitos[j].estaVacia():
                j+=1
            else:
                vector[i] = colasDigitos[j].quitar()
                i+=1

    def radixSortVector(self, vector:Vector[int]):
        self.__validarVectorYContenido(int,vector)
        colasDigitos = self.__armarColas()
        digito = 1

        while (digito < max(vector)):
            self.__colaNumeros(vector,colasDigitos,digito)
            self.__reorganizarVectorRadix(vector,colasDigitos)
            digito*=DIGITOS


    #BUCKET SORT
    #BOGO SORT
    def bogoSortVector(self, vector:Vector):
        ordenado = self.vectorOrdenado(vector)

        while not ordenado:
            vector.mezclar()
            ordenado = self.vectorOrdenado(vector)

    #MIRACLE SORT    
    def miracleSortVector(self, vector:Vector):
        ordenado = self.vectorOrdenado(vector)

        while not ordenado:
            ordenado = self.vectorOrdenado()

    #STALIN SORT
