from .Validaciones import DataStruct, TypeStruct, Generic, T, validarTipoObjeto, validarCondicion
from .Vector import Vector
from .Excepciones.Generales import *
from .Excepciones.LinkedList import *

MAXIMO_CURSORES = 3

#NODO -------------------------------------------------------------------------------------------------------------
class Nodo(DataStruct, Generic[T]):
    #ATRIBUTOS
    __anterior:Nodo[T]
    __siguiente:Nodo[T]

    #CONSTRUCTOR
    def __init__(self, tipo:type, dato:T):
        """Dado un tipo de dato y un dato, crea un nodo de lista
        
        **parameters**
            -   tipo (type)
            -   dato (T): del tipo ingresado previamente
        
        **excepciones**
            -   **TypeError**: si algun dato ingresado por parametro no coincide con el resto
        """
        super().__init__(tipo, dato, False)
        self.setAnterior(None)
        self.setSiguiente(None)

    #METODOS GENERALES
    def __str__(self):
        cadena = ""

        if self.getAnterior() is not None:
            cadena+= f"[{self.getAnterior().getDato()}] - "

        cadena+= "{"+f"{self.getDato()}"+"}"

        if self.getSiguiente() is not None:
            cadena+= f" - [{self.getSiguiente().getDato()}]"

        return cadena
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, value:Nodo):
        if type(value) is not Nodo: return False
        return self.getDato() == value.getDato()

    #VALIDACIONES
    def __validarConexion(self, nodo:Nodo[T]):
        """Valida la coneccion con otro Nodo
        
        **parameters**
            -   nodo (Nodo[T]): puede ser None. Mismo tipo de dato que este nodo
        
        **excepciones**
            -   **TypeError**: si el parametro ingresado no es un Nodo
            -   **NodoInvalidoError**: si el nodo ingresado no tiene el mismo tipo de dato que este nodo
        """
        if nodo is not None:
            validarTipoObjeto(Nodo,nodo,"Ingrese un nodo")
            validarCondicion(self.getType() is not nodo.getType(), 
                         "Ingresa un nodo con el mismo tipo de dato", NodoInvalidoError)

    @staticmethod
    def validarConeccion(nodo1:Nodo[T], nodo2:Nodo[T]):
        """Valida que dos nodos se puedan Conectar
        
        **parameters**
            -   nodo1 (Nodo[T]): puede ser None
            -   nodo2 (Nodo[T]): puede ser None

        **excepciones**
            -   **TypeError** si los parametros ingresados no son Nodos
            -   **NodoInvalidoError** si los nodos no almacenan el mismo tipo de dato
        """
        if nodo1 is not None:
            validarTipoObjeto(Nodo, nodo1, "Ingresa un nodo")
        if nodo2 is not None:
            validarTipoObjeto(Nodo, nodo2, "Ingresa un nodo")
        if None not in (nodo1, nodo2):
            validarCondicion(nodo1.getType() is not nodo2.getType(),
                             "Ingresa dos nodos con el mismo tipo de dato", NodoInvalidoError)

    #METODO ESTATICOS
    @staticmethod
    def conectarNodos(nodoAnterior:Nodo[T], nodoSiguiente:Nodo[T]):
        """Dado dos nodos, los conecta
        
        **parameters**
            -   nodoAnterior (Nodo[T]): puede ser None
            -   nodoSiguiente (Nodo[T]): puede ser None

        **excepciones**
            -   **TypeError** si los parametros ingresados no son Nodos
            -   **NodoInvalidoError** si los nodos no almacenan el mismo tipo de dato
        """
        Nodo.validarConeccion(nodoAnterior, nodoSiguiente)

        if nodoAnterior is not None:
            nodoAnterior.setSiguiente(nodoSiguiente)
        if nodoSiguiente is not None:
            nodoSiguiente.setAnterior(nodoAnterior)

    @staticmethod
    def desconectarNodo(nodo:Nodo[T]):
        """Desconecta un nodo ingresado
        
        **parameters**
            -   nodo (Nodo[T])
        
        **excepciones**
            -   **TypeError** si el nodo ingresado no es un nodo
        """
        validarTipoObjeto(Nodo, nodo, "Ingrese un nodo")

        nodo.setSiguiente(None)
        nodo.setAnterior(None)

    #GETTERS
    def getAnterior(self) -> Nodo[T]:
        """Obtiene el nodo anterior en la lista

        **return**
            -   (Nodo[T]) nodo previo
        """
        return self.__anterior
    
    def getSiguiente(self) -> Nodo[T]:
        """Obtiene el nodo siguiente en la lista

        **return**
            -   (Nodo[T]) nodo proximo
        """
        return self.__siguiente
    
    #SETTERS
    def setAnterior(self, anterior:Nodo[T]):
        """Setea un nodo como el anterior

        **parameters**
            -   anterior (Nodo[T])

        **excepciones**
            -   **TypeError**: si el parametro ingresado no es un Nodo
            -   **NodoInvalidoError**: si el nodo ingresado no tiene el mismo tipo de dato que este nodo
        """
        self.__validarConexion(anterior)
        self.__anterior = anterior

    def setSiguiente(self, siguiente:Nodo[T]):
        """Setea un nodo como el siguiente

        **parameters**
            -   anterior (Nodo[T])

        **excepciones**
            -   **TypeError**: si el parametro ingresado no es un Nodo
            -   **NodoInvalidoError**: si el nodo ingresado no tiene el mismo tipo de dato que este nodo
        """
        self.__validarConexion(siguiente)
        self.__siguiente = siguiente

    def setDato(self, dato:T):
        """Seta el dato del nodo
        
        **parameters**
            -   dato (T)
        
        **excepciones**
            -   **TypeError**: si el dato ingresado no corresponde con el tipo ingresado
        """
        return super().setDato(dato)

#CURSOR ------------------------------------------------------------------------------------------------------------
class Cursor(TypeStruct,Generic[T]):
    #ATRIBUTOS
    __nodo:Nodo[T]

    #CONSTRUCTORES
    def __init__(self, tipo:type):
        """Crea un cursor para una lista
        
        **parameters**
            -   **tipo** (type)

        **excepciones**
            -   **TypeError**: si el tipo ingresado no es un type
        """
        super().__init__(tipo)
        self.setNodo(None)

    #METODOS GENERALES
    def estaPrendido(self) -> bool:
        """Verifica que el nodo esté prendido
        
        **return**
            -   (bool) Verdadero si el nodo no es None, falso si es None
        """
        return self.getNodo() is not None

    def activarCursor(self, nodo:Nodo[T]):
        """Dado un nodo, activa el cursor y lo pone hasta esa poscicion
        
        **parameters**
            -   nodo (Nodo[T])

        **excepciones**
            -   **TypeError** si el parametro ingresado no es un None   
            -   **ErrorCursorEncendido** si el cursor no está apagado
            -   **NodoInvalidoError** si el nodo ingresado es None
        """        
        validarTipoObjeto(Nodo, nodo, "Ingresa un Nodo")
        self.validarCursorApagado()
        validarCondicion(nodo is None, "Ingresa un nodo no None para inicar el cursor", NodoInvalidoError)
        
        self.setNodo(nodo)

    def desactivarCursor(self):
        """Apaga el cursor
        
        **excepciones**
            -   **ErrorCursorDesactivado** si el cursor no está prendido
        """
        self.validarCursorPrendido()
        self.setNodo(None)

    def avanzarNodo(self):
        """Mueve el cursor hacia el siguiente nodo. Si es el ultimo nodo de la lista, el cursor se apaga automaticamente
        
        **excepciones**
            -   **ErrorCursorDesactivado**: si el cursor esta apagado
        """
        self.validarCursorPrendido()
        self.setNodo(self.getNodo().getSiguiente())
        
    def retrocederNodo(self):
        """Mueve el cursor hacia el anterior nodo. Si es el primer nodo de la lista, el cursor se apaga automaticamente
        
        **excepciones**
            -   **ErrorCursorDesactivado**: si el cursor esta apagado
        """
        self.validarCursorPrendido()
        self.setNodo()

    def insertar(self, dato:T):
        """Dado un dato, inserta un nodo con ese dato entre dos nodos
        
        **parameters**
            -   dato (T)
        
        **excepciones**
            -   **ErrorCursorDesactivado**: si el cursor esta apagado
            -   **TypeError**: si el dato ingresado no pertenece al tipo ingresado T
            
        """
        self.validarCursorPrendido()

        nodo = Nodo(dato)

        Nodo.conectarNodos(self.getNodo().getAnterior(), nodo)
        Nodo.conectarNodos(nodo, self.getNodo())

        self.setNodo(nodo)

    def extirpar(self) -> T:
        """Quita un nodo de entre dos nodo, se posiciona en el siguiente y retorna el dato quitado
        
        **return**
            -   (T) dato almacenado en el nodo extirpado

        **excepciones**
            -   **ErrorCursorDesactivado**: si el cursor esta apagado
        """

        nodo = self.getNodo()

        Nodo.conectarNodos(nodo.getAnterior(), nodo.getSiguiente())
        
        if nodo.getSiguiente() is None:
            self.avanzarNodo()
        else:
            self.retrocederNodo()

        Nodo.desconectarNodo(nodo)

        return nodo.getDato()
        

    #VALIDACIONES
    def validarCursorPrendido(self):
        """Valida que el cursor esté prendido
        
        **excepciones**
            -   **ErrorCursorDesactivado** si el cursor no está prendido
        """
        validarCondicion(not self.estaPrendido(), "El cursor no está encendido", ErrorCursorDesactivado)

    def validarCursorApagado(self):
        """Valida que el cursor esté apagado
        
        **excepciones**
            -   **ErrorCursorEncendido** si el cursor no está apagado
        """
        validarCondicion(self.estaPrendido(),
                         "Para ejecutar está accion, el cursor debe estár apagado", ErrorCursorEncendido)
    
    #GETTERS

    #Calculables
    def getDatoCursor(self) -> T:
        """Retorna el dato almacenado en el nodo sobre el cual esta parado el cursor

        **return**
            -   (T): dato almacenado en el cursor
    
        **excepciones**
            -   **ErrorCursorDesactivado** si el cursor no está prendido
        """
        self.validarCursorPrendido()
        return self.getNodo().getDato()

    #Atributos
    def getNodo(self) -> Nodo[T] | None:
        """Retorna el nodo ingresado en el cursor
        
        **return**
            -   (Nodo[T]) nodo sobre el cual el nodo está poscicionado. Puede ser None
        """
        return self.__nodo

    #SETTERS
    def setDatoCursor(self, dato:T):
        self.validarCursorPrendido()
        self.getNodo().setDato(dato)

    def setNodo(self, nodo:Nodo[T]):
        """Setea el cursor sobre un nodo ingresado
        
        **parameters**
            -   nodo (Nodo[T]): puede ser None
        
        **excepciones**
            -   **TypeError** si el parametro ingresado no es un None
        """
        if (nodo is not None):
            validarTipoObjeto(Nodo, nodo, "Ingrese un nodo")
        
        self.__nodo = nodo

#LISTA ---------------------------------------------------------------------------------------------------------------------
class Lista(TypeStruct, Generic[T]):
    #ATRIBUTOS
    __primerNodo:Nodo[T]
    __ultimoNodo:Nodo[T]
    __longitud:int
    __cursores:Vector[Cursor[T]]

    #CONSTRUCTOR
    def __init__(self, tipo):
        """Dado un tipo de objeto, crea una lista que soporta ese tipo de objetos
        
        **parameters**
            -   tipo (type)
        
        **excepciones**
            -   **TypeError**: si el tipo ingresado no es un type
        """
        super().__init__(tipo)
        self.__setPrimero(None)
        self.__setUltimo(None)
        self.__iniciarCuenta()
        self.__generarCursores()
        

    #METODOS GENERALES
    def __str__(self):
        if self.estaVacia():
            return "{"+"}"
        else:    
            cursor = Cursor(self.getType())
            cadena = "{"
            cursor.activarCursor(self.__getPrimero())

            while cursor.estaPrendido():
                cadena += f"[{cursor.getDatoCursor()}]-"
                cursor.avanzarNodo()   

            return cadena[:-1] + "}"

    #METODOS DE CLASE
    def estaVacia(self) -> bool:
        """Verifica que la lista este vacia
        
        **return**
            -   (bool) Verdadero si la lista tiene 0 objetos, falso si tiene mas
        """
        return self.getLongitud() == 0

    def agregarInicio(self, elemento:T):
        """Agrega un elemento al inicio de la lista
        
        **parameters**
            -   elemento (T)

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es del tipo ingresado T
        """
        self.__validarEntrada__(elemento)    
        nodo = Nodo(self.getType(), elemento)

        if self.estaVacia():
            self.__setUltimo(nodo)
        else:
            Nodo.conectarNodos(nodo, self.__getPrimero())
            
        self.__setPrimero(nodo)
        self.__sumarObjeto()

    def quitarInicio(self) -> T:
        """Quita el primer elemento de la lista
        
        **return**
            -   (T) primer elemento de la lista

        **excepciones**
            -   **VacioError**: si la lista está vacia
        """
        self.__validarListaNoVacia()
        nodo = self.__getPrimero()

        self.__setPrimero(self.__getPrimero().getSiguiente())
        Nodo.conectarNodos(None, self.__getPrimero())
        Nodo.desconectarNodo(nodo)

        return nodo.getDato()

    def agregarFinal(self, elemento:T):
        """Agrega un elemento al final de la lista
        
        **parameters**
            -   elemento (T)

        **excepciones**
            -   **TypeError**: si el elemento ingresado no es del tipo ingresado T
        """
        self.__validarEntrada__(elemento)    
        nodo = Nodo(self.getType(), elemento)

        if self.estaVacia():
            self.__setPrimero(nodo)
        else:
            Nodo.conectarNodos(self.__getUltimo(),nodo)
            
        self.__setUltimo(nodo)
        self.__sumarObjeto()

    def quitarFinal(self) -> T:
        """Quita el ultimo elemento de la lista
        
        **return**
            -   (T) ultimo elemento de la lista

        **excepciones**
            -   **VacioError**: si la lista está vacia
        """
        self.__validarListaNoVacia()
        nodo = self.__getUltimo()

        self.__setUltimo(self.__getUltimo().getAnterior())
        Nodo.conectarNodos(self.__getUltimo(), None)
        Nodo.desconectarNodo(nodo)

        return nodo.getDato()


    #METODOS INTERNOS
    def __iniciarCuenta(self):
        """Inicia el conteo de objetos en la lista"""
        self.__longitud = 0

    def __sumarObjeto(self):
        """Suma uno al conteo de objetos en la lista"""
        self.__longitud += 1
    
    def __restarObjeto(self):
        """Resta uno al conteo de objetos en la lista"""
        self.__longitud -= 1

    #VALIDACIONES
    def __validarListaNoVacia(self):
        """Valida que la lista no esté vacia

        **excepciones**
            -   **VacioError**: si la lista está vacia
        """
        validarCondicion(self.estaVacia(), "La lista está vacia", VacioError)
    #MANEJO CURSORES
    def __generarCursores(self) -> Vector[Cursor[T]]:
        """Generea un vector de cursores permitidos para hacer
        
        **return**
            -   (Vector[Cursor[T]]): longitud 3
        """
        vectorCursores = Vector(Cursor, MAXIMO_CURSORES)

        for i in range(MAXIMO_CURSORES):
            vectorCursores[i] = Cursor(self.getType())

        self.__cursores = vectorCursores

    #GETTERS
    def __getPrimero(self) -> Nodo[T]:
        """Retorna el primer nodo de la lista
        
        **return**
            -   (Nodo[T]) nodo inicial
        """
        return self.__primerNodo
    
    def __getUltimo(self) -> Nodo[T]:
        """Retorna el primer nodo de la lista
        
        **return**
            -   (Nodo[T]) nodo inicial
        """
        return self.__ultimoNodo
    

    def getLongitud(self) -> int:
        """Retorna la longitud de la lista"""
        return self.__longitud
    
    #SETTERS
    
    def __setPrimero(self, nodo:Nodo[T]):
        """Setea al primer nodo de la lista
        
        **parameters**
            -   nodo (Nodo[T]): nodo inicial
        """
        self.__primerNodo = nodo
    
    def __setUltimo(self, nodo:Nodo[T]):
        """Setea al ultimo nodo de la lista
        
        **parameters**
            -   nodo (Nodo[T]): nodo final
        """
        self.__ultimoNodo = nodo
    
