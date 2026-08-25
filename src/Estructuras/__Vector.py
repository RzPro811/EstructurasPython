from .__Validaciones import *
from .__Excepciones.Generales import *
from .__Heredables import TypeStruct
from typing import Generator, Generic, Iterable
from random import shuffle

class TipoExpansion(Enum):
    AUTOMATICA = "AUTOMATICA"
    DESACTIVADA = "DESACTIVADA"
    MANUAL = "MANUAL"

class Vector(Generic[T], TypeStruct):
    #ATRIBUTOS
    __longitudOriginal: int
    __array: list[T]
    __tipoExpansion: TipoExpansion

    #CONSTRUCTOR
    def __init__(self, tipo:type, longitud:int, tipoExpansion:TipoExpansion = TipoExpansion.DESACTIVADA) -> Vector[T]:
        """Dado un tipo de vector y una longitud crea un vector del tipo de dato ingresado
        
        **parameters**
            -   **tipo** (type): tipo de dato T
            -   **longitud** (int): longitud del vector
            -   **tipoExpansion** (bool): DESACTIVADA (por defecto), AUTOMATICA o MANUAL

        **excepciones**
            -   **TypeError**: Si ninguno de los parametros ingresados es el indicado por parametro
            -   **LongitudNegativaError**: Si la longitud ingresada es menor o igual a cero
        """
        super().__init__(tipo)
        self.__setLongitudOriginal(longitud)
        self.__setTipoExpansion(tipoExpansion)
        self.__array = self.__generarVector(longitud)

    #METODOS GENERALES
    def __str__(self) -> str:
        cadena = "< "

        for item in self:
            cadena += f"{item}, "

        return cadena[:-2] + " >"
    
    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self.__array)
    
    def __iter__(self) -> Generator[T] :
        for item in self.__array:
            yield item

    def __getitem__(self, key:int) -> T:
        self.__validarIndice(key)
        return self.__array[key]
    
    def __setitem__(self, key:int, value:T) -> None:
        self.__validarIndice(key)
        self.__validarEntrada__(value, True)
        self.__array[key] = value

    #METODOS DE CLASE
    def agregar(self, elemento:T) -> None:
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
            self.__validarExpansionAutomatica()
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

    def expandir(self, expansiones:int = 1) -> None:
        """Expande manualmente el vector, añadiendo tantos espacios como haya tenído el vector al momento de crearse
        
        **parameters**
            -   expansiones (int): por defecto 1. Si ingresa un numero mayor, entonces el vector se expandirá esa cantidad de veces

        **Excepciones**
            -   **MetodoInvalidoError** Si el vector no tiene tipo de expansión MANUAL
            -   **TypeError** Si el parametro ingresado no es un int
            -   **ImplosionError** Si la cantidad de expansiones no es una cantidad estrictamente positiva
        """
        self.__validarExpansionManual()
        validarTipoObjeto(int, expansiones, "Ingresa una cantidad de expansiones entera")
        validarNoNegativo(expansiones,False,"Ingrese un numero de expansión mayor o igual que 1", ImplosionError)

        for i in range(expansiones):
            self.__expandir()

    def contraer(self, contracciones:int = 1) -> None:
        """Contrae manualmente el vector, quitando tantos espacios como haya tenído el vector al momento de crearse
        
        **parameters**
            -   expansiones (int): por defecto 1. Si ingresa un numero mayor, entonces el vector se contraerá esa cantidad de veces

        **Excepciones**
            -   **MetodoInvalidoError** Si el vector no tiene tipo de expansión MANUAL
            -   **TypeError** Si el parametro ingresado no es un int
            -   **ImplosionError** Si la cantidad de contracciones no es una cantidad estrictamente positiva
        """
        self.__validarExpansionManual()
        validarTipoObjeto(int, contracciones, "Ingresa una cantidad de contracciones entera")
        validarNoNegativo(contracciones, False, "Ingresa un numero de contracción mayor o igual que 1", ImplosionError)

        while (self.estaExpandido() and (contracciones > 0)):
            self.__contraer()
            contracciones -= 1

    def intercambiar(self, indice:int, jndice:int) -> None:
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

    def mezclar(self) -> None:
        """Mezcla los elementos en el vector, por mera diversion"""
        shuffle(self.__array) 

    def invertir(self) -> None:
        """Invierte la lista poniendo los datos en la poscicion n en la poscion longitud - n"""
        for i in range(self.getLongitud()//2):
            self.intercambiar(i, self.getLongitud()-1-i)

    def vaciar(self) -> None:
        """Vacia el vector"""
        self.__array = self.__generarVector(self.__getLongitudOriginal())

    def copiar(self) -> Vector[T]:
        """Crea una copia exacta del vector
        
        **return**
            -   (Vector[T]) un vector con los mismos elemento dentro suyo
        """
        copia = Vector(self.getType(), self.__getLongitudOriginal(), self.esExpansible())

        copia.__array = self.__array.copy()

        return copia

    def copiarContendio(self, vector:Vector[T]) -> None:
        """Dado un vector vacio, copia el contenido de este vector al otro vector
        
        **parameters**
            -   vector (Vector[T]): Vacio, mismo tipo de dato que este vector y longitud mayor o igual a la de este vector
        
        **excepciones**
            -   **TypeError** si lo ingresado no es un vector o el tipo de dato del contenido es distinto
            -   **ImplosionError** si el vector ingresado mide menos de lo que mide este vector
        """
        validarTipoObjeto(Vector, vector, "Ingresa un vector")
        validarCondicion(vector.getType() is not self.getType(), 
                         "Ingresa un vector con el mismo tipo de dato", TypeError)
        validarMayorQue(vector.getLongitud(), self.getLongitud(), True, 
                        "Ingrese un vector con la misma longitud o mayor que este vector", ImplosionError)
        
        for i in range(self.getLongitud()):
            vector[i] = self[i]

    #METODOS INTERNOS
    def __generarVector(self, longitud:int) -> list[T]:
        """Dada una longitud, retorna una lista de esa longitud unicamente con elementos None
        
        **parameters**
            -   **longitud** (int)

        **return**
            -   **list[None]** lista de elementos None con la longitud ingresada   
        """
        return [None]*longitud

    def __expandir(self) -> None:
        """Expande el vector"""
        self.__array.extend(self.__generarVector(self.__getLongitudOriginal()))

    def __contraer(self) -> None:
        """Contrae el vector"""
        for i in range(self.__getLongitudOriginal()):
            self.__array.pop()

    def __buscar(self, item:T) -> int:
        """Dado un item, lo busca en el vector mediante una busqueda lineal
        
        **parameters**
            -   item (T)

        **return**
            -   (int) indice del item si está en el vector, -1 si no
        """
        encontrado = False
        i = 0

        while not encontrado and (i <= self.__getPoscicionFinal()):
            if (self[i] == item):
                encontrado = True
            else:
                i+=1

        if not encontrado:
            return NO_ENCONTRADO
        else: return i

    #VALIDACIONES
    def __validarIndice(self, indice:int) -> None:
        """Valida que el indice se encuentre el rango del vector"""
        validarRango(indice, PRIMERA_POSCICION,self.__getPoscicionFinal(),
                     mensaje= f"Ingresa un valor entre {PRIMERA_POSCICION} y {self.__getPoscicionFinal()}")

    def __validarExpansionAutomatica(self) -> None:
        """Valida que el vector se pueda expandir automaticamente"""
        validarCondicion(self.getTipoExpansion() == TipoExpansion.AUTOMATICA,
                         "El vector está lleno y no se puede expandir" + (
                             " por su cuenta" if (self.esExpansible()) else ""), LlenoError)

    def __validarExpansionManual(self) -> None:
        """Valida que el vector tenga tipo de expansión manual"""
        validarCondicion(self.getTipoExpansion() != TipoExpansion.MANUAL,
                         "Este vector no tiene expansión manual", MetodoInvalidoError)

    def __validarNoVacio(self) -> None:
        """Valida que el vector no este vacío"""
        validarCondicion(self.estaVacio(), "El vector está vacío", VacioError)

    #ESTATICOS
    @staticmethod
    def crearConIterable(iterable:Iterable, tipoExpansion:TipoExpansion = TipoExpansion.DESACTIVADA) -> Vector[T]:
        """Dado un tipo de objeto iterable, crea un vector con los elementos en el objeto

        **parameters**
            -   iterable (Iterable): todos los elementos deben ser del mismo tipo de objeto
            -   tipoExpansion (TipoExpansion): DESACTIVADA (por defecto), AUTOMATICA o MANUAL

        **excepciones**
            -   **TypeError**: Si el tipod e los parameteros no es el indicado o si al menos un elemento del iterable tiene un tipo de objeto distinto
        """
        if not isinstance(iterable, Iterable): raise TypeError("Ingresa un tipo iterable")
        tipo = ValidarTipoUnico(iterable, "Ingresa una lista de elementos con tipo unico")

        vector = Vector(tipo, len(iterable), tipoExpansion)
        i = 0

        for item in iterable:
            vector[i] = item
            i+=1

        return vector

    #FLAGS
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

    def estaElItem(self, item) -> bool:
        """Verifica que un item se encuentre en el vector
        
        **parameters**
            -   item (T): puede ser None
        
        **return**
            -   (bool) Verdadero si el item ingresado se encuentra en el vector, falso si no
            
        **excepciones**
            -   **TypeError**: si el item ingresado no es None o del tipo ingresado T
        """
        self.__validarEntrada__(item, True)
        return self.__buscar(item) != NO_ENCONTRADO

    def esExpansible(self) -> bool:
        """Valida que el vector se pueda expandir al llenarse
        
        **return**
            -  (bool) Verdadero si el tipo de expansión del vector no es DESACTIVADA, falso si sí
        """
        return self.getTipoExpansion() != TipoExpansion.DESACTIVADA

    def expansionAutomatica(self) -> bool:
        """Verifica que el vector tenga expansión automatica
        
        **return**
            - (bool) Verdadero si el tipo de expansión del vector es AUTOMATICO, falso si no
        """
        return self.getTipoExpansion() == TipoExpansion.AUTOMATICA

    def estaExpandido(self) -> bool:
        return self.getLongitud() == self.__getLongitudOriginal()

    #FLAGS INTERNAS
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

    #GETTERS SIMPLES
    def getTipoExpansion(self) -> TipoExpansion:
        """Obtiene el tipo de Expansion
        
        **return**
            -   (TipoExpansion) AUTOMATICA, MANUAL, DESACTIVADA
        """
        return self.__tipoExpansion

    #GETTERS COMPLEJOS
    def getLongitud(self) -> int:
        """Obtiene la longitud del vector
        
        **return**
            -   (int) longitud del vector
        """
        return len(self)
    
    def getCantidadElementos(self) -> int:
        """Obtiene la cantidad de elementos en este vector
        
        **return**
            -   (int) cantidad de posciciones en el vector que no contienen un None
        """
        elementos = 0

        for item in self:
            if item is not None:
                elementos +=1
        
        return elementos

    def getIndice(self, item:T) -> int:
        """Dado un item en el vector, retorna el indice del vector
        
        **parameters**
            -   item (T): Debe encontrarse en el vector 

        **excepciones**
            -   **TypeError**: Si el item ingresado no es del tipo ingresado T
            -   **ElementoNoEncontrado**: Si el item no está en el vector
        """
        self.__validarEntrada__(item)
        indice = self.__buscar(item)

        validarValorCompatible(indice, NO_ENCONTRADO, "Este elemento no se encuentra en el vector", ElementoNoEncontrado)
        return indice

    #GETTERS SIMPLES INTERNOS
    def __getLongitudOriginal(self) -> int:
        """Obtiene la longitud original del vector antes de expandirse
        
        **return**
            -   (int) longitud ingresada por parametro
        """
        return self.__longitudOriginal

    #GETTERS COMPLEJOS INTERNOS
    def __getPoscicionFinal(self) -> int:
        """Obtiene el indice de la ultima poscicion
        
        **return**
            -   (int) longitud - 1
        """
        return self.getLongitud() - 1
    
    #SETTERS INTERNOS
    def __setTipoExpansion(self, tipoExpansion:TipoExpansion) -> None:
        """Setea el tipo de expansión del vector
        
        **parameters**
            -   tipoExpansion (TipoExpansion): DESACTIVADA, AUTOMATICA, MANUAL
        
        **excepciones**
            -   **TypeError**: Si el parametro ingresado no es un tipo de expansión
        """
        validarTipoObjeto(TipoExpansion, tipoExpansion, "Ingresa un tipo de Expansión valido")
        self.__tipoExpansion = tipoExpansion

    def __setLongitudOriginal(self, longitud:int) -> None:
        """Setea la longtitud del vector al momento de crearlo
        
        **parameters**
            -   longitud (int): mayor que cero

        **excepciones**
            -   **LongitudNegativaError** si la longitud ingresada es menor o igual a cero
        """
        validarNoNegativo(longitud,False, "Ingrese una longitud positiva", LongitudNegativaError)
        self.__longitudOriginal = longitud
        

#MATRIZ-----------------------------------------------------------------------------------------------------------------------------------------
class Matriz(Generic[T], TypeStruct):
    #ATRIBUTOS
    __array:list[list[T]]
    
    #CONSTRUCTORES
    def __init__(self, tipo:type, longitudColu:int, longitudFila:int) -> Matriz[T]:
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

        self.__array = []

        for i in range(longitudColu):
            self.__array.append([])
            for j in range(longitudFila):
                self.__array[i].append(None)

        super().__init__(tipo)

    #METODOS GENERALES
    def __str__(self) -> str:
        cadena = "\n"

        for fila in self.__array:
            fil = "< "
            for item in fila:
                fil += f"{item}, "

            cadena += fil[:-2] + " >\n"

        return cadena

    def __repr__(self) -> str:
        cadena = "["
        for fila in self.__array:
            cadena+= str(fila)
        return cadena
    
    def __len__(self) -> int:
        return self.getLongitudFila() * self.getLongitudColu()

    def __iter__(self) -> Generator[T]:
        for fila in self.__array:
            for item in fila:
                yield item

    #METODOS DE CLASE

    def agregar(self, elemento:T) -> None:
        """Agrega un elemento en la primera poscicion vacía en la matriz
        
        **parameters**
            -   elemento (T): no puede ser None

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es del tipo ingresado T
        """
        self.__validarEntrada__(elemento)
        self.__validarNoLleno()

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

    def agregarEnFila(self, indice:int, elemento:T) -> None:
        """Dado un elemento y un indice de fila, añade el elemento a la ultima poscición vacía de esa fila
        
        **parameters**
            -   indice (int): entre 0 y la longitud de las filas - 1
            -   elemento (T)
        
        **excepciones**
            -   **TypeError**: si ningun parametro ingresado es del tipo especificado
            -   **IndexError**: si el indice se sale del rango especificado
            -   **LlenoError**: si la fila está llena
        """
        self.__validarEntrada__(elemento)
        self.__validarFilaNoLlena(indice)

        i = PRIMERA_POSCICION
        agregado = False
        
        while not agregado and (i <= self.__getUltimaPosFila()):
            if self.getItem(indice,i) is None:
                agregado = True
                self.setItem(indice,i,elemento) 

    def agregarEnColumna(self, indice:int, elemento:T) -> None:
        """Dado un elemento y un indice de columna, añade el elemento a la ultima poscición vacía de esa columna
        
        **parameters**
            -   indice (int): entre 0 y la longitud de las columnas - 1
            -   elemento (T)
        
        **excepciones**
            -   **TypeError**: si ningun parametro ingresado es del tipo especificado
            -   **IndexError**: si el indice se sale del rango especificado
            -   **LlenoError**: si la columna está llena
        """
        self.__validarEntrada__(elemento)
        self.__validarColumnaNoLlena(indice)

        i = PRIMERA_POSCICION
        agregado = False
        
        while not agregado and (i <= self.__getUltimaPosColu()):
            if self.getItem(i,indice) is None:
                agregado = True
                self.setItem(i,indice,elemento) 

    def remover(self, indice:int, jndice:int) -> T:
        """Dado un indice columna y un indice fila, elimina el elemento en la poscición ingresada
                
        **parameters**
            -   indice (int): entre 0 y la longitud de las columnas - 1
            -   jndice (int): entre 0 y la longitud de las filas - 1
        
        **return**
            -   (T) elemento en la poscición ingresada
        
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
        self.__validarIndices(indice,jndice)

        elemento = self.getItem(indice,jndice)
        self.setItem(indice,jndice, None)

        return elemento

    def copiar(self) -> Matriz[T]:
        """Crea una copia exacta de la matriz
        
        **return**
            -   (Matriz[T]) Matriz con los mismo elementos y mismas dimensiones que la matriz original
        """
        matriz = Matriz(self.getType(),self.getLongitudColu(), self.getLongitudFila())
        
        for item in self:
            matriz.agregar(item)

        return matriz

    def expandirFilas(self, cantidad:int = 1, datoInicial:T = None) -> None:
        """Expande las filas de la matriz 

        **parameters**
            -   cantidad (int): por defecto 1. Si ingresa un valor (que debe ser positivo), se expandirá esa cantidad de veces 
            -   datoInicial (T): por defecto None. Si ingresa otro valor, entonces todos los espacios creados tendrán ese valor por defecto

        **excepciones**
            -   **TypeError**: si algun dato ingresado por parametro no pertenece al tipo especficado
            -   **ImplosionError**: si la cantidad ingresada es menor o igual que cero
        """
        self.__validarEntrada__(datoInicial,True)
        self.__validarExpansion(cantidad)

        for fila in self.__array:
            for i in range(cantidad):
                fila.append(datoInicial)

    def expandirColumnas(self, cantidad:int = 1, datoInicial:T = None) -> None:
        """Expande las columnas de la matriz 

        **parameters**
            -   cantidad (int): por defecto 1. Si ingresa un valor (que debe ser positivo), se expandirá esa cantidad de veces 
            -   datoInicial (T): por defecto None. Si ingresa otro valor, entonces todos los espacios creados tendrán ese valor por defecto

        **excepciones**
            -   **TypeError**: si algun dato ingresado por parametro no pertenece al tipo especficado
            -   **ImplosionError**: si la cantidad ingresada es menor o igual que cero
        """
        self.__validarEntrada__(datoInicial,True)
        self.__validarExpansion(cantidad)

        self.__array.append([datoInicial]*self.getLongitudFila())

    def expandirMatriz(self, expansionFila:int = 1, expansionColu:int = 1, datoInicial:T = None) -> None:
        """Expande las filas y las columnas de la matriz 

        **parameters**
            -   expansionFila (int): por defecto 1. Si ingresa un valor (que debe ser positivo), se expandirá esa cantidad de veces 
            -   expansionColu (int): por defecto 1. Si ingresa un valor (que debe ser positivo), se expandirá esa cantidad de veces 
            -   datoInicial (T): por defecto None. Si ingresa otro valor, entonces todos los espacios creados tendrán ese valor por defecto

        **excepciones**
            -   **TypeError**: si algun dato ingresado por parametro no pertenece al tipo especficado
            -   **ImplosionError**: si la cantidad ingresada es menor o igual que cero
        """
        self.expandirColumnas(expansionColu, datoInicial)
        self.expandirFilas(expansionFila, datoInicial)

    def eliminarFila(self, indice:int) -> Vector[T]:
        """Dado un indice fila, elimina la fila en esa poscición y retorna un Vector con esos datos
        
        **parameters**
            -   indice (int): entre 0 y la longitud de las columnas - 1
        
        **return**
            -   (Vector[T]) Vector con los datos de la fila eliminada
            
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
        self.__validarIndiceFila(indice)
        return Vector.crearConIterable(self.__array.pop(indice))


    def eliminarColumna(self, indice:int) -> Vector[T]:
        """Dado un indice columna, elimina la columna en esa poscición y retorna un Vector con esos datos
        
        **parameters**
            -   indice (int): entre 0 y la longitud de las filas - 1
        
        **return**
            -   (Vector[T]) Vector con los datos de la columna eliminada
            
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
        columnaEliminada = Vector(self.getType(), self.getLongitudColu())

        for i in range(self.getLongitudColu()):
            columnaEliminada[i] = self.__array[i].pop(indice)

        return columnaEliminada

    def contraerMatriz(self, indice:int, jndice:int) -> None:
        """Dado un indice columna y un indice columna, elimina esa matriz y esa columna
        
        **parameters**
            -   indice (int): entre 0 y la longitud de las filas - 1
            
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
        self.eliminarColumna(indice)
        self.eliminarFila(jndice)

    #METODOS INTERNOS
    def __buscar(self, item:T) -> tuple[int, int]:
        """Dado un item, lo busca y retorna los indices fila y columna.

        **parameters**
            -   item (T)

        **return**
            -   (int) indice columna
            -   (int) indice fila 
        """
        i = PRIMERA_POSCICION
        j:int
        encontrado = False

        while not encontrado and (i <= self.__getUltimaPosColu()):
            j = PRIMERA_POSCICION
            while not encontrado and (i <= self.__getUltimaPosFila()):
                if (item == self.getItem(i,j)):
                    encontrado = True
                else:
                    j+=1
            if not encontrado: i+=1

        if encontrado: return i,j
        else: return NO_ENCONTRADO, NO_ENCONTRADO
        
    #VALIDACIONES
    def __validarIndiceFila(self, indice:int) -> None:
        """Valida que un indice ingresado, pueda ser un indice fila
        
        **parameters**
            -   indice (int): entre 0 y la longitud de las columnas - 1
        
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
        validarTipoObjeto(int, indice, "Ingresa un indice int")
        validarRango(indice,PRIMERA_POSCICION,self.__getUltimaPosFila(),
                     mensaje= f"Ingresa un poscicion entre {PRIMERA_POSCICION} y {self.__getUltimaPosFila()}")

    def __validarIndiceColu(self, indice:int) -> None:
        """Valida que un indice ingresado, pueda ser un indice columna
        
        **parameters**
            -   indice (int): entre 0 y la longitud de las filas - 1
        
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
        validarRango(indice,PRIMERA_POSCICION,self.__getUltimaPosColu(),
                     mensaje= f"Ingresa un poscicion entre {PRIMERA_POSCICION} y {self.__getUltimaPosColu()}")
        
    def __validarIndices(self, indice:int, jndice:int) -> None:
        """Valida que dos indice ingresados, puedan ser un indices columna y fila validos (en ese orden)
        
        **parameters**
            -   indice (int): entre 0 y la longitud de las columnas - 1
            -   jndice (int): entre 0 y la longitud de las filas - 1
        
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
        self.__validarIndiceColu(indice)
        self.__validarIndiceFila(jndice)

    def __validarNoLleno(self) -> None:
        """Valida que la matriz no este llena
        
        **excepciones**
            -   **LlenoError**: si la matriz está llena
        """
        validarCondicion(self.estaLleno(),"La matriz está llena", LlenoError)

    def __validarFilaNoLlena(self,indice) -> None:
        """Valida que una fila no esté llena

        **parameters**
            -   indice (int): entre 0 y la longitud de las filas - 1
        
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
            -   **LlenoError**: si la fila está llena
        """
        self.__validarIndiceColu(indice)
        validarCondicion(self.filaLlena(indice),f"La fila {indice} está llena", LlenoError)
        
    def __validarColumnaNoLlena(self,indice) -> None:
        """Valida que una columna no esté llena
        
        **parameters**
            -   indice (int): entre 0 y la longitud de las columnas - 1
        
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
            -   **LlenoError**: si la columna está llena
        """
        self.__validarIndiceFila(indice)
        validarCondicion(self.columnaLlena(indice),f"La fila {indice} está llena", LlenoError)
        
    def __validarExpansion(self, cantidad:int) -> None:        
        """Dado una cantidad y un dato inicial, valida que la expansión se lleve a cabo
        
        **parameters**
            -   cantidad (int): positiva

        **excepciones**
            -   **TypeError**: si la cantidad ingresada por parametro no es un int
            -   **ImplosionError**: si la cantidad ingresada es menor o igual que cero
        """
        validarTipoObjeto(int, cantidad, "Ingresa una cantidad int")
        validarNoNegativo(cantidad, False, "Ingresa una cantidad positiva para la expancion", ImplosionError)

    #FLAGS    
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
        """Verfiida que una fila esté llena

        **parameters**
            -   indice (int): entre 0 y la longitud de las columnas - 1
        
        **return**
            -   (bool) Verdadero si ningun elemento de la fila es None, falso si al menos uno lo es
            
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
        self.__validarIndiceColu(indice)
        i = PRIMERA_POSCICION
        llena = True

        while llena and (i < self.getLongitudFila()):
            llena = self.getItem(indice, i) is not None
            i+=1

        return llena
    
    def columnaLlena(self, indice:int) -> bool:
        """Verfiida que una columna esté llena

        **parameters**
            -   indice (int): entre 0 y la longitud de las filas - 1
        
        **return**
            -   (bool) Verdadero si ningun elemento de la columna es None, falso si al menos uno lo es
            
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
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
        """Verfiida que una fila esté vacía

        **parameters**
            -   indice (int): entre 0 y la longitud de las columnas - 1
        
        **return**
            -   (bool) Verdadero si todos los elementos de la fila son None, falso si al menos uno no lo es
            
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
        self.__validarIndiceColu(indice)
        i = self.__getUltimaPosFila()
        vacia = True

        while vacia and (i >= PRIMERA_POSCICION):
            vacia = self.getItem(indice, i) is None
            i-=1

        return vacia
    
    def columnaVacia(self, indice:int) -> bool:
        """Verfiida que una columna esté vacía

        **parameters**
            -   indice (int): entre 0 y la longitud de las filas - 1
        
        **return**
            -   (bool) Verdadero si todos los elementos de la columna son None, falso si al menos uno no lo es
            
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
        self.__validarIndiceFila(indice)
        i = self.__getUltimaPosColu()
        vacia = True

        while vacia and (i >= PRIMERA_POSCICION):
            vacia = self.getItem(i, indice) is None
            i-=1

        return vacia
            

    def esCuadrada(self) -> bool:
        """Verifica que la matriz sea cuadrada
        
        **return**
            -   (bool) Verdadero si las filas y las longitudes miden exactamente lo mismo, falso si no
        """
        return self.getLongitudFila() == self.getLongitudColu()
    
    def esSimetrica(self) -> bool:
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

    def estaElItem(self, item:T) -> bool:
        """Verifica que el item se encuentre en la matriz
        
        **parameters**
            -   item (T): puede ser None

        **return**
            -   (bool) Verdadero si está en la matriz, falso si no

        **excepciones**
            -   **TypeError**: Si el item no es del tipo ingresado T
        """
        self.__validarEntrada__(item, True)
        i,j = self.__buscar(item)
        return i != NO_ENCONTRADO

    #GETTERS COMPLEJOS
    def getCantidadElementos(self) -> int:
        """Obtiene la cantidad de elementos almacenados en la matriz
        
        **return**
            -   (int) cantidad de elementos distintos de None en la matriz
        """
        elementos = 0

        for item in self:
            if item is not None:
                elementos+=1

        return elementos
    
    def getFila(self, indice:int) -> Vector[T]:
        """Dado un indice, retorna la fila en esa poscición

        **parameters**
            -   indice (int): entre 0 y la longitud de las filas - 1
        
        **return**
            -   (Vector[T]) vector con los elementos de esa fila
            
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
        self.__validarIndiceColu(indice)
        
        return Vector.crearConIterable(self.__array[indice])

    def getColumna(self, indice:int) -> Vector[T]:
        """Dado un indice, retorna la columna en esa poscición
        
        **parameters**
            -   indice (int): entre 0 y la longitud de las columnas - 1
        
        **return**
            -   (Vector[T]) vector con los elementos de esa columna
            
        **excepciones**
            -   **TypeError**: si el indice ingresado no es un int
            -   **IndexError**: si el indice se sale del rango especificado
        """
        self.__validarIndiceFila(indice)
        vector = Vector(self.getType(),self.getLongitudColu())

        for i in range(self.getLongitudColu()):
            vector[i] = self.__array[i][indice]

        return vector

    def getLongitudFila(self) -> int:
        """Obtiene la longitud de las filas
        
        **return**
            -   (int) dimension fila
        """
        return len(self.__array[PRIMERA_POSCICION])

    def getLongitudColu(self) -> int:
        """Obtiene la longitud de las columnas
        
        **return**
            -   (int) dimensión columna   
        """
        return len(self.__array)

    def getItem(self, indice:int, jndice:int) -> T:
        """Dado dos indices, obtiene el valor en esa poscición
        
        **parameters**
            -   indice (int): entre 0 y la longitud de las columnas - 1
            -   jndice (int): entre 0 y la longitud de las filas - 1
        
        **excepciones**
            -   **TypeError**: si los indices ingresados no son int
            -   **IndexError**: si los indices se salen del rango especificado
        """
        self.__validarIndices(indice, jndice)
        return self.__array[indice][jndice]

    def getIndices(self, item:T) -> tuple[int, int]:
        """Dado un item de la matriz, retorna sus indices
        
        **parameters**
            -   item (T): Pertence a la matriz

        **return**
            -   (int) inidce fila
            -   (int) indice columna

        **excepciones**
            -   **TypeError**: Si el item ingresado no es del tipo ingresado T
            -   **ElementoNoEncontrado**: Si el elemento no se encuentra en la matriz
        """
        self.__validarEntrada__(item, True)
        i, j = self.__buscar(item)

        validarValorCompatible(i, NO_ENCONTRADO, "Este item no se encuentrá en la matriz", ElementoNoEncontrado)
        return i,j

    def getIndiceFila(self, item:T) -> int:
        """Dado un item, retorna el indice fila

        **parameters**
            -   item (T): Pertence a la matriz

        **return**
            -   (int) inidce fila

        **excepciones**
            -   **TypeError**: Si el item ingresado no es del tipo ingresado T
            -   **ElementoNoEncontrado**: Si el elemento no se encuentra en la matriz
        """
        self.__validarEntrada__(item, True)
        i,j = self.__buscar(item)
        validarValorCompatible(i, NO_ENCONTRADO, "Este item no se encuentrá en la matriz", ElementoNoEncontrado)
        return i
        
    def getIndiceColumna(self, item:T) -> int:
        """Dado un item, retorna el indice columna

        **parameters**
            -   item (T): Pertence a la matriz

        **return**
            -   (int) inidce columna

        **excepciones**
            -   **TypeError**: Si el item ingresado no es del tipo ingresado T
            -   **ElementoNoEncontrado**: Si el elemento no se encuentra en la matriz
        """
        self.__validarEntrada__(item, True)
        i,j = self.__buscar(item)
        validarValorCompatible(j, NO_ENCONTRADO, "Este item no se encuentrá en la matriz", ElementoNoEncontrado)
        return j
        
    def getCantidadEspacios(self) -> int:
        """Obtiene la cantidad de espacios totales en la matriz
        
        **return**
            -   (int) longitud filas x longitud columnas
        """
        return self.getLongitudColu()*self.getIndiceFila()

    #GETTERS COMPLEJOS INTERNOS
    def __getUltimaPosFila(self) -> int:
        """Obtiene la ultima poscición de la fila
        
        **return**
            -   (int) longitud fila - 1
        """
        return self.getLongitudFila() -1

    def __getUltimaPosColu(self) -> int:
        """Obtiene la ultima poscición de la colu
        
        **return**
            -   (int) longitud colu - 1
        """
        return self.getLongitudColu() -1

    #SETTERS COMPLEJOS
    def setItem(self, indice:int, jndice:int, elemento:T) -> None:
        """Dado dos indices y un elemento, setea el valor en esa poscición
        
        **parameters**
            -   indice (int): entre 0 y la longitud de las columnas - 1
            -   jndice (int): entre 0 y la longitud de las filas - 1
            -   elemento (T): puede ser None

        **excepciones**
            -   **TypeError**: si los indices ingresados no son int o el elemento no es del tipo ingresado T o None
            -   **IndexError**: si los indices se salen del rango especificado
        """
        self.__validarIndices(indice,jndice)
        self.__validarEntrada__(elemento, True)
        self.__array[indice][jndice] = elemento

