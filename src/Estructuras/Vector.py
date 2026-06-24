from .Validaciones import T, Generic, TypeStruct, validarTipoObjeto, validarRango, validarNoNegativo, validarCondicion
from .Excepciones.Generales import *
from typing import Generator
from random import shuffle

PRIMERA_POSCICION = 0

class Vector(Generic[T], TypeStruct):
    #ATRIBUTOS
    __longitudOriginal: int
    __array: list[T]
    __expansible: bool

    #CONSTRUCTOR
    def __init__(self, tipo:type, longitud:int, expandir:bool = False):
        """Dado un tipo de vector y una longitud crea un vector del tipo de dato ingresado
        
        **parameters**
            -   **tipo** (type): tipo de dato almacenable
            -   **longitud** (int): longitud del vector
            -   **expandir** (bool): por defecto False. Determina si el vector se va a expandir o no tras ser llenado
        """
        super().__init__(tipo)
        validarTipoObjeto(bool, expandir, "La condicion 'expandir' debe ser booleana")
        self.__setLongitudOriginal(longitud)
        self.__array = self.__generarVector(longitud)
        self.__expansible = expandir

    #METODOS GENERALES
    def __str__(self) -> str:
        cadena = "< "

        for item in self:
            cadena += f"{item}, "

        return cadena[:-2] + " >"
        
    def __len__(self) -> int:
        return len(self.__array)
    
    def __iter__(self) -> Generator[T] :
        for item in self.__array:
            yield item

    def __getitem__(self, key:int) -> T:
        self.__validarIndice(key)
        return self.__array[key]
    
    def __setitem__(self, key:int, value:T):
        self.__validarIndice(key)
        self.__validarEntrada__(value, True)
        self.__array[key] = value

    #METODOS DE CLASE
    def estaVacio(self) -> bool:
        """Verifica que el vector este vacío
        
        **return**
            -   (bool) Verdadero si todos los elementos en el vector son null, falso si al menos uno no lo es
        """
        vacio = True
        i = PRIMERA_POSCICION

        while vacio and (i <= self.__getPoscicionFinal()):
            vacio = self[i] is None
            i+=1

        return vacio
    
    def estaLleno(self) -> bool:
        """Verifica que el vector este lleno
        
        **return**
            -   (bool) Verdadero si ningun elemento del vector es null, falso si al menos uno lo es
        """
        lleno = True
        i = self.__getPoscicionFinal()

        while lleno and i >= PRIMERA_POSCICION:
            lleno = self[i] is not None
            i-=1
        
        return lleno

    def esExpansible(self) -> bool:
        """Valida que el vector se pueda expandir al llenarse
        
        **return**
            -  (bool) si el vector se expande al llenarse, falso si no
        """
        return self.__expansible
    
    def agregar(self, elemento:T):
        """Agrega un nuevo elemento al vector en la primera posicion que sea None
        
        **parameters**
            -   **elemento** (Generico): distinto de None

        **Excepciones**
            -   **TypeError** si el elemento no es del tipo ingresado o si es None
            -   **LlenoError** si el vector está lleno y no se puede expandir
        """
        self.__validarEntrada__(elemento)
        agregado = False
        i = PRIMERA_POSCICION

        if self.estaLleno():
            self.__validarExpansible()
            self.__expandir()

        while not agregado and (i <= self.__getPoscicionFinal()):
            if self[i] is None:
                self[i] = elemento
                agregado = True
            else: i+=1


    def quitar(self) -> T:
        """Quita el ultimo elemento que no sea None del vector
        
        **return**
            -   **T** Elemento removido

        **excepciones**
            -   **VacioError**: si el vector está vacío 
        """
        self.__validarNoVacio()
        quitado = False
        i = self.__getPoscicionFinal()
        
        while not quitado:
            if self[i] is not None:
                elemento = self.remover(i)
                quitado = True
            i-=1
        
        if self.__tramoFinalVacio() and (self.getLongitud() != self.__getLongitudOriginal()):
            self.__contraer()

        return elemento


    def remover(self, indice:int) -> T:
        """Quita el elemento en la poscicion ingresada por **parameters**        
        **parameters**
            -   **indice** (int): entre 0 y la longitud del vector - 1 

        **return**
            -   **T** Elemento removido

        **excepciones**
            -   **TypeError**: si el indice ingresado no es tipo int
            -   **IndexError**: si el indice ingresado está fuera de rango
        """
        self.__validarIndice(indice)

        elemento = self[indice]
        self[indice] = None

        return elemento


    def intercambiar(self, indice:int, jndice:int):
        """Dadas dos posciciones del vector, intercambia los elementos en esas dos posciciones
        
        **parameters**
            -   **indice** (int): entre 0 y la longitud del vector - 1
            -   **jndice** (int): entre 0 y la longitud del vector - 1
        
        **excepciones**
            -   **TypeError** Si alguno de los dos indices no es valido
            -   **IndexError** Si alguno de los dos indeces se sale del rango permitido
        """
        self.__validarIndice(indice)
        self.__validarIndice(jndice)

        aux = self[indice]
        self[indice] = self[jndice]
        self[jndice] = aux

    def mezclar(self):
        """Mezcla los elementos en el vector, por mera diversion"""
        shuffle(self.__array) 

    def vaciar(self):
        """Vacia el vector"""
        self.__array = self.__generarVector(self.__getLongitudOriginal())
    

    #METODOS INTERNOS
    def __generarVector(self, longitud:int) -> list[T]:
        """Dada una longitud, retorna una lista de esa longitud unicamente con elementos None
        
        **parameters**
            -   **longitud** (int)

        **return**
            -   **list[None]** lista de elementos None con la longitud ingresada   
        """
        return [None]*longitud

    def __tramoFinalVacio(self) -> bool:
        """Verifica que el ultimo tramo de expansión del vector, este vacío
        
        **return**
            -   (bool) Verdadero si el tramo final tiene unicamente elementos None, falso si al menos uno no lo es
        """
        vacio = True
        i = self.__getPoscicionFinal()

        while vacio and (i > self.__getLongitudOriginal() - self.__getLongitudOriginal()):
            vacio = self[i] is None
            i-=1

        return vacio

    def __expandir(self):
        """Expande el vector"""
        self.__array.extend(self.__generarVector(self.__getLongitudOriginal()))

    def __contraer(self):
        """Contrae el vector"""
        for i in range(self.__getLongitudOriginal()):
            self.__array.pop()

    #VALIDACIONES
    def __validarIndice(self, indice:int):
        """Valida que el indice se encuentre el rango del vector"""
        validarRango(indice, PRIMERA_POSCICION,self.__getPoscicionFinal(),
                     mensaje= f"Ingresa un valor entre {PRIMERA_POSCICION} y {self.__getPoscicionFinal()}")

    def __validarExpansible(self):
        """Valida que el vector se pueda expandir"""
        validarCondicion(not self.esExpansible(),
                         "El vector está lleno y no se puede expandir", LlenoError)

    def __validarNoVacio(self):
        """Valida que el vector no este vacío"""
        validarCondicion(self.estaVacio(), "El vector está vacío", VacioError)

    #GETTERS

    #Atributos Calculables
    def getLongitud(self) -> int:
        return len(self)

    def getCantidadElementos(self) -> int:
        elementos = 0

        for item in self:
            if item is not None:
                elementos +=1
        
        return elementos

    def __getPoscicionFinal(self) -> int:
        return self.getLongitud() - 1


    #Atributos reales
    def __getLongitudOriginal(self) -> int:
        return self.__longitudOriginal
    

    #SETTERS
    def __setLongitudOriginal(self, longitud:int):
        validarNoNegativo(longitud,False, "Ingrese una longitud positiva", LongitudNegativaError)
        self.__longitudOriginal = longitud
        

#MATRIZ-----------------------------------------------------------------------------------------------------------------------------------------
class Matriz(Generic[T], TypeStruct):
    #ATRIBUTOS
    __array:Vector[Vector[T]]
    
    #CONSTRUCTORES
    def __init__(self, tipo, longitudColu:int, longitudFila:int):
        validarNoNegativo(longitudFila, False, "Ingrese una longitud Positiva", LongitudNegativaError)
        validarNoNegativo(longitudColu, False, "Ingrese una longitud Positiva", LongitudNegativaError)

        self.__array = Vector(Vector,longitudColu)

        for i in range(longitudColu):
            self.__array[i] = Vector(tipo, longitudFila)

        super().__init__(tipo)

    #METODOS GENERALES
    def __str__(self) -> int:
        cadena = "\n"

        for fila in self.__array:
            cadena += str(fila) + "\n"

        return cadena
    def __len__(self):
        return self.getLongitudFila() * self.getLongitudColu()
    def __iter__(self) -> Generator[T]:
        for fila in self.__array:
            for item in fila:
                yield item

    #METODOS DE CLASE
    def estaLleno(self) -> bool:
        lleno = True

        i =self.__getUltimaPosColu()

        while lleno and (i >= PRIMERA_POSCICION):
            j = self.__getUltimaPosFila()

            while lleno and (j >= PRIMERA_POSCICION):
                lleno = self.getItem(i,j) is not None
                j-=1

            i-=1

        return lleno

    def estaVacio(self) -> bool:
        vacio = True

        i = PRIMERA_POSCICION
        
        while vacio and (i<=self.__getUltimaPosColu()):
            j = PRIMERA_POSCICION

            while vacio and (j<= self.__getUltimaPosFila()):
                vacio = self.getItem(i,j) is None
                j+=1
            i+=1

        return vacio


    def esCuadrada(self):
        return self.getLongitudFila() == self.getLongitudColu()
    
    def esSimetrica(self):
        simetrica = self.esCuadrada()
        i = PRIMERA_POSCICION

        while simetrica and (i <= self.__getUltimaPosColu()):
            j = i+1
            while simetrica and (j <= self.__getUltimaPosFila):
                simetrica = self.getItem(i,j) == self.getItem(j,i)
                j+=1
            i+=1

        return simetrica

    def agregar(self, elemento:T):
        self.__validarEntrada__(elemento)
        agregado = False
        i = PRIMERA_POSCICION

        while (i <= self.__getUltimaPosColu()) and not agregado:
            j = PRIMERA_POSCICION
            
            while (j <= self.__getUltimaPosFila()) and not agregado:
                
                if self.getItem(i,j) is None:
                    self.setItem(i,j,elemento)
                    agregado = True
                
                j+=1
            
            i+=1

    def copiar(self) -> Matriz[T]:
        matriz = Matriz(self.getType(),self.getLongitudColu(), self.getLongitudFila())
        
        for item in self:
            matriz.agregar(item)

        return matriz

    #VALIDACIONES
    def __validarIndiceFila(self, indice:int):
        validarRango(indice,PRIMERA_POSCICION,self.__getUltimaPosFila(),
                     mensaje= f"Ingresa un poscicion entre {PRIMERA_POSCICION} y {self.__getUltimaPosFila()}")

    def __validarIndiceColu(self, indice:int):
        validarRango(indice,PRIMERA_POSCICION,self.__getUltimaPosColu(),
                     mensaje= f"Ingresa un poscicion entre {PRIMERA_POSCICION} y {self.__getUltimaPosColu()}")
        
    def __validarIndices(self, indice:int, jndice:int):
        self.__validarIndiceColu(indice)
        self.__validarIndiceFila(jndice)

    #GETTERS
    def getCantidadElementos(self) -> int:
        elementos = 0

        for item in self:
            if item is not None:
                elementos+=1

        return elementos

    def getLongitudFila(self) -> int :
        return len(self.__array[PRIMERA_POSCICION])
    def getLongitudColu(self) -> int :
        return len(self.__array)

    def getItem(self, indice:int, jndice:int) -> T:
        self.__validarIndices(indice, jndice)
        return self.__array[indice][jndice]

    def __getUltimaPosFila(self) -> int :
        return self.getLongitudFila() -1
    def __getUltimaPosColu(self) -> int :
        return self.getLongitudColu() -1

    #SETTERS
    def setItem(self, indice:int, jndice:int, elemento:T):
        self.__validarIndices(indice,jndice)
        self.__validarEntrada__(elemento, True)
        self.__array[indice][jndice] = elemento

#COLA-------------------------------------------------------------------------------------------------------------------------------------------
class Cola(Generic[T], TypeStruct):
    #CONSTANTES
    __PRIMER_DATO = 0
    #ATRIBUTOS
    __cola:list[T]

    #CONSTRUCTOR
    def __init__(self, tipo:type):
        """Dado un tipo de elemento, crea una cola que almacena ese tipo de datos
        
        **parameters**
        -   **tipo** (type)

        **excepciones**
            -   **TypeError**: si el tipo ingresado no es type
        """
        super().__init__(tipo)
        self.__cola = []

    #METODOS GENERALES
    def __str__(self):
        return "[COLA] proximo elemento a salir: " +str(self.__cola[self.__PRIMER_DATO])

    def __len__(self):
        return len(self.__cola)

    #METODOS DE CLASE
    def estaVacia(self):
        return len(self) != 0

    def agregar(self, elemento:T):
        self.__validarEntrada__(elemento)
        self.__cola.append(elemento)

    def quitar(self) -> T:
        self.__validarColaVacia()
        return self.__cola.pop(self.__PRIMER_DATO)
    
    #VALIDACIONES
    def __validarColaVacia(self):
        validarCondicion(self.estaVacia(), "La cola está vacía", VacioError)

    #GETTERS
    def getLongitud(self):
        return len(self)

#PILA-------------------------------------------------------------------------------------------------------------------------------------------

class Pila(Generic[T], TypeStruct):
    #ATRIBUTOS
    __pila:list[T]

    #CONSTRUCTOR
    def __init__(self, tipo:type):
        """Dado un tipo de elemento, crea una pila que almacena ese tipo de datos
        
        **parameters**
        -   **tipo** (type)

        **excepciones**
            -   **TypeError**: si el tipo ingresado no es type
        """
        super().__init__(tipo)
        self.__pila = []

    #METODOS GENERALES
    def __str__(self):
        return "[PILA] proximo elemento a salir: " +str(self.__pila[self.getLongitud()-1])

    def __len__(self):
        return len(self.__pila)

    #METODOS DE CLASE
    def estaVacia(self):
        return len(self) != 0

    def agregar(self, elemento:T):
        self.__validarEntrada__(elemento)
        self.__pila.append(elemento)

    def quitar(self) -> T:
        self.__validarColaVacia()
        return self.__pila.pop()
    
    #VALIDACIONES
    def __validarColaVacia(self):
        validarCondicion(self.estaVacia(), "La cola está vacía", VacioError)

    #GETTERS
    def getLongitud(self):
        return len(self)

#HEAP-------------------------------------------------------------------------------------------------------------------------------------------
class Heap(Generic[T], TypeStruct):#CONSTANTES
    POSCICION_RAIZ = 0

    #ATRIBUTOS
    __monton:Vector[T]
    __metodo:function

    #CONSTRUCTORES
    def __init__(self, tipo:type, metodo =None):
        """Crea el heap
        
        **parameters**
            -   tipo (type) tipo de los datos a almacenar
        """
        if (not callable(metodo) and (metodo is not None)): raise TypeError("Se debe ingresar una funcion que retorna comparables")

        super().__init__(tipo)
        self.__setMetodo(metodo)
        self.__monton = Vector(self.getType(),1)

    #METODOS GENERALES
    def __repr__(self) -> str:
        """No tengo ni idea que hace esta cosa pero sirve bien para ver el contenido del heap al debuguear"""
        return str(self.__monton)

    #METODOS DE CLASE
    def estaVacio(self) -> bool:
        """Verifica que el heap este vacio
        
        **return**
            -    (bool) Verdadero si todos los elementos son None, falso si al menos uno no es None"""

        i = 0
        vacio = True

        while (vacio and (i < self.getCantidadElementos())):
            vacio = self.__monton[i] == None
            i += 1

        return bool

    def estaCompleto(self) -> bool:
        """Verifica que el heap este completo
        
        **return**
            -   (bool) Verdadero si todos los subarboles del heap estan completos, falso si al menos uno no lo esta"""

        return self.__subArbolCompleto(self.POSCICION_RAIZ)

    def agregar(self, elemento:T):
        """Agrega un nuevo elemento en la ultima poscicion del heap

        **parameters**
            -   elemento (T)

        **excepciones**
            - **TypeError**: si el tipo ingresado no es del tipo ingresado en el constructor 
        """
        
        self.__validarEntrada__(elemento)
        
        self.__monton[self.getCantidadElementos()] = elemento
        if (self.__estaLleno()): self.__expandir()
        self.__ordenarDesdeAbajo(self.getCantidadElementos()-1)

    def quitar(self) -> T:
        """Quita el elemento de la raiz del heap
        
        **return**
            -   (T) elemento de la raiz

        **excepciones**
            -   **ErrorRegistroVacio** si el heap esta vacio
        """
        validarCondicion(self.estaVacio(), "El Heap esta vacio", VacioError)

        elemento = self.__getRaiz()
        self.__setRaiz(self.__getItem(self.getCantidadElementos()-1))
        self.__monton[self.getCantidadElementos()-1] = None
        self.__ordenarDesdeArriba(self.POSCICION_RAIZ)
        return elemento

    #METODOS INTERNOS

    def __estaLleno(self):
        """Verifica que el heap este lleno
        
        **return**
            -   (bool) Verdadero si ningun elemento es None, Falso si al menos uno es None
        """
        lleno = True
        i = 0

        while (lleno and (i < self.getCantidadElementos())):
            lleno = (self.__monton[i] != None)
            i+=1
        
        return lleno

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
        montonNuevo = self.__generarMonton(self.getCantidadElementos()+self.getNiveles()*2)
        for i in range(self.getCantidadElementos()):
            montonNuevo[i] = self.__getItem(i) 

        self.__monton = montonNuevo
    
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
        si lo hay, se comparara el resultado del metodo al ingresarle el **parameters**padre o hijo.
        
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
        if (poscicion > self.POSCICION_RAIZ):
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

            -   vector **list**: todos los elementos deben ser el mismo tipo
            -   metodo **function**: metodo comparable, por defecto None
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

            -   vector **list**: todos los elementos deben ser el mismo tipo
            -   metodo **function**: metodo comparable, por defecto None
        """
        heap = Heap(type(vector[0]), metodo)
        try:
            for elemento in vector:
                heap.agregar(elemento)        
            for i in range(len(vector)-1,-1,-1):
                vector[i] = heap.quitar()
        except TypeError:
            raise TypeError("Para que funcione el ordenamiento, todos los elementos de la lista ingresada deben ser del mismo tipo")
                       

    #GETTERS
    def getCapacidadMaxima(self) -> int:
        return len(self.__monton) 

    def getCantidadElementos(self) -> int:
        """Cuenta la cantidad de elementos no nulos en el heap
        
        **return**
            -   (int) cantidad elementos almacenados
        """
        esNulo = True
        i = self.getCapacidadMaxima()

        while (i > 0) and esNulo:
            esNulo = self.__getItem(i-1) is None
            i-= 1
            
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
        return self.__getItem(self.POSCICION_RAIZ)

    def __getMetodo(self):
        """Obtiene el metodo de comparacion
        
        **return**
            -   (function)
        """
        return self.__metodoOrdenamiento

    def __metodo(self, elemento:T):
        """Aplica el metodo de comparacion a un elemento del heap

        PARAMETOS:
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
        self.__monton[self.POSCICION_RAIZ] = elemento