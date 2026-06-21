from .Validaciones import T, Generic, TypeStruct, validarTipoObjeto, validarRango, validarNoNegativo, validarCondicion
from .Excepciones.Generales import *
from typing import Generator
from random import shuffle

class Vector(Generic[T], TypeStruct):
    #CONSTANTES
    __PRIMERA_POSCICION = 0

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
        i = self.__PRIMERA_POSCICION

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

        while lleno and i >= self.__PRIMERA_POSCICION:
            lleno = self[i] is not None
            i-=1
        
        return lleno

    def esExpansible(self) -> bool:
        """Valida que el vector se pueda expandir al llenarse
        
        **return**
            -  **bool** si el vector se expande al llenarse, falso si no
        """
        return self.__expansible
    
    def agregar(self, elemnto:T):
        """Agrega un nuevo elemento al vector en la primera posicion que sea None
        
        **parameters**
            -   **elemento** (Generico): distinto de None

        **Excepciones**
            -   **TypeError** si el elemento no es del tipo ingresado o si es None
            -   **LlenoError** si el vector está lleno y no se puede expandir
        """
        self.__validarEntrada__(elemnto)
        agregado = False
        i = self.__PRIMERA_POSCICION

        if self.estaLleno():
            self.__validarExpansible()
            self.__expandir()

        while not agregado and (i <= self.__getPoscicionFinal()):
            if self[i] is None:
                self[i] = elemnto
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
        validarRango(indice, Vector.__PRIMERA_POSCICION,self.__getPoscicionFinal(),
                     mensaje= f"Ingresa un valor entre {Vector.__PRIMERA_POSCICION} y {self.__getPoscicionFinal()}")

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
#LISTA------------------------------------------------------------------------------------------------------------------------------------------

class Lista(Generic[T], TypeStruct):
    #ATRIBUTOS
    __lista:list[Generator[T]]

    #CONSTRUCTOR
    def __init__(self, tipo):
        super().__init__(tipo)
        self.__lista = []

#COLA-------------------------------------------------------------------------------------------------------------------------------------------
#PILA-------------------------------------------------------------------------------------------------------------------------------------------
#HEAP-------------------------------------------------------------------------------------------------------------------------------------------
