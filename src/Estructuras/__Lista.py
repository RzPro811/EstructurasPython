from .__Validaciones import  T, validarTipoObjeto, validarCondicion, validarRango, PRIMERA_POSCICION, NO_ENCONTRADO, validarNoNegativo, ValidarTipoUnico
from .__Heredables import DataStruct, TypeStruct, Generic
from .__Vector import Vector
from .__Excepciones.Generales import *
from .__Excepciones.LinkedList import *

MAXIMO_CURSORES = 3

#NODO -------------------------------------------------------------------------------------------------------------
class Nodo(DataStruct, Generic[T]):
    #ATRIBUTOS
    __anterior:Nodo[T]
    __siguiente:Nodo[T]

    #CONSTRUCTOR
    def __init__(self, tipo:type, dato:T) -> Nodo[T]:
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
    def __str__(self) -> str:
        cadena = ""

        if self.getAnterior() is not None:
            cadena+= f"[{self.getAnterior().getDato()}] - "

        cadena+= "{"+f"{self.getDato()}"+"}"

        if self.getSiguiente() is not None:
            cadena+= f" - [{self.getSiguiente().getDato()}]"

        return cadena
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, value:Nodo) -> bool:
        if type(value) is not Nodo: return False
        return self.getDato() == value.getDato()

    #METODOS DE CLASE
    def desconectarNodo(self) -> None:
        """Desconecta el nodo"""
        validarTipoObjeto(Nodo, self, "Ingrese un nodo")

        self.setSiguiente(None)
        self.setAnterior(None)

    #VALIDACIONES
    def __validarConexion(self, nodo:Nodo[T]) -> None:
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
    def validarConeccion(nodo1:Nodo[T], nodo2:Nodo[T]) -> None:
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
    def conectarNodos(nodoAnterior:Nodo[T], nodoSiguiente:Nodo[T]) -> None:
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
    def setAnterior(self, anterior:Nodo[T]) -> None:
        """Setea un nodo como el anterior

        **parameters**
            -   anterior (Nodo[T])

        **excepciones**
            -   **TypeError**: si el parametro ingresado no es un Nodo
            -   **NodoInvalidoError**: si el nodo ingresado no tiene el mismo tipo de dato que este nodo
        """
        self.__validarConexion(anterior)
        self.__anterior = anterior

    def setSiguiente(self, siguiente:Nodo[T]) -> None:
        """Setea un nodo como el siguiente

        **parameters**
            -   anterior (Nodo[T])

        **excepciones**
            -   **TypeError**: si el parametro ingresado no es un Nodo
            -   **NodoInvalidoError**: si el nodo ingresado no tiene el mismo tipo de dato que este nodo
        """
        self.__validarConexion(siguiente)
        self.__siguiente = siguiente

    def setDato(self, dato:T) -> None:
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
    __poscicion:int

    #CONSTRUCTORES
    def __init__(self, tipo:type) -> Cursor[T]:
        """Crea un cursor para una lista
        
        **parameters**
            -   **tipo** (type)

        **excepciones**
            -   **TypeError**: si el tipo ingresado no es un type
        """
        super().__init__(tipo)
        self.setNodo(None)

    #METODOS DE CLASE
    def activarCursor(self, nodo:Nodo[T], poscicionInicial:int) -> None:
        """Dado un nodo, activa el cursor y lo pone hasta esa poscicion
        
        **parameters**
            -   nodo (Nodo[T])
            -   posciciónInicial (int): positiva o cero

        **excepciones**
            -   **TypeError**: si los parametros ingresados no cumplen con los tipos establecidos   
            -   **ErrorCursorEncendido**: si el cursor no está apagado
            -   **NodoInvalidoError**: si el nodo ingresado es None
            -   **IndexError**: si la poscición ingresada es negativa
        """        
        validarTipoObjeto(Nodo, nodo, "Ingresa un Nodo")
        self.validarCursorApagado()
        validarCondicion(nodo is None, "Ingresa un nodo no None para inicar el cursor", NodoInvalidoError)
        
        self.setNodo(nodo)
        self.setPoscicion(poscicionInicial)

    def desactivarCursor(self) -> None:
        """Apaga el cursor
        
        **excepciones**
            -   **ErrorCursorDesactivado** si el cursor no está prendido
        """
        self.validarCursorPrendido()
        self.setNodo(None)
        self.__apagar()

    def avanzarNodo(self) -> None:
        """Mueve el cursor hacia el siguiente nodo. Si es el ultimo nodo de la lista, el cursor se apaga automaticamente
        
        **excepciones**
            -   **ErrorCursorDesactivado**: si el cursor esta apagado
        """
        self.validarCursorPrendido()
        self.setNodo(self.getNodo().getSiguiente())
        self.__avanzar()
        
    def retrocederNodo(self) -> None:
        """Mueve el cursor hacia el anterior nodo. Si es el primer nodo de la lista, el cursor se apaga automaticamente
        
        **excepciones**
            -   **ErrorCursorDesactivado**: si el cursor esta apagado
        """
        self.validarCursorPrendido()
        self.setNodo(self.getNodo().getAnterior())
        self.__retroceder()

    def insertar(self, dato:T) -> None:
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
            self.retrocederNodo()
            self.__retroceder()
        else:
            self.avanzarNodo()

        nodo.desconectarNodo()

        return nodo.getDato()

    #METODOS INTERNOS
    def __avanzar(self) -> None:
        """Suma 1 a la poscición del cursor"""
        self.__poscicion += 1

    def __retroceder(self) -> None:
        """Resta 1 a la posición del cursor"""
        self.__poscicion -= 1

    def __apagar(self) -> None:
        """Quita la poscición cuando se apaga el cursor"""
        self.__poscicion = None

    #VALIDACIONES
    def validarCursorPrendido(self) -> None:
        """Valida que el cursor esté prendido
        
        **excepciones**
            -   **ErrorCursorDesactivado** si el cursor no está prendido
        """
        validarCondicion(not self.estaPrendido(), "El cursor no está encendido", ErrorCursorDesactivado)

    def validarCursorApagado(self) -> None:
        """Valida que el cursor esté apagado
        
        **excepciones**
            -   **ErrorCursorEncendido** si el cursor no está apagado
        """
        validarCondicion(self.estaPrendido(),
                         "Para ejecutar está accion, el cursor debe estár apagado", ErrorCursorEncendido)

    #VALIDACIONES INTERNAS
    def __validarPoscicion(self, indice:int) -> None:
        """Dado un indice, valida que sea correcto
        
        **parameters**
            -   indice (int): Mayor o igual que cero

        **excepciones**
            -   **TypeError**: Si el parametro ingresado no es int
            -   **IndexError**: Si el indice ingresado es negativo
        """
        validarTipoObjeto(int, indice, "Ingresa un indice int")
        validarNoNegativo(indice, True, "Ingresa una poscición no negativa", IndexError)

    #FLAGS
    def estaPrendido(self) -> bool:
        """Verifica que el nodo esté prendido
        
        **return**
            -   (bool) Verdadero si el nodo no es None, falso si es None
        """
        return self.getNodo() is not None

    #GETTERS SIMPLES
    def getNodo(self) -> Nodo[T] | None:
        """Retorna el nodo ingresado en el cursor
        
        **return**
            -   (Nodo[T]) nodo sobre el cual el nodo está poscicionado. Puede ser None
        """
        return self.__nodo

    def getPoscicion(self) -> int:
        """Obtiene la poscición del nodo sobre el que está parado el cursor
        
        **return**
            -   (int) poscición del cursor   
        """
        return self.__poscicion

    #GETTERS COMPLEJOS
    def getDatoCursor(self) -> T:
        """Retorna el dato almacenado en el nodo sobre el cual esta parado el cursor

        **return**
            -   (T): dato almacenado en el cursor
    
        **excepciones**
            -   **ErrorCursorDesactivado** si el cursor no está prendido
        """
        self.validarCursorPrendido()
        return self.getNodo().getDato()

    #SETTERS SIMPLES
    def setNodo(self, nodo:Nodo[T]) -> None:
        """Setea el cursor sobre un nodo ingresado
        
        **parameters**
            -   nodo (Nodo[T]): puede ser None
        
        **excepciones**
            -   **TypeError** si el parametro ingresado no es un None
        """
        if (nodo is not None):
            validarTipoObjeto(Nodo, nodo, "Ingrese un nodo")
        
        self.__nodo = nodo

    def setPoscicion(self, poscicion:int) -> None:
        """Setea la poscición sobre el cual está el cursor
        
        **parameters**
            -   poscicion (int): mayor que cero

        **excepciones**
            -   **TypeError**: Si el parametro ingresado no es int
            -   **IndexError**: Si el indice ingresado es negativo
        """
        self.__validarPoscicion(poscicion)
        self.__poscicion = poscicion

    #SETTERS COMPLEJOS
    def setDatoCursor(self, dato:T) -> None:
        """Setea el dato almacenado en el nodo sobre el cual esta parado el cursor

        **parameters**
            -   dato (T)
    
        **excepciones**
            -   **TypeError**: si el tipo del dato no es el tipo ingreado T
            -   **ErrorCursorDesactivado**: si el cursor no está prendido
        """
        self.validarCursorPrendido()
        self.getNodo().setDato(dato)

#LISTA ---------------------------------------------------------------------------------------------------------------------
class Lista(TypeStruct, Generic[T]):
    #ATRIBUTOS
    __primerNodo:Nodo[T]
    __ultimoNodo:Nodo[T]
    __longitud:int
    __cursores:Vector[Cursor[T]]

    #CONSTRUCTOR
    def __init__(self, tipo) -> Lista[T]:
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
    def __str__(self) -> str:
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

    def __iter__(self):
        cursor = Cursor(self.getType())
        cursor.activarCursor(self.__getPrimero())

        for i in range(self.getLongitud()):
            yield cursor.getDatoCursor()
            
            cursor.avanzarNodo()

    #METODOS DE CLASE
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
        self.__restarObjeto()

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
        self.__restarObjeto()

        return nodo.getDato()

    def mezclar(self):
        """Mezcla los elementos de la lista"""
        vecAux = Vector(self.getType(),self.getLongitud())

        for i in range(vecAux.getLongitud()):
            vecAux[i] = self.quitarInicio()

        vecAux.mezclar()
        for i in range(vecAux.getLongitud()):
            self.agregarFinal(vecAux[i])

    def invertir(self):
        """Invierte la lista poniendo los datos en la poscicion n en la poscion longitud - n"""
        cursor1 = Cursor(self.getType())
        cursor2 = Cursor(self.getType())

        cursor1.activarCursor(self.__getPrimero())
        cursor2.activarCursor(self.__getUltimo())

        for i in range(self.getLongitud()//2):
            aux = cursor1.getDatoCursor()
            cursor1.setDatoCursor(cursor2.getDatoCursor())
            cursor2.setDatoCursor(aux)

            cursor1.avanzarNodo()
            cursor2.retrocederNodo()

        cursor1.desactivarCursor()
        cursor2.desactivarCursor()

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

    def cursoresDisponibles(self, cantidad:int = 1) -> bool:
        """Verfica que haya cursores diponibles
        
        **parameters**
            -   cantidad (int): por defecto 1. Ingrese otra cantidad si necesitas esa cantidad de cursores encendidos

        **excepciones**
            -   
        """ 
        self.__validarIndiceCursor(cantidad)

        disponible = False
        libres = 0
        i = 0

        while (i <= MAXIMO_CURSORES) and (libres < cantidad):
            if (self.__cursores[i].estaPrendido()):
                libres+=1
                
            if libres < cantidad:
                libres = True

            i+=1

        return disponible
    
    def activarCursorInicio(self) -> int:
        """Activa el primer cursor que esté apagado en el primer nodo y retorna el indice del cursor
        
        **return**
            -   (int) indice del cursor (1, 2 o 3)
        
        **excepciones**
            -   **ErrorCursorEncendido**: si todos los cursores estan encendidos
        """
        i = 0
        encedido = False

        while (i < MAXIMO_CURSORES) and not encedido:
            if (not self.__cursores[i].estaPrendido()):
                encedido = True
                self.__cursores[i].activarCursor(self.__getPrimero(), PRIMERA_POSCICION)
            else:
                i+=1
        
        if not encedido:
            raise ErrorCursorEncendido("Todos los cursores han sido encendidos")

        return i+1

    def activarCursorFinal(self) -> int:
        """Activa el primer cursor que esté apagado en el ultimo nodo y retorna el indice del cursor
        
        **return**
            -   (int) indice del cursor (1, 2 o 3)
        
        **excepciones**
            -   **ErrorCursorEncendido**: si todos los cursores estan encendidos
        """
        i = 0
        encedido = False

        while (i < MAXIMO_CURSORES) and not encedido:
            if (not self.__cursores[i].estaPrendido()):
                encedido = True
                self.__cursores[i].activarCursor(self.__getUltimo(), self.__getultimaPoscicion())
            else:
                i+=1

        if not encedido:
            raise ErrorCursorEncendido("Todos los cursores han sido encendidos")

        return i+1

    def iniciarCursorInicio(self, i:int = 1):
        """Prende el cursor y lo posciciona en el primer Nodo de la lista
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorEncendido** si el cursor de la poscicion ingresada esta prendido
        """
        self.__validarCursorNoUsable(i)
        self.__getCursor(i).activarCursor(self.__getPrimero())

    def iniciarCursorFinal(self, i:int = 1):
        """Prende el cursor y lo posciciona en el último Nodo de la lista
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorEncendido** si el cursor de la poscicion ingresada esta prendido
        """
        self.__validarCursorNoUsable(i)
        self.__getCursor(i).activarCursor(self.__getUltimo(), self.__getultimaPoscicion())

    def desactivarCursor(self, i:int = 1):
        """Desactiva el cursor
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado** si el cursor de la poscicion ingresada esta apagado
        """
        self.__validarCursorUsable(i)
        self.__getCursor(i).desactivarCursor()

    def prenderTodosLosCursoresInicio(self):
        """Inicia todos los cursores en el incio de la lista"""
        for cursor in self.__cursores:
            if cursor.estaPrendido():
                cursor.desactivarCursor()

            cursor.activarCursor(self.__getPrimero())

    def prenderTodosLosCursoresFinal(self):
        """Inicia todos los cursores al final de la lista"""
        for cursor in self.__cursores:
            if cursor.estaPrendido():
                cursor.desactivarCursor()

            cursor.activarCursor(self.__getUltimo())

    def apagarTodosLosCursores(self):
        """Apaga todos los cursores que estén prendidos"""
        for cursor in self.__cursores:
            if cursor.estaPrendido():
                cursor.desactivarCursor()

    def avanzarCursor(self, i:int = 1):
        """Mueve el cursor al siguiente nodo
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado** si el cursor de la poscicion ingresada esta apagado
        """
        self.__getCursor(i).avanzarNodo()

    def retrocederCursor(self, i:int = 1):
        """Mueve el cursor al nodo anterior
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado** si el cursor de la poscicion ingresada esta apagado
        """
        self.__getCursor(i).retrocederNodo()

    def insertarCursor(self, dato:T, i:int = 1):
        """Inserta un dato en la lista colocando un nuevo nodo entre el nodo del cursor y el nodo anterior
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado** si el cursor de la poscicion ingresada esta apagado
        """
        self.__validarCursorUsable(i)
        self.__validarEntrada__(dato)

        self.__getCursor(i).insertar(dato)

    def extirparCursor(self, i:int = 1) -> T:
        """Quita el dato del nodo del cursor de la lista y retorna el valor. 
        Luego posciciona el cursor en el siguiente nodo
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado** si el cursor de la poscicion ingresada esta apagado
        """
        self.__validarCursorUsable(i)

        return self.__getCursor(i).extirpar()

    def intercambiarCursorSiguiente(self, i = 1):
        """Intercambia el dato del nodo sobre el cual está posicionado el cursor con el dato del nodo siguiente
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado** si el cursor de la poscicion ingresada esta apagado
        """
        self.__validarCursorUsable(i) 
        
        dato = self.getDatoCursor(i)
        self.__getCursor(i).setDatoCursor(self.__getCursor(i).getNodo().getSiguiente().getDato())
        self.__getCursor(i).getNodo().getSiguiente().setDato(dato)

    def intercambiarCursorAnterior(self, i = 1):
        """Intercabia el dato del nodo sobre el cual está poscicionado el cursor con el dato del nodo anterior
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado** si el cursor de la poscicion ingresada esta apagado
        """
        self.__validarCursorUsable(i) 
        
        dato = self.getDatoCursor(i)
        self.__getCursor(i).setDatoCursor(self.__getCursor(i).getNodo().getAnterior().getDato())
        self.__getCursor(i).getNodo().getAnterior().setDato(dato)

    def intercambiarCursores(self,i:int, j:int):
        """Dado dos indices de cursor, intercambia los datos de ambos cursores
        
        **parameters**
            -   i (int): entre 1 y 3
            -   j (int): entre 1 y 3

        **excepciones**
            -   **TypeError** si algún indice ingresado no es un int
            -   **IndexError** si algún indice es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado** si algún cursor de algúna poscicion ingresada esta apagado
        """
        self.__validarCursorUsable(i)
        self.__validarCursorUsable(j)

        dato = self.getDatoCursor(i)
        self.setDatoCursor(self.getDatoCursor(j), i)
        self.setDatoCursor(dato, j)

    def cursorPrendido(self, i:int = 1) -> bool:
        """Verifica que el cursor esté prendido
        
        **parameters**
            -   i (int): por defecto 1, ingrese 2 o 3 para cambiar de cursor

        **return**
            -   (bool) Verdadero si el cursor está prendido, falso si no

        **excepciones**
            -   **TypeError** si algún indice ingresado no es un int
            -   **IndexError** si algún indice es menor que 1 o mayor que 3
        """
        return self.__getCursor(i).estaPrendido()

    def llegoAlFin(self, i:int = 1) -> bool:
        """Verifica que el cursor esté en la última poscicion
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **return**
            -   (bool): Verdadero si el nodo siguiente al nodo del cursor es None, falso si no
            
        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado** si el cursor de la poscicion ingresada esta apagado
        """
        self.__validarCursorUsable(i)
        return self.__getCursor(i).getNodo().getSiguiente() is None
    
    def llegoAlInicio(self, i:int = 1) -> bool:
        """Verifica que el cursor esté en la primera poscicion
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **return**
            -   (bool): Verdadero si el nodo anterior al nodo del cursor es None, falso si no
            
        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado** si el cursor de la poscicion ingresada esta apagado
        """
        self.__validarCursorUsable(i)
        return self.__getCursor(i).getNodo().getAnterior() is None
    

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

    def __validarIndiceCursor(self, indice:int):
        """Verifica que un indice usado para usar un cursor sea valido

        **parameters**
            -   indice (int): entre 1 y 3

        **excepciones**
            -   **TypeError** si el indice ingresado no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
        """   
        validarTipoObjeto(int, indice, "Ingresa un indice int")
        validarRango(indice, 1 , MAXIMO_CURSORES, 
                     mensaje=f"solo hay {MAXIMO_CURSORES} disponibles"
        )

    def __validarCursorUsable(self, i:int):
        """Valida que, el cursor en la poscicion ingresada i, esté prendido

        **parameters**
            -   i (int): entre 1 y 3

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado** si el cursor de la poscicion ingresada esta apagado
        """
        self.__validarIndiceCursor(i)
        self.__getCursor(i).validarCursorPrendido()

    def __validarCursorNoUsable(self, i:int):
        """Valida que, el cursor en la poscicion ingresada i, este apagado

        **parameters**
            -   i (int): entre 1 y 3

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorEncendido** si el cursor de la poscicion ingresada esta prendido
        """
        self.__validarIndiceCursor(i)
        self.__getCursor(i).validarCursorApagado()

    #METODOS ESTATICOS
    @staticmethod
    def iniciarCursores(*listas:Lista, cursor:int = 1) -> None:
        """Dado una serie de listas, activa los cursores en el primer cursor
        
        **parameters**
            -   *listas (Lista): cualquier tipo de dato almacenado
            -   cursor (int): por defecto 1. Entre 1 y 3

        **excepciones**
            -   **TypeError**: si se ingreso algo que no fuese una lista o si el cursor seleccionado no es int 
            -   **IndexError**: si el cursor es menor que 1 o mayor que 3
        """    
        for lista in listas:
            validarTipoObjeto(Lista, lista, "Ingrese solo listas por parametro")
            if lista.cursorPrendido(cursor):
                lista.desactivarCursor(cursor)

            lista.iniciarCursorInicio(cursor)
    
    @staticmethod
    def finalizarCursores(*listas:Lista, cursor:int = 1) -> None:
        """Dado una serie de listas, activa los cursores en el ultimo cursor
        
        **parameters**
            -   *listas (Lista): cualquier tipo de dato almacenado
            -   cursor (int): por defecto 1. Entre 1 y 3

        **excepciones**
            -   **TypeError**: si se ingreso algo que no fuese una lista o si el cursor seleccionado no es int 
            -   **IndexError**: si el cursor es menor que 1 o mayor que 3
        """    
        for lista in listas:
            validarTipoObjeto(Lista, lista, "Ingrese solo listas por parametro")
            if lista.cursorPrendido(cursor):
                lista.desactivarCursor(cursor)

            lista.iniciarCursorFinal(cursor)

    @staticmethod
    def avanzarCursores(*listas:Lista, cursor:int = 1) -> None:
        """Dado una serie de listas, avanza sus cursores al siguiente nodo
        
        **parameters**
            -   *listas (Lista): cualquier tipo de dato almacenado
            -   cursor (int): por defecto 1. Entre 1 y 3

        **excepciones**
            -   **TypeError**: si se ingreso algo que no fuese una lista o si el cursor seleccionado no es int 
            -   **IndexError**: si el cursor es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado**: si algún cursor de alguna lista ingresada esta apagado
        """    
        for lista in listas:
            validarTipoObjeto(Lista, lista, "Ingrese solo listas por parametro")
            lista.avanzarCursor(cursor)

    @staticmethod
    def retrocederCursores(*listas:Lista, cursor:int = 1) -> None:
        """Dado una serie de listas, retrocede los cursores al nodo anterior
        
        **parameters**
            -   *listas (Lista): cualquier tipo de dato almacenado
            -   cursor (int): por defecto 1. Entre 1 y 3

        **excepciones**
            -   **TypeError**: si se ingreso algo que no fuese una lista o si el cursor seleccionado no es int 
            -   **IndexError**: si el cursor es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado**: si algún cursor de alguna lista ingresada esta apagado
        """    
        for lista in listas:
            validarTipoObjeto(Lista, lista, "Ingrese solo listas por parametro")
            lista.retrocederCursor(cursor)
    
    @staticmethod
    def avanzarCursores(*listas:Lista, cursor:int = 1) -> None:
        """Dado una serie de listas, desactiva todo los cursores
        
        **parameters**
            -   *listas (Lista): cualquier tipo de dato almacenado
            -   cursor (int): por defecto 1. Entre 1 y 3

        **excepciones**
            -   **TypeError**: si se ingreso algo que no fuese una lista o si el cursor seleccionado no es int 
            -   **IndexError**: si el cursor es menor que 1 o mayor que 3
            -   **ErrorCursorDesactivado**: si algún cursor de alguna lista ingresada esta apagado
        """    
        for lista in listas:
            validarTipoObjeto(Lista, lista, "Ingrese solo listas por parametro")
            if not lista.cursorPrendido():
                lista.desactivarCursor(cursor)

    #FLAGS
    def estaVacia(self) -> bool:
        """Verifica que la lista este vacia
        
        **return**
            -   (bool) Verdadero si la lista tiene 0 objetos, falso si tiene mas
        """
        return self.getLongitud() == 0

    #GETTERS SIMPLES
    def getLongitud(self) -> int:
        """Retorna la longitud de la lista
        
        **return**
            -   (int) cantidad de objetos
        """
        return self.__longitud
    
    #GETTERS COMPLEJOS
    def getDatoCursor(self, i:int = 1) -> T:
        """Obtiene el valor de el nodo, sobre el cual, el cursor está parado
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorEncendido** si el cursor de la poscicion ingresada esta prendido
        """
        self.__validarCursorUsable(i)
        return self.__getCursor(i).getDatoCursor()

    def getSiguienteCursor(self, i:int = 1) -> T:
        """Obtiene el valor de el nodo, el cual, es siguiente al nodo sobre el cual el cursor está parado
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorEncendido** si el cursor de la poscicion ingresada esta prendido
        """
        return self.__getCursor(i).getNodo().getSiguiente().getDato()
    
    def getAnteriorCursor(self, i:int = 1) -> T:
        """Obtiene el valor de el nodo, el cual, es anterior al nodo sobre el cual el cursor está parado
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorEncendido** si el cursor de la poscicion ingresada esta prendido
        """
        return self.__getCursor(i).getNodo().getAnterior().getDato()

    #GETTERS INTERNOS SIMPLES
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

    #GETTERS INTERNOS COMPLEJOS
    def __getultimaPoscicion(self) -> int:
        """Obtiene la ultima poscición en la lista
        
        **return**
            -   (int) longitud -1
        """
        return self.getLongitud() - 1

    def __getCursor(self,i:int) -> Cursor[T]:
        """Obtiene un cursor
        
        **parameters**
            -   i (int): entre 1 y 3

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
        """
        self.__validarIndiceCursor(i)
        return self.__cursores[i-1]

    #SETTERS
    def setDatoCursor(self, dato:T, i:int = 1):
        """Setea el valor de el nodo, sobre el cual, el cursor está parado
        
        **parameters**
            -   i (int): por defecto 1. Ingrese 2 o 3 para cambiar de cursor

        **excepciones**
            -   **TypeError** si el indice ingresado i no es un int
            -   **IndexError** si el indice es menor que 1 o mayor que 3
            -   **ErrorCursorEncendido** si el cursor de la poscicion ingresada esta prendido
        """
        self.__validarCursorUsable(i)
        self.__validarEntrada__(dato)
        self.__getCursor(i).setDatoCursor(dato)

    #SETTERS INTERNOS
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
