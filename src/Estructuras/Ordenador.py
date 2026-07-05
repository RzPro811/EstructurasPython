from .Lista import Vector, Lista, T
from .NoLineales import Heap, Cola, PRIMERA_POSCICION
from .Validaciones import validarTipoObjeto, validarMayorQue, validarOrden
from .Excepciones.Ordenador import*
from random import randint

DIGITOS = 10
MINIMO_RANDOM = 1
MAXIMO_RANDOM = 1000


class Ordenador:
    """Ya que he creado un TDA Vector y un TDA lista, he decidido crear esta herramienta cuando haya necesidad de ordenar
    los elementos en ambas estructuras, con el fin de que no tengas que programar vos mismo los ordenamientos necesarios

    Solo crea un Ordenador, si quiere introduzca una función para ordenar segun el resultado y listo, 
    tendrá su ordenador de Vectores y Listas enlazadas.

    ### ALGORITMOS INCLUIDOS:
        -   **BubbleSort** (Vector/Lista)
        -   **SelectionSort** (Vector)
        -   **InsertionSort** (Vector)
        -   **CocktailShakerSort** (Lista)
        -   **GnomeSort** (Lista)
        -   **ShellSort** (Lista)
        -   **MergeSort** (Vector)
        -   **QuickSort** (Vector)
        -   **HeapSort** (Vector/Lista)
        -   **CountingSort** (Vector/Lista)
        -   **RadixSort** (Vector/Lista)
        -   **BucketSort** (Vector/Lista)
        -   **BogoSort** (Vector/Lista)
        -   **StalinSort** (Vector/Lista)
        -   **MiracleSort** (Vector/Lista)
    
    """
    __metodo:function

    #CONSTRUCTOR
    def __init__(self, metodoOrdenamiento:function = None):
        """Crea un ordenador
        
        **parameters**
            -   metodoOrdenamiento (function): por defecto None. Si se introduce una funcion, 
            se ordenarán los datos de un vector o lista en base a lo que retorne el metodo

        **excepciones**
            -   **TypeError**: Si no se ingresa una funcion por parametro
        """
        if not callable(metodoOrdenamiento) and (metodoOrdenamiento is not None):
            raise TypeError("Ingrese una funcion que retorne algo comparable")
        self.__metodo = metodoOrdenamiento

    #METODOS DE CLASE
    def vectorOrdenado(self, vector:Vector[T]) -> bool:
        """Dado un vector, verifica que esté ordenado
        
        **parameters**
            -   vector (Vector[T])

        **return**
            -   (bool) Verdadero si el vector está ordenado, falso si no

        **excepciones**
            -   **TypeError** si lo ingresado no fue un Vector
        """
        self.__validarVector(vector)
        ordenado = True
        i = 0

        while ordenado and (i < vector.getLongitud()-1):
            ordenado = self.__esMenor(vector[i], vector[i+1])
            i+=1

        return ordenado
    
    def listaOrdenada(self, lista:Lista[T]) -> bool:
        """Dado una lista, verifica que esté ordenado
        
        **parameters**
            -   lista (Lista[T])

        **return**
            -   (bool) Verdadero si la lista está ordenada, falso si no

        **excepciones**
            -   **TypeError** si lo ingresado no fue una Lista
        """
        self.__validarLista(lista)
        ordenado = True

        lista.activarCursorInicio()
        while not lista.llegoAlFin() and ordenado:
            ordenado = self.__esMenor(lista.getDatoCursor(), lista.getSiguienteCursor())
            lista.avanzarCursor()

        lista.desactivarCursor()
        return ordenado
    
    def convertirAVector(self, lista:Lista[T]) -> Vector[T]:
        self.__validarLista(lista)

        vector = Vector(lista.getType(), lista.getLongitud())
        
        i = 0
        for elemento in lista:
            vector[i] = elemento
            i+=1

        return vector
        
    def convertirALista(self, vector:Vector) -> Lista[T]:
        self.__validarVector(vector)

        lista = Lista(vector.getType())

        for elemento in vector:
            lista.agregarFinal(elemento)

        return lista

    def generarVectorNumeros(self, numeroMax:int) -> Vector[int]:
        validarMayorQue(numeroMax,MINIMO_RANDOM,
                        mensaje= "Ingresa un numero mayor o igual que 1", error = GeneracionNegativaError)
        vector = Vector(int, numeroMax)

        for i in range(numeroMax):
            vector[i] = i+1

        return vector
    
    def generarVectorNumRandom(self, largo, minimo = MINIMO_RANDOM, maximo = MAXIMO_RANDOM) -> Vector[int]:
        validarOrden(minimo, maximo, 
                     f"El numero {maximo} es mas chico que {minimo}, debiste ingrsar {minimo} antes que {maximo}",MaximoMinimoIntercambiados)
        vector = Vector(int, largo)

        for i in range(largo):
            vector[i] = randint(minimo, maximo)

        return vector
    
    def generarListaNumeros(self, numeroMax:int) -> Lista[int]:
        validarMayorQue(numeroMax,MINIMO_RANDOM,
                        mensaje= "Ingresa un numero mayor o igual que 1", error = GeneracionNegativaError)
        lista = Lista(int)

        for i in range(numeroMax):
            lista.agregarFinal(i+1)

        return lista
    
    def generarListaNumRandom(self, largo, minimo = MINIMO_RANDOM, maximo = MAXIMO_RANDOM) -> Lista[int]:
        lista = Lista(int)

        for i in range(largo):
            lista.agregarFinal(randint(minimo, maximo))

        return lista

    #METODOS INTERNOS
    def __funcion(self, item:T):
        """Ejecuta la funcion
        
        **parameters**
            -   item (T)

        **return**
            -   (???) debe ser comparable
        
        **excepcioens**
            -   **???**: las que vengan con el metodo
        """
        return self.__metodo(item)

    def __hayMetodo(self) -> bool:
        """Verfica que haya un metodo para ordenar ingresado
        
        **return**
            -   (bool) verdadero si no se ingreso un none por metodo, falso si si
        """
        return self.__metodo is not None

    def __esMayor(self, item:T, jtem:T) -> bool:
        """Dado dos items, verifca que el primero sea mayor al segundo. 
        Si uno es none, se considerará a None como el mayor.
        Si se ingresó un metodo en el constructor, se comparara los resultados de evaluar las funciones
        con respecto de los items ingresados

        **parameters**
            -   item (T)
            -   jtem (T)
        
        **return**
            -   (bool): si el primer elemento es mayor al segundo (o lo obtenido al evaluarlos en el metodo ingresado)
        """
        if item is None:
            return True
        if jtem is None:
            return False
        if self.__hayMetodo():
            return self.__funcion(item) > self.__funcion(jtem)
        return item > jtem

    def __esMenor(self, item:T, jtem:T) -> bool:
        """Dado dos items, verifca que el primero sea menor al segundo. 
        Si uno es none, se considerará a None como el mayor.
        Si se ingresó un metodo en el constructor, se comparara los resultados de evaluar las funciones
        con respecto de los items ingresados

        **parameters**
            -   item (T)
            -   jtem (T)
        
        **return**
            -   (bool): si el primer elemento es menor al segundo (o lo obtenido al evaluarlos en el metodo ingresado)
        """
        if jtem is None:
            return True
        if item is None:
            return False
        if self.__hayMetodo():
            return self.__funcion(item) < self.__funcion(jtem)
        return item < jtem
    
    def maxVector(self, vector:Vector[T]) -> T:
        """Devuelve el maximo de un vecotr"""
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


    #BUBBLE SORT
    def bubbleSortVector(self, vector:Vector[T]):
        """BUBBLE SORT (VECTOR)
        
        Dado un vector, lo recorre tantas veces como la longitud del vector - 1.
        En cada pasa intercambia dos elementos si el primero es mas chico que el segundo

        **parameters**  
            -   vector (Vector[T])

        **excepciones**
            -   **Incomparable** si el tipo de datos del vector no es comparables
        
        **complejidad**: O(x^2)
            -   x: longitud del vecor                   
        """
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
            
            inicio+=1
            lista.avanzarCursor()

        return terminado
    
    def __repasoTrasero(self, lista:Lista[T], inicio:int, fin:int) -> bool:
        terminado = True

        while inicio < fin:
            if self.__esMenor(lista.getDatoCursor(), lista.getAnteriorCursor()):
                terminado = False
                lista.intercambiarCursorAnterior()

            fin -= 1
            lista.retrocederCursor()

        return terminado

    def cocktailShakerSortLista(self, lista:Lista[T]):
        self.__validarLista(lista)
        terminado = False
        inicio, fin = PRIMERA_POSCICION, lista.getLongitud() -1

        lista.activarCursorInicio()
        while not terminado and (inicio < fin):
            terminado = self.__repasoDelantero(lista, inicio, fin)
            inicio +=1
            
            if not terminado:
                terminado = self.__repasoTrasero(lista, inicio, fin)
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
    def heapSortVector(self, vector:Vector[T]):
        self.__validarVector(vector)
        heapMin = Heap(vector.getType(),self.__metodo)

        for elemento in vector:
            heapMin.agregar(elemento)

        for i in range(vector.getLongitud()):
            vector[i] = heapMin.quitar()


    def heapSortLista(self, lista:Lista[T]):
        self.__validarLista(lista)
        heapMin = Heap(lista.getType(),self.__metodo)

        while not lista.estaVacia():
            heapMin.agregar(lista.quitarInicio())

        while not heapMin.estaVacio():
            lista.agregarFinal(heapMin.quitar())

    #COUNTING SORT
    #RADIX SORT
    def __armarColas(self) -> Vector[Cola[int]]:
        colas = Vector(Cola, DIGITOS)

        for i in range(DIGITOS):
            colas[i] = Cola(int)

        return colas

    def __calcularIndiceRadix(self, numero:int, diezPotencia:int):
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

    def bogoSortLista(self, lista:Lista):
        ordenado = self.listaOrdenada(lista)
        
        while not ordenado:
            lista.mezclar()
            ordenado = self.listaOrdenada(lista)

    #MIRACLE SORT    
    def miracleSortVector(self, vector:Vector):
        ordenado = self.vectorOrdenado(vector)

        while not ordenado:
            ordenado = self.vectorOrdenado()

    #STALIN SORT