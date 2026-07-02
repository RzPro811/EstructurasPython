from Validaciones import DataStruct, TypeStruct, Generic, T, validarTipoObjeto, validarCondicion
from.Excepciones.LinkedList import *
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
        
        """
        super().__init__(tipo, dato, False)

    #METODOS GENERALES
    def __str__(self):
        cadena = ""

        if self.getAnterior() is not None:
            cadena+= f"[{self.getAnterior().getDato()}] -"

        cadena+= "{"+f"{self.getDato()}"+"}"

        if self.getSiguiente() is not None:
            cadena+= f"- [{self.getAnterior()}]"

        return cadena
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, value:Nodo):
        if type(value) is not Nodo: return False
        return self.getDato() == value.getDato()

    #VALIDACIONES
    def __validarConexion(self, nodo:Nodo[T]):
        if nodo is not None:
            validarTipoObjeto(Nodo,nodo,"Ingrese un nodo")
            validarCondicion(self.getType() is not nodo.getType(), 
                         "Ingresa un nodo con el mismo tipo de dato", NodoInvalidoError)

    @staticmethod
    def validarConeccion(nodo1:Nodo[T], nodo2:Nodo[T]):
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
        Nodo.validarConeccion(nodoAnterior, nodoSiguiente)

        if nodoAnterior is not None:
            nodoAnterior.setSiguiente(nodoSiguiente)
        if nodoSiguiente is not None:
            nodoSiguiente.setAnterior(nodoAnterior)

    @staticmethod
    def desconectarNodo(nodo:Nodo[T]):
        validarTipoObjeto(Nodo, nodo, "Ingrese un nodo")

        nodo.setSiguiente(None)
        nodo.setAnterior(None)



    #GETTERS
    def getAnterior(self) -> Nodo[T]:
        return self.__anterior
    
    def getSiguiente(self) -> Nodo[T]:
        return self.__siguiente
    
    #SETTERS
    def setAnterior(self, anterior:Nodo[T]):
        self.__validarConexion(anterior)
        self.__anterior = anterior

    def setSiguiente(self, siguiente:Nodo[T]):
        self.__validarConexion(siguiente)
        self.__siguiente = siguiente
