from Validaciones import DataStruct, TypeStruct, Generic, T, validarTipoObjeto, validarCondicion
from.Excepciones.LinkedList import *
#NODO -------------------------------------------------------------------------------------------------------------
class Nodo(DataStruct, Generic[T]):
    #ATRIBUTOS
    __anterior:Nodo[T]
    __siguiente:Nodo[T]
    #CONSTRUCTOR
    #METODOS GENERALES
    #VALIDACIONES
    def __validarConexion(self, nodo:Nodo[T]):
        validarTipoObjeto(Nodo,nodo,"Ingrese un nodo")
        validarCondicion(self.getType() is not nodo.getType(), "Ingresa un nodo con el mismo tipo de dato", NodoInvalidoError)

    #METODO ESTATICOS
    

    #GETTERS
    def getAnterior(self) -> Nodo[T]:
        return self.__anterior
    
    def getSiguiente(self) -> Nodo[T]:
        return self.__siguiente
    
    #SETTERS
    def setAnterior(self, anterior:Nodo[T]):
        self.__anterior = anterior

    def setSiguiente(self, siguiente:Nodo[T]):
        self.__siguiente = siguiente
