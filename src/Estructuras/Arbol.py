from Heredables import TypeStruct, DataStruct, Generic, T
from Validaciones import validarTipoObjeto

#SEMILLA -------------------------------------------------------------------------------------------------------------
class SemillaBin(DataStruct, Generic[T]):
    #ATRIBUTOS
    __izquierda:SemillaBin[T]
    __derecha:SemillaBin[T]

    #CONSTRUCTOR
    def __init__(self, tipo, dato):
        super().__init__(tipo, dato, False)
        self.setIzquierda(None)
        self.setDerecha(None)

    #METODOS DE CLASE
    def tieneHijoIzq(self) -> bool:
        return self.getIzquierda() is not None

    def tieneHijoDer(self) -> bool:
        return self.getDerecha() is not None

    def tieneHijos(self) -> bool:
        return self.tieneHijoDer() or self.tieneHijoIzq()

    def tieneAmbosHijos(self) -> bool:
        return self.tieneHijoIzq() and self.tieneHijoDer()

    def desconectar(self):
        self.setIzquierda(None)
        self.setDerecha(None)

    #VALIDACIONES
    @staticmethod
    def validarSemilla(semilla:SemillaBin):
        if semilla is not None:
            validarTipoObjeto(SemillaBin, semilla, "Ingresa una semilla")

    #METODOS ESTATICOS
    @staticmethod
    def intercambiarDatos(semilla1:SemillaBin, semilla2:SemillaBin):
        dato = semilla1.getDato()
        semilla1.setDato(semilla2.getDato())
        semilla2.setDato(dato)
        
    #GETTERS
    def getEquilibrio(self) -> int:
        if not self.tieneHijos():
            return 0

        if self.tieneAmbosHijos():
            return self.getIzquierda().getEquilibrio() + self.getDerecha().getEquilibrio()

        if self.tieneHijoIzq():
            return -1 + self.getIzquierda().getEquilibrio()

        return 1 + self.getDerecha().getEquilibrio()

    def getIzquierda(self) -> SemillaBin[T]:
        return self.__izquierda

    def getDerecha(self) -> SemillaBin[T]:
        return self.__derecha

    #SETTERS
    def setIzquierda(self, izquierda:SemillaBin[T]):
        SemillaBin.validarSemilla(izquierda)
        self.__izquierda = izquierda

    def setDerecha(self, derecha:SemillaBin[T]):
        SemillaBin.validarSemilla(derecha)
        self.__derecha = derecha


#ARBOL --------------------------------------------------------------------------------------------------------------
class ArbolBin(Generic[T], TypeStruct):
    #ATRIBUTOS
    __raiz:SemillaBin[T]
    __ordenamiento:function

    #CONSTRUCTOR
    def __init__(self, tipo, metodo:function = None):
        super().__init__(tipo)

        self.__ordenamiento = metodo
        self.__raiz = None


    #GETTERS
    def getCantidadElementos(self) -> int:
        return 0
    
    #SETTERS
    