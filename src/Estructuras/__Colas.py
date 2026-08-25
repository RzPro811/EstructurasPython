from .__Validaciones import T, validarCondicion
from .__Heredables import TypeStruct, Generic
from .__Vector import PRIMERA_POSCICION, Generator
from .__Excepciones.Generales import *
from .__Lista import Lista


#COLA-------------------------------------------------------------------------------------------------------------------------------------------
class Cola(Generic[T], TypeStruct):
    #ATRIBUTOS
    __cola:Lista[T]

    #CONSTRUCTOR
    def __init__(self, tipo:type) -> Cola[T]:
        """Dado un tipo de elemento, crea una cola que almacena ese tipo de datos
        
        **parameters**
        -   **tipo** (type)

        **excepciones**
            -   **TypeError**: si el tipo ingresado no es type
        """
        super().__init__(tipo)
        self.__cola = Lista(tipo)

    #METODOS GENERALES
    def __str__(self) -> str:
        return "[COLA] "

    def __len__(self) -> int:
        return len(self.__cola)

    def __iter__(self) -> Generator[T]:
        while not self.estaVacia():
            yield self.quitar()

    #METODOS DE CLASE
    def estaVacia(self) -> bool:
        """Valida que la cola esté vacia
        
        **return**
            -   (bool) Verdadero si la cola no tiene elementos, falso si si
        """
        return self.__cola.estaVacia()

    def agregar(self, elemento:T) -> None:
        """Agrega un elemento a la cola
        
        **parameters**
            -   elemento (T)

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es del tipo ingresado T
        """
        self.__cola.agregarFinal(elemento)

    def quitar(self) -> T:
        """Quita el elemento que fue agregado antes que todos los demas de la cola
        
        **return**
            -   (T) primer elemento de la cola

        **excepciones**
            -   **VacioError**: si la cola está vacia
        """
        self.__validarColaVacia()
        return self.__cola.quitarInicio()
    
    #VALIDACIONES
    def __validarColaVacia(self) -> None:
        """Valida que la cola no esté vacía
        
        **excepciones**
            -   **VacioError**: si la cola está vacía
        """
        validarCondicion(self.estaVacia(), "La cola está vacía", VacioError)

    #GETTERS
    def getLongitud(self) -> int:
        """Obtiene la cantidad de elementos almacenados en la cola
        
        **return**
            -   (int) cantidad de items en la cola
        """
        return len(self)

#PILA-------------------------------------------------------------------------------------------------------------------------------------------
class Pila(Generic[T], TypeStruct):
    #ATRIBUTOS
    __pila:Lista[T]

    #CONSTRUCTOR
    def __init__(self, tipo:type) -> Pila[T]:
        """Dado un tipo de elemento, crea una pila que almacena ese tipo de datos
        
        **parameters**
        -   **tipo** (type)

        **excepciones**
            -   **TypeError**: si el tipo ingresado no es type
        """
        super().__init__(tipo)
        self.__pila = []

    #METODOS GENERALES
    def __str__(self) -> str:
        return "[PILA]"

    def __len__(self) -> int:
        return self.__pila.getLongitud()

    def __iter__(self) -> Generator[T]:
        while not self.estaVacia():
            yield self.quitar()

    #METODOS DE CLASE
    def estaVacia(self) -> bool:
        """Valida que la pila esté vacia
        
        **return**
            -   (bool) Verdadero si la pila no tiene elementos, falso si si
        """
        return self.__pila.estaVacia()

    def agregar(self, elemento:T) -> None:
        """Agrega un elemento a la pila
    
        **parameters**
            -   elemento (T)

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es del tipo ingresado T"""
        self.__pila.agregarFinal(elemento)

    def quitar(self) -> T:
        """Quita el ultimo elemento agregado a la pila
        
        **return**
            -   (T) ultimo elemento de la pila

        **excepciones**
            -   **VacioError**: si la pila está vacia
        """
        self.__validarPilaVacia()
        return self.__pila.quitarFinal()
    
    #VALIDACIONES
    def __validarPilaVacia(self) -> None:
        """Valida que la pila no esté vacía
        
        **excepciones**
            -   **VacioError**: si la pila está vacía
        """
        validarCondicion(self.estaVacia(), "La pila está vacía", VacioError)

    #GETTERS
    def getLongitud(self) -> int:
        """Obtiene la cantidad de elementos almacenados en la pila
        
        **return**
            -   (int) cantidad de items en la pila
        """
        return len(self)

#HEAP-------------------------------------------------------------------------------------------------------------------------------------------
class Heap(Generic[T], TypeStruct):
    #ATRIBUTOS
    __monton:list[T]
    __metodoOrdenamiento:function

    #CONSTRUCTORES
    def __init__(self, tipo:type, metodo =None) -> Heap[T]:
        """Crea el heap
        
        **parameters**
            -   tipo (type) tipo de los datos a almacenar
            -   metodo (function): metodo para ordenar los elementos del heap
        """
        super().__init__(tipo)
        self.__setMetodo(metodo)
        self.__monton = [None]

    #METODOS GENERALES
    def __repr__(self) -> str:
        return str(self.__monton)

    def __iter__(self) -> Generator[T]:
        while not self.estaVacio():
            yield self.quitar()

    #METODOS DE CLASE
    def agregar(self, elemento:T):
        """Agrega un nuevo elemento en la ultima poscicion del heap

        **parameters**
            -   elemento (T)

        **excepciones**
            - **TypeError**: si el tipo ingresado no es del tipo ingresado en el constructor 
        """
        
        self.__validarEntrada__(elemento)

        if (self.__estaLleno()): 
            self.__expandir()
         
        self.__monton[self.getCantidadElementos()] = elemento
        self.__ordenarDesdeAbajo(self.getCantidadElementos()-1)

    def quitar(self) -> T:
        """Quita el elemento de la raiz del heap
        
        **return**
            -   (T) elemento de la raiz

        **excepciones**
            -   **VacioError** si el heap esta vacio
        """
        validarCondicion(self.estaVacio(), "El Heap esta vacio", VacioError)

        elemento = self.__getRaiz()
        self.__setRaiz(self.__getItem(self.getCantidadElementos()-1))
        self.__monton[self.getCantidadElementos()-1] = None
        self.__ordenarDesdeArriba(PRIMERA_POSCICION)

        if self.__ultimoNivelVacio() and not self.estaVacio():
            self.__contraer()

        return elemento

    #METODOS INTERNOS
    def __estaLleno(self):
        """Verifica que el heap este lleno
        
        **return**
            -   (bool) Verdadero si ningun elemento es None, Falso si al menos uno es None
        """
        return self.__getItem(self.__getCapacidadMaxima()-1) is not None

    def __subArbolCompleto(self, poscicion:int)-> bool:
        """Dado una poscicion en el heap, verifica que un subarbol con raiz en el elemento de la poscicion, este completo
        
        **parameters**
            -   poscision (int)
        
        **return**
            -   (bool) Verdadero si el elemento no tiene hijos o si ambos hijos estan completos, falso si tiene un solo hijo o si ambos hijos estan incompletos 
        """
        if (not self.__tieneHijos(poscicion)):
            return True
        if (not self.__tieneAmbosHijos(poscicion)):
            return False
        return (self.__subArbolCompleto(self.__ubicacionHijoIzq(poscicion)) and self.__subArbolCompleto(self.__ubicacionHijoDer(poscicion)))

    def __generarMonton(self, tamanio:int) -> list[Generic[T]]:
        """Genera un monton
    
        **parameters**
            -   tamanio (int)

        **return**
            -   **list[Tipo Ingresado]** una lista llena de None 
        """
        return [None]*tamanio
    
    def __pow2(self, num:int) -> int:
        if num == 0:
            return 1
        return self.__pow2(num - 1) * 2

    def __ultimoNivelVacio(self):
        i = self.__getCapacidadMaxima()
        tramo = i/2  
        vacio = True
        
        while (i >= tramo) and vacio:
            i-= 1
            vacio = self.__getItem(i) is None

        return vacio

    def __ubicacionHijoIzq(self, poscicion:int) -> int:
        """Dada una poscicion del heap, retorna la poscicion del hijo izquierdo
        
        **parameters**
            -   poscicion (int)
        
        **return**
            -   (int) 2*poscicion+1
        """
        return  2*poscicion+1

    
    def __ubicacionHijoDer(self, poscicion:int) -> int:
        """Dada una poscicion del heap, retorna la poscicion del hijo derecho
        
        **parameters**
            -   poscicion (int)
        
        **return**
            -   (int) 2*poscicion+2
        """
        return  2*poscicion+2

    def __ubicacionPadre(self, poscicion:int) -> int:
        """Dada una poscicion del heap, retorna la poscicion del padre
        
        **parameters**
            -   poscicion (int)

        **return**
            -   (int) (poscicion-1)//2
        """

        return (poscicion-1)//2
    
    def __hijoIzquierdo(self, poscicion:int) -> T:
        """Dado una poscicion del heap, retorna al hijo izquierdo

        **parameters**
            -   poscicion (int)
        
        **return**
            -   (T) elemento en la poscicion 2*poscicion+1
        """
        return self.__getItem(self.__ubicacionHijoIzq(poscicion))
        
    def __hijoDerecho(self, poscicion:int) -> T:
        """Dado una poscicion del heap, retorna al hijo derecho

        **parameters**
            -   poscicion (int)
        
        **return**
            -   (T) elemento en la poscicion 2*poscicion+2
        """
        return self.__getItem(self.__ubicacionHijoDer(poscicion))

    def __tieneHijos(self, poscicion:int) -> bool :
        """Dada una posicicon del heap, verifica que el elemento en esa poscicion
        Tenga hijos
        
        **parameters**
            -   poscicion (int)

        **return**
            -   (bool) Verdadero si el elemento tiene al menos un hijo, falso si no tiene ningun hijo
        """ 
        try:
            return self.__hijoIzquierdo(poscicion) != None
        except Exception:
            return False

    
    def __tieneAmbosHijos(self, poscicion:int) -> bool :
        """Dada una posicicon del heap, verifica que el elemento en esa poscicion
        tenga ambos hijos
        
        **parameters**
            -   poscicion (int)

        **return**
            -   (bool) Verdadero si el elemento tiene ambos hijos, falso si no tiene al menos un hijo
        """ 
        try:
            return self.__hijoDerecho(poscicion) != None
        except Exception:
            return False

    def __expandir(self):
        """Expande la lista monton"""
        self.__monton.extend(self.__generarMonton(self.__pow2(self.getNiveles())))

    def __contraer(self):

        for i in range(self.__pow2(self.getNiveles() )):
            self.__monton.pop()
            
    
    def __intercambio(self, padre:int, hijo:int):
        """Dado la direccion de la semilla padre y la direccion de un hijo, los intercambia de lugar
        
        **parameters**
            -   padre (int) poscicion padre
            -   hijo (int) poscicion hijo
        """
        aux = self.__getItem(padre)
        self.__monton[padre] = self.__getItem(hijo)
        self.__monton[hijo] = aux

    def __esMenor(self, padre:Generic[T], hijo:Generic[T]) -> bool:
        """Dado el dato de una semilla padre y una semilla hijo, verifica que el padre sea menor que el hijo.
        Se hara la comparacion entre padre o hijo directamente si no hay un metodo especificado,
        si lo hay, se comparara el resultado del metodo al ingresarle los parametros padre o hijo.
        
        **parameters**
            -   padre (T)
            -   hijo (T)

        **return**
            -   (bool) verdadero si la comparacion verifica que padre es menor que hijo o que metodo(padre) es menor que metodo(hijo), falso si padre es mayor que hijo o si metodo(padre) es mayor que metodo(hijo)
        """
        if (self.__getMetodo() == None):
            return (padre < hijo)
        else:
            return self.__metodo(padre) < self.__metodo(hijo)
    
    def __organizarHeap(self, padre:int, hijo:int):
        """Dado dos posciciones, 
        presuntamente la de un elemento hijo y un elemento padre,
        intercambia los elementos si el elemento padre es mayor que el elemento hijo

        **parameters**
            -   padre (int)
            -   hijo (int)
        """
        if (not self.__esMenor(self.__getItem(padre),self.__getItem(hijo))):
            self.__intercambio(padre,hijo)


    def __hijoMenor(self, poscicion:int) -> int:
        """Dado una poscicion, retorna la ubicacion del hijo mas pequeño deñ elemento de la poscicion ingresada
         
        **parameters**
            -   poscicion (int)

        RETURNS:
            (int) 2*poscicion+1 o 2*poscicion+2
        """
        
        if self.__esMenor(self.__hijoIzquierdo(poscicion),self.__hijoDerecho(poscicion)):
            return self.__ubicacionHijoIzq(poscicion)
        return self.__ubicacionHijoDer(poscicion)
    
    
    def __ordenarDesdeAbajo(self, poscicion:int):
        """Ordena el heap desde un elemento hijo, en la poscicion ingresada, hasta la raiz
        
        **parameters**
            -   poscicion (int) poscicion hijo
        """
        if (poscicion > PRIMERA_POSCICION):
            self.__organizarHeap(self.__ubicacionPadre(poscicion), poscicion)
            self.__ordenarDesdeAbajo(self.__ubicacionPadre(poscicion))

    def __ordenarDesdeArriba(self,poscicion:int):
        """Ordena el heap desde un elemento padre, en la poscicion ingresada, hasta un elemento hijo
        
        **parameters**
            -   poscicion (int) poscicion padre
        """
        if (self.__tieneAmbosHijos(poscicion)):
            hijoMenor = self.__hijoMenor(poscicion)
            self.__organizarHeap(poscicion, hijoMenor)
            self.__ordenarDesdeArriba(hijoMenor)
        elif (self.__tieneHijos(poscicion)):
            self.__organizarHeap(poscicion,self.__ubicacionHijoIzq(poscicion))

    #METODOS ESTATICOS
    @staticmethod
    def ordenarPorMinimo(vector:list[Generic[T]], metodo = None):
        """dado un vector ingresado, se ordenan los elementos mediante el algoritmo HeapMinSort de menor a mayor.
        Si se ingresa un metodo, entonces se considerara el metodo para ser ordenado.

        **parameters**
            -   vector (list): todos los elementos deben ser el mismo tipo
            -   metodo (function): metodo comparable, por defecto None
        """
        heap = Heap(type(vector[0]), metodo)
        try:
            for elemento in vector:
                heap.agregar(elemento)        
            for i in range(len(vector)):
                vector[i] = heap.quitar()
        except TypeError:
            raise TypeError("Para que funcione el ordenamiento, todos los elementos de la lista ingresada deben ser del mismo tipo")

    @staticmethod
    def ordenarPorMaximo(vector:list[Generic[T]], metodo = None):
        """dado un vector ingresado, se ordenan los elementos mediante el algoritmo HeapMinSort de mayor a menor.
        Si se ingresa un metodo, entonces se considerara el metodo para ser ordenado.

        **parameters**
            -   vector (list): todos los elementos deben ser el mismo tipo
            -   metodo (function): metodo comparable, por defecto None
        """
        heap = Heap(type(vector[0]), metodo)
        try:
            for elemento in vector:
                heap.agregar(elemento)        
            for i in range(len(vector)-1,-1,-1):
                vector[i] = heap.quitar()
        except TypeError:
            raise TypeError("Para que funcione el ordenamiento, todos los elementos de la lista ingresada deben ser del mismo tipo")
                       
    #FLAGS    
    def estaVacio(self) -> bool:
        """Verifica que el heap este vacio
        
        **return**
            -    (bool) Verdadero si todos los elementos son None, falso si al menos uno no es None"""
        return (self.__getCapacidadMaxima() == 1) and (self.__getItem(PRIMERA_POSCICION) is None)

    def estaCompleto(self) -> bool:
        """Verifica que el heap este completo
        
        **return**
            -   (bool) Verdadero si todos los subarboles del heap estan completos, falso si al menos uno no lo esta"""

        return self.__subArbolCompleto(PRIMERA_POSCICION)

    #GETTERS
    def __getCapacidadMaxima(self) -> int:
        """Retora la capacidad maxima de elementos que entran en el heap
        """
        return len(self.__monton) 

    def getCantidadElementos(self) -> int:
        """Cuenta la cantidad de elementos no nulos en el heap
        
        **return**
            -   (int) cantidad elementos almacenados
        """
        esNulo = True
        i = self.__getCapacidadMaxima()

        while esNulo and (i > 0):
            esNulo = self.__getItem(i -  1) is None

            if  esNulo: i-=1

        return i

    def getNiveles(self) -> int:
        """Cuenta la cantidad de niveles del heap
        
        **return**
            -   (int) cantidad de niveles
            
        """
        niveles = 0
        elementoPorNivel = 1
        cantidadElementos = self.getCantidadElementos()

        while(cantidadElementos > 0):
                cantidadElementos-= elementoPorNivel
                niveles += 1
                elementoPorNivel*=2

        return niveles

    def __getItem(self, i:int) -> T:
        """Retorna el elemento en la poscicion i
        
        -   **parameters**
            -   i (int): entre 0 y el largo del vector
        
        -   **excepciones**
            -   **IndexError** : si el indice i se sale del rango
        """
        if ((i < 0) or (i>= len(self.__monton))): raise IndexError("Indice fuera de rango")
        return self.__monton[i]
    

    def __getRaiz(self) -> T:
        """Obtiene el elemento en la raiz del heap
        
        **return**
            -   (T) raiz del heap
        """
        return self.__getItem(PRIMERA_POSCICION)

    def __getMetodo(self):
        """Obtiene el metodo de comparacion
        
        **return**
            -   (function)
        """
        return self.__metodoOrdenamiento

    def __metodo(self, elemento:T):
        """Aplica el metodo de comparacion a un elemento del heap

        **parameters**:
            -   elemento (T): elemento en el heap

        **return**
            -  (T) el resultado de aplicarle el metodo al elemento 
        """
        return self.__metodoOrdenamiento(elemento)

    #SETTERS
    def __setRaiz(self, elemento:T):
        """Setea la raiz del heap
        
        **parameters**
            -   elemento (T) elemento del heap 
        """
        self.__monton[PRIMERA_POSCICION] = elemento
    
    def __setMetodo(self, metodo):
        """Obtiene el metodo de comparacion
        
        **return**
            -   (function)
        """
        validarCondicion(not callable(metodo) and (metodo is not None), "Ingresa un metodo para comparar en el ordenamiento",TypeError)
        self.__metodoOrdenamiento = metodo