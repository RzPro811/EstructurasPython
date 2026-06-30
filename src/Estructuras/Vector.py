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
    def __init__(self, tipo:type, longitudColu:int, longitudFila:int):
        """Dado dos longitudes, colu y fila, y un tipo de dato, crea una matriz con ese tipo de datos

        **parameters**
            -   tipo (type) 
            -   longitudColu (int): mayor que cero
            -   longitudFila (int): mayor que cero
        
        **excepciones**
            -   **TypeError** si alguno de los parametros no es del tipo especificado
            -   **LongitudNegativaError** si alguna longitud ingresada es negativa
        """
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
        """Verifica que la matriz esté llena
        
        **retunr**
            -   (bool) verdadero si no hay valores None en la matriz, falso si hay al menos un item None
        """
        lleno = True

        i =self.__getUltimaPosColu()

        while lleno and (i >= PRIMERA_POSCICION):
            j = self.__getUltimaPosFila()

            while lleno and (j >= PRIMERA_POSCICION):
                lleno = self.getItem(i,j) is not None
                j-=1

            i-=1

        return lleno
    
    def filaLlena(self, indice:int) -> bool:
        self.__validarIndiceColu(indice)
        i = PRIMERA_POSCICION
        llena = True

        while llena and (i < self.getLongitudFila()):
            llena = self.getItem(indice, i) is not None
            i+=1

        return llena
    
    def columnaLlena(self, indice:int) -> bool:
        self.__validarIndiceFila(indice)
        i = PRIMERA_POSCICION
        llena = True

        while llena and (i < self.getLongitudColu()):
            llena = self.getItem(i, indice) is not None
            i+=1

        return llena

    def estaVacio(self) -> bool:
        """Verifica que la matriz esté vacía
        
        **return**
            -   (bool) Verdadero si todos los elementos son None, falso si al menos uno no lo es
        """
        vacio = True

        i = PRIMERA_POSCICION
        
        while vacio and (i<=self.__getUltimaPosColu()):
            j = PRIMERA_POSCICION

            while vacio and (j<= self.__getUltimaPosFila()):
                vacio = self.getItem(i,j) is None
                j+=1
            i+=1

        return vacio

    
    def filaVacia(self, indice:int) -> bool:
        self.__validarIndiceColu(indice)
        i = self.__getUltimaPosFila()
        vacia = True

        while vacia and (i >= PRIMERA_POSCICION):
            vacia = self.getItem(indice, i) is None
            i-=1

        return vacia
    
    def columnaVacia(self, indice:int) -> bool:
        self.__validarIndiceFila(indice)
        i = self.__getUltimaPosColu()
        vacia = True

        while vacia and (i >= PRIMERA_POSCICION):
            vacia = self.getItem(i, indice) is None
            i-=1

        return vacia
            

    def esCuadrada(self):
        """Verifica que la matriz sea cuadrada
        
        **return**
            -   (bool) Verdadero si las filas y las longitudes miden exactamente lo mismo, falso si no
        """
        return self.getLongitudFila() == self.getLongitudColu()
    
    def esSimetrica(self):
        """Verifica que la matriz sea simetrica
        
        **return**
            -   (bool) verdadero si, para poscicion (i,j) en la matriz, se encuentra el mismo elemento en la poscicion (j,i)
            falso si al menos en una poscicion (i,j) hay un elemento distinto en la poscicion (j,i)
        """
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
        """Agrega un elemento en la primera poscicion vacía en la matriz
        
        **parameters**
            -   elemento (T): no puede ser None

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es del tipo ingresado T
        """
        self.__validarEntrada__(elemento)
        self.__validarNoLleno(elemento)
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

    def agregarEnFila(self, indice:int, elemento:T):
        self.__validarEntrada__(elemento)
        self.__validarFilaNoLlena(indice)

        i = PRIMERA_POSCICION
        agregado = False
        
        while not agregado and (i <= self.__getUltimaPosFila()):
            if self.getItem(indice,i) is None:
                agregado = True
                self.setItem(indice,i,elemento) 

    def agregarEnColumna(self, indice:int, elemento:T):
        self.__validarEntrada__(elemento)
        self.__validarColumnaNoLlena(indice)

        i = PRIMERA_POSCICION
        agregado = False
        
        while not agregado and (i <= self.__getUltimaPosColu()):
            if self.getItem(i,indice) is None:
                agregado = True
                self.setItem(i,indice,elemento) 

    def remover(self, indice:int, jndice:int) -> T:
        self.__validarIndices(indice,jndice)

        elemento = self.getItem(indice,jndice)
        self.setItem(indice,jndice, None)

        return elemento


    def copiar(self) -> Matriz[T]:
        matriz = Matriz(self.getType(),self.getLongitudColu(), self.getLongitudFila())
        
        for item in self:
            matriz.agregar(item)

        return matriz

    def expandir(self, datoInicial:T = None, cantidad:int = 1):
        self.__validarEntrada__(datoInicial)
        validarNoNegativo(cantidad,False, "Ingresa una cantidad positiva para la expancion", LongitudNegativaError)


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

    def __validarNoLleno(self):
        validarCondicion(self.estaLleno(),"La matriz está llena", LlenoError)

    def __validarFilaNoLlena(self,indice):
        self.__validarIndiceColu(indice)
        validarCondicion(self.filaLlena(indice),f"La fila {indice} está llena", LlenoError)
        
    def __validarColumnaNoLlena(self,indice):
        self.__validarIndiceFila(indice)
        validarCondicion(self.columnaLlena(indice),f"La fila {indice} está llena", LlenoError)
        

    #GETTERS
    def getCantidadElementos(self) -> int:
        elementos = 0

        for item in self:
            if item is not None:
                elementos+=1

        return elementos
    
    def getFila(self, indice:int):
        self.__validarIndiceColu(indice)
        
        return self.__array[indice]

    def getColumna(self, indice:int):
        self.__validarIndiceFila(indice)
        vector = Vector(self.getType(),self.getLongitudColu())

        for i in range(self.getLongitudColu()):
            vector[i] = self.__array[i][indice]

        return vector

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

