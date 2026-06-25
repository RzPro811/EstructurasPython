from .Validaciones import TypeStruct, TypeVar, Generic, validarCondicion, validarRango, validarTipoObjeto, validarTipo
from .Vector import PRIMERA_POSCICION
from .Excepciones.Grafo import *

V = TypeVar("V")
E = TypeVar("E")

SIN_ADYACENCIA = 0
ADYAENCIA = 1
AUTO_ADYACENCIA = 2

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
    #CONSTANTES
    __ULTIMO_AGREGADO = -1
    #ATRIBUTOS
    __vertices:list[Vertice[V]]
    __aristas:list[Arista[E]]
    __adyacencia:list[list[int]]
    
    __orientado:bool
    
    __tipoVertice:TypeStruct
    __tipoArista:TypeStruct

    #CONSTRUCTOR
    def __init__(self, tipoVertice:type, tipoArista:type = None, orientado:bool = False):
        self.setTipos(tipoVertice,tipoArista)
        self.__vertices = []
        self.__aristas = []  
        self.__orientado = orientado
        self.__adyacencia = []

    #METODOS GENERALES
    def __str__(self):
        cadena = f"Grafo <{self.getTipoVertice().__name__};"

        if self.getTipoArista() is not None: cadena +=f"{self.getTipoArista().__name__}>\nVertices: "
        else: cadena += "None>\nVertices: "

        i = 0
        for vertice in self.__vertices:
            cadena+=f"({i}) {vertice.getDato()};"
            i+=1
        
        if self.getTipoArista() is not None:
            cadena += "\n Aristas: "
            for arista in self.__aristas:
                cadena += f"({arista.getInicio()};"
                if arista.getFinal() is not None:
                    cadena += f"{arista.getFinal()})"
                else:
                    cadena += f"{arista.getInicio()})"
                cadena += f"{arista.getDato()}; "
        
        return cadena +"\n"
    
    
    #METODOS DE CLASE
    def esOrientado(self) -> bool:
        return self.__orientado

    def agregarVertice(self, dato:V):
        self.__validarTipoV(dato)
        self.__actualizarVertices(Vertice(self.getTipoVertice(),dato))

    def conectarVertices(self, indice:int, jndice:int, dato:E = None):
        self.__validarTipoE(dato)
        self.__valdiarIndices(indice, jndice)

        if indice == jndice:
            arista = Arista(self.getTipoArista(), dato, indice)
        elif self.esOrientado():
            arista = Arista(self.getTipoArista(),dato, indice, jndice)
        else:
            arista = Arista(self.getTipoArista(), dato)

        self.__actualizarAristas(indice,jndice, arista)


    #METODOS INTERNOS
    def __actualizarVertices(self, vertice:Vertice[V]):
        self.__vertices.append(vertice)
        self.__adyacencia.append([])

        for arista in self.__aristas:
            self.__adyacencia[Grafo.__ULTIMO_AGREGADO].append(SIN_ADYACENCIA)

    def __actualizarAristas(self, indice:int, jndice:int, arista:Arista[E]):
        self.__aristas.append(arista)
        
        for i in range(len(self.__vertices)):
            if (i != indice ) and (i != jndice):
                self.__adyacencia[i].append(SIN_ADYACENCIA)
            elif (indice == jndice):
                self.__adyacencia[i].append(AUTO_ADYACENCIA)
            else:
                self.__adyacencia[i].append(ADYAENCIA)

    #VALIDACIONES
    def __valdiarIndices(self, indice:int, jndice:int):
        validarTipoObjeto(int, indice)
        validarTipoObjeto(int, jndice)
        validarRango(indice,PRIMERA_POSCICION,len(self.__vertices) -1)
        validarRango(jndice,PRIMERA_POSCICION,len(self.__vertices) -1)

    def __validarTipoV(self, dato:V):
        self.__tipoVertice.__validarEntrada__(dato)
        
    def __validarTipoE(self, dato:E):
        self.__tipoArista.__validarEntrada__(dato,True)

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