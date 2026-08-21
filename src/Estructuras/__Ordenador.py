from .__Lista import Vector, Lista, T
from .__NoLineales import Heap, Cola, PRIMERA_POSCICION
from .__Validaciones import validarTipoObjeto, validarMayorQue, validarOrden, validarNoNegativo
from .Excepciones.Ordenador import*
from random import randint

visualizacion = True

try:
    from matplotlib import pyplot as plt
    from matplotlib.container import BarContainer
    from matplotlib.patches import Rectangle
except ImportError as e:
    visualizacion = False

LARGO_VISUALIZACION = 20
DIGITOS = 10
MINIMO_RANDOM = 1
MAXIMO_RANDOM = 1000
CANTIDAD_BALDES = 5

class Ordenador:
    """ # ORDENADOR
    
    Ya que he creado un TDA Vector y un TDA lista, he decidido crear esta herramienta cuando haya necesidad de ordenar
    los elementos en ambas estructuras, con el fin de que no tengas que programar vos mismo los ordenamientos necesarios

    Solo crea un Ordenador, si quiere introduzca una función para ordenar segun el resultado y listo, 
    tendrá su ordenador de Vectores y Listas enlazadas.

    ### ALGORITMOS INCLUIDOS:
    
    #### Para estructuras casi ordenadas
        -   **BubbleSort** (Vector/Lista)
        -   **SelectionSort** (Vector)
        -   **InsertionSort** (Vector)
        -   **CocktailShakerSort** (Lista)
        -   **GnomeSort** (Lista)
        -   **ShellSort** (Lista)
    #### Divide y Venceras
        -   **MergeSort** (Vector)
        -   **QuickSort** (Vector)
        -   **HeapSort** (Vector/Lista)
    #### No Comparativos
        -   **CountingSort** (Vector/Lista)
        -   **RadixSort** (Vector/Lista)
        -   **BucketSort** (Vector/Lista)
    #### Algoritmos de broma
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
        """Dada una lista, la convierte en vector
        
        **parameters**
            -   lista (Lista[T])

        **return**
            -   (Vector[T]) Vector con los elementos de la lista

        **excepciones**
        """
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
                     f"El numero {maximo} es más chico que {minimo}, debiste ingrsar {minimo} antes que {maximo}",MaximoMinimoIntercambiados)
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

    #ALGORITMOS PARA ESTRUCTURAS CASI ORDENADAS

    #BUBBLE SORT
    def bubbleSortVector(self, vector:Vector[T]):
        """# BUBBLE SORT
        
        ## Vector
        Dado un vector, lo recorre tantas veces como la longitud del vector - 1.
        En cada pasa intercambia dos elementos si el primero es más chico que el segundo. 
        Al final de cada iteracion, el elemento más grande queda al final del vector como si de 
        una burbuja subiendo a la superficie del agua se tratase

        **parameters**  
            -   vector (Vector[T]): Tipo de datos comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es un vector
            -   **Incomparable**: si el tipo de datos del vector no es comparables
        
        **complejidad**: 
            -   O(x^2) x: longitud del vecor                   
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
        """# BUBBLE SORT
        
        ## Lista
        Dado una lista, la recorre tantas veces como la longitud de la lista - 1.
        En cada pasa intercambia dos elementos si el primero es más chico que el segundo. 
        Al final de cada iteracion, el elemento más grande queda al final de la lista como si de 
        una burbuja subiendo a la superficie del agua se tratase

        **parameters**  
            -   lista (Lista[T]): Tipo de datos comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es una lista
            -   **Incomparable**: si el tipo de datos de la lista no es comparables
        
        **complejidad**: 
            -   O(x^2) x: longitud de la lista
        """                   
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
        """# SELECTION SORT
        
        ## Vector
        Recorre el vector tantas veces como la longitud del vector -1 buscando el elemento más chico.
        Una vez seleccionado ese elemento, lo coloca en la primera poscicion del vector.

        **parameters**  
            -   vector (Vector[T]): Tipo de datos comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es un vector
            -   **Incomparable**: si el tipo de datos del vector no es comparables
        
        **complejidad**:
            -   O(x^2) x: longitud de el vector
        """
        self.__validarVector(vector)

        for i in range(vector.getLongitud()):
            menor = i
            for j in range(i, vector.getLongitud()):
                if self.__esMenor(vector[j], vector[menor]):
                    menor = j

            vector.intercambiar(i, menor)

    #INSERTION SORT
    def insertionSortVector(self, vector:Vector[T]):
        """# INSERTION SORT
        
        ## Vector
        Agarra a cada elemento del vector y lo arrastra hacia atras, 
        insertando el elemento en el lugar que le corrresponde

        **parameters**  
            -   vector (Vector[T]): Tipo de datos comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es un vector
            -   **Incomparable**: si el tipo de datos del vector no es comparables
        
        **complejidad**:
            -   O(x^2) x: longitud de el vector
        """
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
        """# COTAIL SHAKER SORT
        
        ## Lista
        Dado una lista, la recorre tantas veces como la longitud de la lista - 1.
        Es parecido al bubble sort pero va hacia adelante y hacia atras, como un bartender sacudiendo una coctelera.
        Al final de cada iteracion, siempre queda el elemento mas grande al final y el elemento más chico hacia atras 

        **parameters**  
            -   lista (Lista[T]): Tipo de datos comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es una lista
            -   **Incomparable**: si el tipo de datos de la lista no es comparables
        
        **complejidad**: 
            -   O(x^2) x: longitud de la lista
        """                   
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

    def gnomeSortLista(self, lista:Lista[T]):
        """# BUBBLE SORT
        
        ## Lista
        Dado una lista, la recorre hacia adelante comparando cada elemento con el siguiente.
        Si encuentra un elemento más pequeño que el anterior, lo arrastra al final. Como un gnomo 
        que está llevando cosas de un lugar a otro (qsy, nunca ví un gnomo trabajando).
        Es básicamente un Insertion Sort pero con pasos extra-

        **parameters**  
            -   lista (Lista[T]): Tipo de datos comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es una lista
            -   **Incomparable**: si el tipo de datos de la lista no es comparables
        
        **complejidad**: 
            -   O(x^2) x: longitud de la lista
        """                   
        self.__validarLista(lista)
        i = PRIMERA_POSCICION

        lista.iniciarCursorInicio()
        while (i < lista.getLongitud() - 1):
            if self.__esMenor(lista.getDatoCursor(), lista.getSiguienteCursor()):
                lista.avanzarCursor()
                i+=1
            else:
                lista.intercambiarCursorSiguiente()
                
                if (i > PRIMERA_POSCICION) and not self.__esMenor(lista.getAnteriorCursor(),lista.getDatoCursor()):
                    lista.retrocederCursor()
                    i-=1

        lista.desactivarCursor()

    #SHELL SORT

    #ALGORITMOS DIVIDE Y VENCERAS

    #MERGE SORT
    def __mergearAuxiliares(self, vector:Vector[T], vectorAux:Vector[T], pos1:int, pos2:int):
        vector[pos1] = vectorAux[pos2]
        return pos2+1

    def __laGranReunificacion(self, vector:Vector[T], vectorAux1:Vector[T], vectorAux2:Vector[T]):
        i = PRIMERA_POSCICION
        j = PRIMERA_POSCICION

        for k in range(vector.getLongitud()):
            if j == vectorAux2.getLongitud():
                i = self.__mergearAuxiliares(vector, vectorAux1, k, i)
            elif i == vectorAux1.getLongitud():
                j = self.__mergearAuxiliares(vector, vectorAux2, k, j)
            elif (self.__esMenor(vectorAux1[i], vectorAux2[j])):
                i = self.__mergearAuxiliares(vector, vectorAux1, k, i)
            else:
                j = self.__mergearAuxiliares(vector, vectorAux2, k, j)

    def __generarVectorAux(self, vector:Vector[T], inicio:int, fin:int):
        vectorAux = Vector(vector.getType(), fin - inicio)

        for i in range(vectorAux.getLongitud()):
            vectorAux[i] = vector[i + inicio]

        return vectorAux

    def mergeSortVector(self, vector:Vector[T]):
        """# MERGE SORT
        
        ## Vector
        Separa el contenido del vector en dos vectores auxiliares.
        Luego separa esos dos vectores auxiliares en otros dos vectores auxiliares.
        Y así recursivamente hasta que los vectores auxiliares tengan un solo elemento.
        Luego los reunifica poniendo los elementos mas pequeños primero.

        **parameters**  
            -   vector (Vector[T]): Tipo de datos comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es un vector
            -   **Incomparable**: si el tipo de datos del vector no es comparables
        
        **complejidad**:
            -   O(log2 (x)) x: longitud de el vector
        """
        if vector.getLongitud() > 1:
            vectorAux1 = self.__generarVectorAux(vector, PRIMERA_POSCICION, vector.getLongitud()//2)
            vectorAux2 = self.__generarVectorAux(vector, vectorAux1.getLongitud(),vector.getLongitud())

            self.mergeSortVector(vectorAux1)
            self.mergeSortVector(vectorAux2)

            self.__laGranReunificacion(vector, vectorAux1, vectorAux2)


    #QUICK SORT
    def __elegirPivote(self, vector:Vector, inicio:int, final:int):
        i, j, piv = inicio+1, final, inicio
        
        while (i < j):
            if vector[i] <= vector[piv]:
                i+=1
            elif vector[j] >= vector[piv]:
                j-=1
            else:
                vector.intercambiar(i,j)

        vector.intercambiar(i-1, piv)

        return i-1

    def __quick(self, vector:Vector, inicio:int, fin:int):
        if (fin - inicio > 0):
            pivote = self.__elegirPivote(vector, inicio, fin)

            self.__quick(vector, inicio, pivote - 1)
            self.__quick(vector, pivote + 1, fin)

    def quickSort(self, vector:Vector[T]):
        """# QUICK SORT
        
        ## Vector
        Agarra un elemento cualquiera llamado "pivote", en este caso el ultimo elemento, lo arrastra 
        hasta la poscicion que le corresponde, y deja todos los valores mas pequeños antes del pivote y los 
        más grandes después del pivote. Y luego se aplica Quick Sort a los elementos antes y despues del pivote
        recursivamente. Todo sin crear vectores auxiliares 
        
        **parameters**  
            -   vector (Vector[T]): Tipo de datos comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es un vector
            -   **Incomparable**: si el tipo de datos del vector no es comparables
        
        **complejidad**:
            -   O(xln2 (x)) x: longitud de el vector, Si es que el pivote acaba en el medio
            -   O(x^2) x: longitud de el vector, Si es que el pivote es el elemento mas grande o el mas chico del vector
        """
        self.__validarVector(vector)
        self.__quick(vector, PRIMERA_POSCICION, vector.getLongitud()-1)

    #HEAP SORT
    def heapSortVector(self, vector:Vector[T]):
        """# HEAP SORT
        
        ## Vector
        Mete todo el contenido del vector en un Heap.
        Luego saca cada elemento del heap desde la primera poscicion hasta la ultima
        
        **parameters**  
            -   vector (Vector[T]): Tipo de datos comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es un vector
            -   **Incomparable**: si el tipo de datos del vector no es comparables
        
        **complejidad**:
            -   O(log2 (x)) x: longitud de el vector
        """
        self.__validarVector(vector)
        heapMin = Heap(vector.getType(),self.__metodo)

        for elemento in vector:
            heapMin.agregar(elemento)

        for i in range(vector.getLongitud()):
            vector[i] = heapMin.quitar()


    def heapSortLista(self, lista:Lista[T]):
        """# HEAP SORT
        
        ## Lista
        Mete todo el contenido de la lista en un Heap.
        Luego saca cada elemento del heap desde la primera poscicion hasta la ultima
        
        **parameters**  
            -   lista (Lista[T]): Tipo de datos comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es una lista
            -   **Incomparable**: si el tipo de datos de la no es comparables
        
        **complejidad**:
            -   O(log2 (x)) x: longitud de la lista
        """
        self.__validarLista(lista)
        heapMin = Heap(lista.getType(),self.__metodo)

        while not lista.estaVacia():
            heapMin.agregar(lista.quitarInicio())

        while not heapMin.estaVacio():
            lista.agregarFinal(heapMin.quitar())

    #ALGORITMOS NO COMPARATIVOS

    #COUNTING SORT
    def __vectorConteo(self, estructura:Vector[int]|Lista[int]) -> Vector[int]:
        conteo = Vector(int, max(estructura) + 1)

        for i in range(conteo.getLongitud()):
            conteo[i] = PRIMERA_POSCICION
        return conteo

    def __verPosciciones(self, estructura:Vector[int]|Lista[int], conteo:Vector[int]):
        for numero in estructura:
            conteo[numero] +=1

    def __ajustarConteo(self, conteo:Vector[int]):
        for i in range(1, conteo.getLongitud()):
            conteo[i] += conteo[i-1]

    def __compactadorMetodosCountingSort(self, estructura:Vector[int]|Lista[int]) -> Vector[int]:
        conteo = self.__vectorConteo(estructura)
        self.__verPosciciones(estructura,conteo)
        self.__ajustarConteo(conteo)
        return conteo
        
    def __reordenamientoCountingVector(self, vector:Vector[int], conteo:Vector[int]):
        i = conteo.getLongitud() - 1 

        while conteo[PRIMERA_POSCICION] > PRIMERA_POSCICION:
            if (i > 0) and (conteo[i] == conteo[i-1]):
                i-=1
            else:
                conteo[i] -= 1
                vector[conteo[i]] = i
 
    def __reordenamientoCountingLista(self, lista:Lista[int], conteo:Vector[int]):
        i = conteo.getLongitud() - 1 

        lista.iniciarCursorFinal()
        while conteo[PRIMERA_POSCICION] > PRIMERA_POSCICION:
            if (i > 0) and (conteo[i] == conteo[i-1]):
                i-=1
            else:
                conteo[i] -= 1
                lista.setDatoCursor(i)
                lista.retrocederCursor()

    def countingSortVector(self, vector:Vector[int]):
        """# COUNTING SORT
        
        ## Vector
        Dado un vector de numeros enteros positivos (de preferencia, todos más chicos que el largo del vector)
        Cuenta cada uno de esos elementos. Una vez hecha las cuentas, calcula la posicion que le corresponde a cada
        elemento y los coloca allí

        **parameters**  
            -   vector (Vector[int]): Tipo de datos comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es un vector y no contiene enteros
        
        **complejidad**:
            -   O(x+y) x: longitud de el vector, y: numero mas grande en el vector
        """
        self.__validarVectorYContenido(int, vector)
        conteo = self.__compactadorMetodosCountingSort(vector)
        self.__reordenamientoCountingVector(vector, conteo)

    def countingSortLista(self, lista:Lista[int]):
        """# COUNTING SORT
        
        ## Lista
        Dado un lista de numeros enteros positivos (de preferencia, todos más chicos que el largo de la lista)
        Cuenta cada uno de esos elementos. Una vez hecha las cuentas, calcula la posicion que le corresponde a cada
        elemento y los coloca allí

        **parameters**  
            -   lista (Lista[int]): Enteros positivos

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es una lista y no contiene enteros
        
        **complejidad**:
            -   O(x+y) x: longitud de la lista, y: numero mas grande en la lista
        """
        self.__validarVectorYContenido(int, lista)
        conteo = self.__compactadorMetodosCountingSort(lista)
        self.__reordenamientoCountingLista(lista, conteo)

    #RADIX SORT
    def __armarColas(self) -> Vector[Cola[int]]:
        colas = Vector(Cola, DIGITOS)

        for i in range(DIGITOS):
            colas[i] = Cola(int)

        return colas

    def __calcularIndiceRadix(self, numero:int, diezPotencia:int):
        return (numero // diezPotencia) %DIGITOS

    def __colaNumeros(self,estructura:Vector[int]|Lista[int], colasDigitos:Vector[Cola[int]], diezPotencia:int):
        for numero in estructura:
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

    def __reorganizarListaRadix(self, lista:Lista[int], colasDigitos:Vector[Cola[int]]):
        i = 0
        lista.activarCursorInicio()

        while lista.cursorPrendido():
            if colasDigitos[i].estaVacia():
                i+=1
            else:
                lista.setDatoCursor(colasDigitos[i].quitar())
                lista.avanzarCursor()

    def radixSortVector(self, vector:Vector[int]):
        """# RADIX SORT
        
        ## Vector
        Dado un vector de numeros enteros positivos (de preferencia, todos con una cantidad de
        digitos más pequña que la cantidad de elementos del vector) ordena cada uno de los nuemros 
        digito por digito. Osea, primero ordena las unidades de cada numero,
        luego las decenas, luego las centenas, y así sucesivamente

        **parameters**  
            -   vector (Vector[int]): Enteros positivos

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es un vector y no contiene enteros
        
        **complejidad**:
            -   O(x*y) x: longitud de el vector, y: cantidad de digitos del numero más grande
        """
        self.__validarVectorYContenido(int,vector)
        colasDigitos = self.__armarColas()
        digito = 1

        while (digito < max(vector)):
            self.__colaNumeros(vector,colasDigitos,digito)
            self.__reorganizarVectorRadix(vector,colasDigitos)
            digito*=DIGITOS

    def radixSortLista(self, lista:Lista[int]):
        """# RADIX SORT
        
        ## Lista
        Dada una lista de numeros enteros positivos (de preferencia, todos con una cantidad de
        digitos más pequeña que la cantidad de elementos de la lista) ordena cada uno de los nuemros 
        digito por digito. Osea, primero ordena las unidades de cada numero,
        luego las decenas, luego las centenas, y así sucesivamente

        **parameters**  
            -   lista (Lista[int]): Enteros positivos

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es una lista y no contiene enteros
        
        **complejidad**:
            -   O(x*y) x: longitud de la lista, y: cantidad de digitos del numero más grande
        """
        self.__validarListaYContenido(int, lista)
        colasDigitos = self.__armarColas()
        digito = 1
        while digito < max(lista):
            self.__colaNumeros(lista,colasDigitos,digito)
            self.__reorganizarListaRadix(lista,colasDigitos)
            digito*=DIGITOS

    #BUCKET SORT
    def __crearBaldes(self, tipoDatos:type, cantidad:int) -> Vector[Heap[T]]:
        baldes = Vector(Heap, cantidad)
        
        for i in range(cantidad):
            baldes[i] = Heap(tipoDatos)
        
        return baldes 

    def __organizarBaldesInt(self, estructura:Vector[int]|Lista[int], baldes:Vector[Heap[int]]):
        minimo = min(estructura)
        maximo = max(estructura)

        for numero in estructura:
            baldes[
                ((numero - minimo) * CANTIDAD_BALDES) // (maximo - minimo +1)
            ].agregar(numero)

    def __organizarBaldesFloat(self, estructura:Vector[float]|Lista[float], baldes:Vector[Heap[float]]):
            for decimal in estructura:
                if (decimal < 0) or (decimal > 1): 
                    raise ValueError("Este metodo solo funciona para flotantes entre 0 y 1")

                baldes[int(decimal//0.1)].agregar(decimal)


    def __ordenarBaldesVector(self, vector:Vector[T], baldes:Vector[Heap[T]]):
        i, j = PRIMERA_POSCICION, PRIMERA_POSCICION

        while i < vector.getLongitud():
            if baldes[j].estaVacio():
                j+=1
            else:
                vector[i] = baldes[j].quitar()
                i+=1

    def bucketSortVector(self, vector:Vector[int]):
        self.__validarVector(vector)
        baldes:Vector[Heap[int]]

        if issubclass(vector.getType(), int):
            baldes = self.__crearBaldes(int, CANTIDAD_BALDES)
            self.__organizarBaldesInt(vector,baldes)
        elif issubclass(vector.getType(), float):
            baldes = self.__crearBaldes(float, DIGITOS) 
            self.__organizarBaldesFloat(vector, baldes)
        else:
            raise TypeError("Ingrese un vector con enteros")

        self.__ordenarBaldesVector(vector, baldes)


    #ALGORITMOS DE BROMA

    #BOGO SORT
    def bogoSortVector(self, vector:Vector):
        """# BOGO SORT
        
        ## Vector
        - "¿Tu vector está desordenado? No te preocupes, voy a mezclarlo para ordenarlo." - mezcla el vector -
        "hmm... parrece que no está ordenado aún. Descuida, voy a mezclarlo de vuelta." - lo vuelve a mezclar -
        "okey... ¡ya está! ... no, esperá, sigue desordenado. Tranquilo lo voy a volver a mezclar...". 
        En eso, un tipo de la audiencia pregunta: -"¿Oye, cuanto tiempo lleva así?". Y otro espectador 
        responde: - "Pues, lleva así como desde hace unas dos semanas". 

        **parameters**  
            -   vector (Vector[int]): Tipo de dato comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es un vector
            -   **Incomparable**: si el tipo de datos de el vector no es comparables
        
        **complejidad**:
            -   O(x!) x: longitud de el vector
        """
        ordenado = self.vectorOrdenado(vector)

        while not ordenado:
            vector.mezclar()
            ordenado = self.vectorOrdenado(vector)

    def bogoSortLista(self, lista:Lista):
        """# BOGO SORT
        
        ## Lista
        - "¿Tu lista está desordenado? No te preocupes, voy a mezclarla para ordenarlo." - mezcla la lista -
        "hmm... parece que no está ordenada aún. Descuida, voy a mezclarla de vuelta." - la vuelve a mezclar -
        "okey... ¡ya está! ... no, esperá, sigue desordenada. Tranquilo la voy a volver a mezclar...". 
        En eso, un tipo de la audiencia pregunta: -"¿Oye, cuanto tiempo lleva así?". Y otro espectador 
        responde: - "Pues, lleva así como desde hace unas dos semanas". 

        **parameters**  
            -   lista (Vector[int]): Tipo de dato comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es una lista
            -   **Incomparable**: si el tipo de datos de la lista no es comparable
        
        **complejidad**:
            -   O(x!) x: longitud de la lista
        """
        ordenado = self.listaOrdenada(lista)
        
        while not ordenado:
            lista.mezclar()
            ordenado = self.listaOrdenada(lista)

    #MIRACLE SORT    
    def miracleSortVector(self, vector:Vector):
        """# MIRACLE SORT
        
        ## Vector
        "¡¡¡OID SIMPLES MORTALES LA PALABRA DE SORTI, EL SANTO DEL ORDEN!!! Cuando todo estaba desordenado, ¡él
        ordeno todo magicamente usando una particula cuantica para ordenar esté vector! ¡Que tu vector no se ordena?
        ¡Ten fe en Sorti que hará el milagro cuantico de llevar una particula de otra estrella para golpear el bit
        necesario para que este vector se ordene! ¡¡EL QUE TIENE FE PUEDE ENCONTRAS LA CONDICION NECESARIA Y SUFICIENTE
        PARA QUE UN GRAFO SEA HAMILTONIANO!!, ¡¡TAMBIÉN VERÁ ESE VECTOR ORDENADO!! ¡¡SIMPLEMENTE NO HAGAS ABSOLUTAMENTE
        NADA Y SORTI ORDENARÁ ESE VECTORRRRR!!

        **parameters**  
            -   vector (Vector[int]): Tipo de dato comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es un vector
            -   **Incomparable**: si el tipo de datos de el vector no es comparables
            -   **RecursionError**: si a Sorti no le pintó ordenar el vector
            -   **KeyboardInterruption**: si es que se te termina la paciencia de tanto esperar que Sorti te ordene el vector
            
        **complejidad**:
            -   infinito
        """
        try:
            ordenado = self.vectorOrdenado(vector)

            while not ordenado:
                ordenado = self.vectorOrdenado(vector)
        except KeyboardInterrupt:
            raise MalditoHereje("COMO TE ATREVEZ A DESAFIAR A SORTI")

    #STALIN SORT
    def stalinSortLista(self, lista:Lista):
        """# STALIN SORT
        
        ## Lista
        - "No se como, pero por alguna razón que desconozco, realmente nunca hubo necesidad de ordenar las listas.
        Cada vez que ingresan siempre llegan ordenadas" - "No es cierto. Soy un elemento de está lista y
        el elemento que está antes de mí es más grande que yo. Hace algo y ordename" - (SONIDO DE DISPARO) - 
        "GUARDIAS, LLEVENSE ESE CUERPO Y ENTIERRENLO EN LA FOSA COMÚN CON LOS DEMAS SUVERSIVOS... Como decía,
        las listas siempre llegan ordenadas a este algoritmo y nunca hay necesidad de ordenarlas."

        **parameters**  
            -   lista (Vector[int]): Tipo de dato comparable

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es una lista
            -   **Incomparable**: si el tipo de datos de la lista no es comparable
        
        **complejidad**:
            -   O(1) porque como dije, la lista siempre llega ordenada
        """
        self.__validarLista(lista)

        lista.activarCursorInicio()
        lista.avanzarCursor()

        while lista.cursorPrendido():
            if self.__esMenor(lista.getDatoCursor(),lista.getAnteriorCursor()):
                lista.extirparCursor()
            else:
                lista.avanzarCursor()

#VISUALIZADOR
TIEMPO_ENTRE_FRAMES = 0.0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001

LONGITUD_CORTA = 40
LONGITUD_LARGA = 200


COMPARACION = "red"
PIVOTE_QUICK = "cyan"
ORDENADO = "green"
FONDO = "black"
OTRAS_BARRAS = "white"

class Visualizador():
    @staticmethod
    def __iniciarAnimacion(longitud:int, titulo:str) -> tuple[Vector[int], BarContainer[Rectangle]]:
        if visualizacion:
            Visualizador.__validarLongitud(longitud)
            vector = Visualizador.__cargarVector(longitud)
            bars = Visualizador.__visualizador(vector, titulo) 
            plt.ion()

            return vector, bars
        else:
            raise ImportError("Instale Matplotlib para usar el visualizador")
    
    @staticmethod
    def __configurarBarras(bars:BarContainer[Rectangle], vector:Vector[int], i:int, color:str):
        bars[i].set_height(vector[i])
        bars[i].set_color(color)

    def __terminarAnimacion(bars:BarContainer, vector:Vector):
        Visualizador.__terminarDePintar(bars, vector)
        plt.ioff()
        plt.show()
    
    @staticmethod
    def __reiniciar(self):
        pass

    @staticmethod
    def __cargarVector(cantidad:int) -> Vector[int]:
        vector = Ordenador().generarVectorNumeros(cantidad)
        vector.mezclar()

        return vector

    @staticmethod
    def __validarLongitud(longitud:int):
        validarTipoObjeto(int, longitud, "Ingrese una longitud entera")
        validarNoNegativo(longitud, False, "Ingrese una longitud positiva")
    
    @staticmethod
    def __visualizador(vector:Vector[int], titulo:str) -> BarContainer[Rectangle]:
        fig, ax = plt.subplots()
        bars = ax.bar(range(vector.getLongitud()), vector)
        ax.axis("off")
        fig.patch.set_facecolor(FONDO)
        ax.set_title(titulo, color = OTRAS_BARRAS)

        return bars

    @staticmethod
    def __terminarDePintar(bars:BarContainer, vector:Vector):
        for i in range(vector.getLongitud()):    
            bars[i].set_color(ORDENADO)
            plt.pause(TIEMPO_ENTRE_FRAMES)

    #BUBBLE SORT
    @staticmethod
    def __framesBubble(vector:Vector):
        i = 0
        terminado = False

        while(i < vector.getLongitud() - 1) and not terminado:
            terminado = True
            for j in range(vector.getLongitud() - 1 - i):
                if vector[j] > vector[j+1]:
                    terminado = False
                    vector.intercambiar(j, j+1)

                yield i, j, j+1
    
            i+=1


    @staticmethod
    def verBubbleSort(longitud:int = LONGITUD_CORTA):
        vector, bars = Visualizador.__iniciarAnimacion(longitud, "Bubble Sort")

        for i, cmp1, cmp2 in Visualizador.__framesBubble(vector):
            for j in range(vector.getLongitud()):
                bars[j].set_height(vector[j])
                if j > vector.getLongitud() -1 -i:
                    color = ORDENADO
                elif j in (cmp1, cmp2):
                    color = COMPARACION
                else:
                    color = OTRAS_BARRAS
                Visualizador.__configurarBarras(bars, vector, j, color)
            plt.pause(TIEMPO_ENTRE_FRAMES)
        
        Visualizador.__terminarDePintar(bars, vector)
        plt.ioff()
        plt.show()

    #SELECTION SORT
    @staticmethod
    def __framesSelection(vector:Vector[int]):
        for i in range(vector.getLongitud()):
            menor = i
            for j in range(i, vector.getLongitud()):
                yield i, j, menor
                if vector[menor] > vector[j]:
                    menor = j

            vector.intercambiar(menor, i)

    def verSelectionSort(longitud:int):
        vector, bars = Visualizador.__iniciarAnimacion(longitud, "Selection Sort")

        for inicio, cmp, menor in Visualizador.__framesSelection(vector):
            for i in range(vector.getLongitud()):
                if i in (menor, cmp):
                    color = COMPARACION
                elif i == inicio:
                    color = PIVOTE_QUICK
                elif i < inicio:
                    color = ORDENADO
                else:
                    color = OTRAS_BARRAS
                Visualizador.__configurarBarras(bars,vector,i,color)
            plt.pause(TIEMPO_ENTRE_FRAMES) 

        Visualizador.__terminarAnimacion(bars, vector)
    
    #INSERTION SORT
    @staticmethod
    def __framesInsertion(vector:Vector[int]):
        for i in range(1,vector.getLongitud()):
            j = i - 1
            aux = vector[i]

            while (j >= 0) and vector[j] > aux: 
                vector.intercambiar(j, j+1)
                j-=1

                yield i, j, j+1

    @staticmethod
    def verInsertionSort(longitud:int):
        vector, bars = Visualizador.__iniciarAnimacion(longitud, "Insertion Sort")

        for pos, cmp1, cmp2 in Visualizador.__framesInsertion(vector):
            for i in range(vector.getLongitud()):
                color = OTRAS_BARRAS
                if i < pos:
                    color = ORDENADO
                if i == pos:
                    color = PIVOTE_QUICK 
                if i in (cmp1, cmp2):
                    color = COMPARACION
                Visualizador.__configurarBarras(bars, vector, i, color)
            plt.pause(TIEMPO_ENTRE_FRAMES)
                
        Visualizador.__terminarAnimacion(bars, vector)


    #QUICK SORT
    @staticmethod
    def __framesQuickSort(vector:Vector, inicio:int, fin:int, pivotes:set[int]):
        if fin - inicio > 0:
            i, j, piv = inicio+1, fin, inicio

            while (i <= j):
                if vector[i] <= vector[piv]:
                    i+=1
                elif vector[j] >= vector[piv]:
                    j-=1
                else:
                    vector.intercambiar(i,j)

                yield i, j, piv

            vector.intercambiar(i-1, piv)
            pivotes.add(i-1)

            yield from Visualizador.__framesQuickSort(vector, inicio, i-2, pivotes)
            yield from Visualizador.__framesQuickSort(vector, i, fin, pivotes)

    @staticmethod
    def verQuickSort(longitud:int = LONGITUD_LARGA):
        vector, bars = Visualizador.__iniciarAnimacion(longitud, "Quick Sort")
        pivotes = set({})

        for inicio, fin, pivote in Visualizador.__framesQuickSort(vector, 0, vector.getLongitud()-1, pivotes):
            
            for j in range(vector.getLongitud()):
                if j in pivotes:
                    color = ORDENADO
                elif j in (inicio, fin):
                    color = COMPARACION
                elif j == pivote:
                    color = PIVOTE_QUICK
                else:
                    color = OTRAS_BARRAS
                Visualizador.__configurarBarras(bars, vector, j, color)

            plt.pause(TIEMPO_ENTRE_FRAMES)
        
        Visualizador.__terminarAnimacion(bars, vector)

    #RADIX SORT
    @staticmethod
    def __generarColas():
        colas = Vector(Cola, DIGITOS)
        for i in range(DIGITOS):
            colas[i] = Cola(int)
        
        return colas

    @staticmethod
    def __cargarCola(vector:Vector[int], colas:Vector[Cola[int]], digito:int):
        for numero in vector:
            colas[(numero // digito) % 10].agregar(numero)

    @staticmethod
    def __retornarAlRadix(vector:Vector[int], colas:Vector[Cola[int]]):
        i,j  = 0, 0

        for i in range(vector.getLongitud()):
            if colas[j].estaVacia():
                j+=1

            vector[i] = colas[j].quitar()
            i+=1

    @staticmethod
    def __framesRadix(vector:Vector):
        colas = Visualizador.__generarColas()
        diezPotencia = 1

        while diezPotencia <= max(vector):
            Visualizador.__cargarCola(vector, colas, diezPotencia)
            Visualizador.__retornarAlRadix(vector, colas)
            yield OTRAS_BARRAS
            diezPotencia *= 10


    @staticmethod
    def verRadixSort(longitud:int):
        vector, bars = Visualizador.__iniciarAnimacion(longitud, "Radix Sort")
        
        for iteracion in Visualizador.__framesRadix(vector):
            for i in range(vector.getLongitud()):
                Visualizador.__configurarBarras(bars,vector,i, iteracion)

                plt.pause(TIEMPO_ENTRE_FRAMES)
        Visualizador.__terminarAnimacion(bars, vector)
