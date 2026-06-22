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
            -   **bool** Verdadero si todos los elementos en el vector son null, falso si al menos uno no lo es
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
            -   **bool** Verdadero si ningun elemento del vector es null, falso si al menos uno lo es
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
            -  **bool** si el vector se expande al llenarse, falso si no
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
        """Quita el elemento en la poscicion ingresada por parametro
        
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
            -   **bool** Verdadero si el tramo final tiene unicamente elementos None, falso si al menos uno no lo es
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
class Heap(Generic[T], TypeStruct):
    #ATRIBUTOS
    __monton:Vector[T]
    __metodo:function

    #CONSTRUCTOR
    def __init__(self, tipo, metodo = None):
        super().__init__(tipo)
        self.__setMetodo(metodo)
        self.__monton = Vector(self.getType(),1)

    #METODOS GENERALES

    #METODOS DE CLASE
    
    #METODOS INTERNOS
    def __generarMonton(self, longitud):
        return Vector(self.getType(),longitud)
    
    #VALIDACIONES
    def __validarMetodo(self, metodo):
        validarCondicion((metodo is None) or (callable(metodo)), "Ingresa un metodo valido", MetodoInvalidoError)

    def __validarIndice(self, indice:int):
        validarTipoObjeto(int, indice, "Ingresa un indice int")
        validarRango(indice, PRIMERA_POSCICION, self.__getLongitud(), 
                     mensaje= f"Ingrese un indice entre {PRIMERA_POSCICION} y {self.__getLongitud()}") 

    #METODOS ESTATICOS
    
    #GETTERS

    #Calculables
    def __getLongitud(self) -> int:
        return len(self.__monton)
    
    def __getPosFinal(self) -> int:
        return self.__getLongitud() - 1
    
    def getNiveles(self) -> int:
        nivel = 0
        pow2 = 1
        escalones = 0

        while escalones < self.__getLongitud():
            escalones + pow2
            nivel+=1
            pow2*=2

        return nivel

    #Atributos
    def __getItem(self, indice:int) -> T:
        self.__validarIndice(indice)
        return self.__monton[indice]

    def __getMetodo(self, elemento:T) -> object:
        self.__validarEntrada__(elemento)
        return self.__metodo(elemento)

    def __getRaiz(self) -> T:
        return self.__getItem(PRIMERA_POSCICION)
    
    #SETTERS
    def __setItem(self, indice:int, entrada:T):
        self.__validarIndice(indice)
        self.__validarEntrada__(entrada)
        self.__monton[indice] = entrada
    
    def __setMetodo(self, metodo):
        self.__validarMetodo(metodo)

    def __setRaiz(self, entrada:T):
        self.__validarEntrada__(entrada)
        self.__monton[PRIMERA_POSCICION] = entrada