from .Validaciones import TypeStruct, TypeVar, Generic, validarCondicion, validarRango, validarTipoObjeto, validarTipo
from .Vector import PRIMERA_POSCICION
from .Excepciones.Grafo import *

V = TypeVar("V")
E = TypeVar("E")

SIN_ADYACENCIA = 0
ADYAENCIA = 1

#VERTICE-------------------------------------------------------------------------------------------------------------------
class Vertice(Generic[V], TypeStruct):
    #ATRIBUTOS
    __dato:V
    __adyacencia:list[Vertice[V]]

    #CONSTRUCTORES
    def __init__(self, tipo:type, dato:V):
        """Dado un tipo de dato y un dato, crea un vertice de Grafo
        
        **parameters**
            -   tipo (type)
            -   dato (V)

        **excepciones**
            -   **TypeError**: si el tipo ingresado no es type o si el dato no es del tipo ingresado
        """
        super().__init__(tipo)
        self.setDato(dato)
        self.__adyacencia = []

    #METODOS DE CLASE
    def conectar(self, vertice:Vertice):
        """Conecta este vertice con otro vertice

        **parameters**
            -   vertice (Vertice)
        
        **excepciones**
            -   **TypeError**: si el vertice ingresado no es type o comparten el mismo tipo de dato (incluyendo herencia)
        """
        self.__validarConexion(vertice)
        self.__adyacencia.append(vertice)

    def desconectar(self, vertice:Vertice):
        """Dado un vertice adyacente a este vertice, lo desconecta

        **parameters**
            -   vertice (Vertice): deben estar conectado

        **excepciones**
            -   **TypeError**: si el vertice ingresado no es vertice 
            -   **AdyacenciaError**: si el vertice ingresado no es adyacente a este vertice
        """
        self.__validarDesconexión(vertice)
        self.__adyacencia.remove(vertice)

    #VALIDACIONES
    def __validarConexion(self, vertice:Vertice[V]):
        """Valida que un vertice con el cual vamos a conectar, sea valido

        **parameters**
            -   vertice (Vertice): tiene que soportar el mismo tipo de dato, o subclase, del vertice original

        **excepciones**
            -   **TypeError**: si el vertice ingresado no es vertice o su tipo asignado no es el mismo, o no es subclase, que el tipo del vertice original
        """
        self.validarVertice(vertice)
        validarCondicion(not issubclass(vertice.getType(),self.getType() or not issubclass(self.getType(), vertice.getType())),
                         "La clase del vertice con el que intentamos realizar la conexión no es valida", TypeError)
            
    def __validarDesconexión(self, vertice:Vertice[V]):
        """Valida que un vertice este conectado

        **parameters**
            -   vertice (Vertice): deben estar conectado

        **excepciones**
            -   **TypeError**: si el vertice ingresado no es vertice 
            -   **AdyacenciaError**: si el vertice ingresado no es adyacente a este vertice
        """
        self.validarVertice(vertice)
        validarCondicion(vertice not in self.__adyacencia, "El vertice ingresado no es adyacente a este vertice", AdyacenciaError)

    @staticmethod
    def validarVertice(vertice:Vertice):
        """Valida que un vertice sea un vertice
        
        **parameters**
            -  vertice (Vertice)

        **excepciones**:
            -   TypeError: si el parametro ingresado no es un vertice
        """
        validarTipoObjeto(Vertice,vertice,"Ingrese un vertice")

    #GETTERS

    #calculables
    def getGrado(self) -> int:
        """Retorna el grado del vertice, es decir, con cuantos vertices tiene adyacencia
        
        **return**
            -   (int) cantidad de vertices con los que limita
        """
        return len(self.__adyacencia)
    
    def getVerticeAdyacente(self, pos:int) -> Vertice[V]:
        
        return self.__adyacencia[pos]


    #atributos
    def getDato(self) -> V:
        """Retorna el tipo de dato almacenado en el vertice del grafo
        
        **return**
            -   **V**: dato 
        """
        return self.__dato

    #SETTERS
    def setDato(self, dato:V):
        """Setea el dato almacenado en el vertice del grafo
        
        **parameters**
            -   dato **V**: tipo de dato
        
        **Excepciones**
            -   **TypeError**: si el dato no es el tipo que admite el vertice
        """
        self.__validarEntrada__(dato)
        self.__dato = dato



#ARISTA--------------------------------------------------------------------------------------------------------------------
class Arista(Generic[E], TypeStruct):
    #ATRIBUTOS
    __dato:E
    __indiceInicio:int
    __indiceFinal:int
    
    #CONSTRUCTOR
    def __init__(self, tipo:type, dato:E = None, inicio:int = None, final:int = None):
        """Dado un tipo de dato y un dato, crea una Arista de grafo. 
        introduce un indice de vertice inicial y final si la arista esta orientada,
        introduzca un indice inicial int y uno final None si la arista entra y sale del mismo vertice
        o introduzca ambos indices como None si la arista no esta orientada

        **parameters**
            -   tipo (type)
            -   dato (E): Por defecto None. Del tipo ingresado por parametro, si el tipo ingresado es None, el dato debe permanecer como None
            -   inicio (int): por defecto None
            -   final (int): por defecto None. Si inicio es None, final debe permanecer siendo None

        **excepciones**
            -   **TypeError**: si alguno de los datos ingresados no es del tipo que les corresponde
            -   **AdyacenciaError**: si el parametro inicio es None y el parametro final es int
        """
        self.__setType(tipo)        
        self.setDato(dato)
        self.setExtremos(inicio, final)

    #VALIDACIONES
    def __validarExtremos(self, inicio:int, final:int):
        if inicio is not None:    
            validarTipoObjeto(int, inicio, "Ingrese un indice inicial entero o None")

        if final is not None:
            validarCondicion(inicio is None, "No se permite tener un inicio None y final entero", AdyacenciaError)
            validarTipoObjeto(int, final, "Ingrese un indice final entero o None")
    

    #GETTERS
    def getDato(self) -> E:
        """Retorna el tipo de dato almacenado en la arista del grafo
        
        **return**
            -   **E**: dato 
        """
        return self.__dato
    
    def getInicio(self) -> int:
        return self.__indiceInicio

    def getFinal(self) -> int:
        return self.__indiceFinal 

    #SETTERS
    def setDato(self, dato:E):
        """Setea el dato almacenado en la arista del grafo
        
        **parameters**
            -   dato **E**: tipo de dato
        
        **Excepciones**
            -   **TypeError**: si el dato no es el tipo que admite la arista
        """
        self.__validarEntrada__(dato, True)
        self.__dato = dato

    def setExtremos(self, inicio:int, final:int):
        self.__validarExtremos(inicio, final)
        self.__indiceInicio = inicio
        self.__indiceFinal = final

    #HERENCIA

    #setters
    def __setType(self, tipo:type):
        if tipo is not None: validarTipo(tipo)
        self.__tipo = None


#CURSOR--------------------------------------------------------------------------------------------------------------------
class Cursor(Generic[V,E]):
    #ATRIBUTOS
    __vertice:Vertice[V]
    __aristas:list[Arista[E]]


#GRAFO---------------------------------------------------------------------------------------------------------------------
class Grafo(Generic[V,E]):
    #ATRIBUTOS
    __vertices:list[Vertice[V]]
    __adyacencia:list[list[int]]
    __orientado:bool
    __tipoVertice:TypeStruct
    __tipoArista:TypeStruct

    #CONSTRUCTOR

    #GETTERS
    
    #Calculables

    #Atributos
    def getTipoVertice(self) -> type:
        return self.__tipoVertice.getType()
    
    def getTipoArista(self) -> type:
        if self.__tipoArista is not None:
            return self.__tipoArista.getType()
        return None
    
    #SETTERS
    def setTipos(self, tipoVertice:type, tipoArista:type):
        self.__tipoVertice = TypeStruct(tipoVertice)
        
        if tipoArista is not None:
            self.__tipoArista = TypeStruct(tipoArista)
        else:
            self.__tipoArista = None