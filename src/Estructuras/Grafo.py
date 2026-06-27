from .Validaciones import TypeStruct, TypeVar, Generic, validarValorCompatible, validarCondicion, validarRango, validarTipoObjeto, validarNoNegativo, Enum
from .Excepciones.Grafo import *
from typing import Generator

V = TypeVar("V")
E = TypeVar("E")

SIN_ADYACENCIA = 0
ADYAENCIA = 1


class Grafo(Generic[V,E]):
    #CONSTANTES
    
    #listas de elementos
    __vertices:dict[V,int]
    __aristas:list[list[E]]
    
    #configuracion del grafo
    __adyacencia:list[list[int]]
    __pesos:list[list[int]]
    __pesado:bool

    #tipos de datos
    __tipoV:TypeStruct 
    __tipoE:TypeStruct

    #CONSTRUCTOR
    def __init__(self, tipoVertices:type, tipoAristas:type = None, pesado:bool = False):
        """Construye un grafo dado un tipo de vertices
        
        **parameters**
            -   tipoVertices (type)
            -   tipoAristas (type): por default None. Setea un tipo de dato para almacenar cosas en las aristas de los grafos
            -   pesado (bool): por default False. Si es True, el grafo será un grafo pesado.  

        **excepciones**
            -   **TypeError**: Si ninguno de los datos ingresados es del tipo correspondiente  
        """
        self.__setTiposDatos(tipoVertices, tipoAristas)
        validarTipoObjeto(bool,pesado, "Ingresa verdadero para pesar el grafo o falso para no setearlo")

        self.__vertices = {}
        self.__aristas = []
        self.__adyacencia = []

        self.__pesado = pesado

        if (self.esPesado()):
            self.__pesos = []

    #METODOS GENERALES 
    def __iter__(self) -> Generator[V]:
        """Cada iteracion retorna un vertice"""
        for vertice in self.__vertices:
            yield vertice
        
    #METODOS DE CLASE
    def esPesado(self) -> bool:
        """Verifica que el grafo esté pesado
        
        **return**
            -   (bool) Verdadero si el grafo es pesado, falso si no
        """
        return self.__pesado

    def esPlanar(self):
        return self.getCantidadAristas() <= 3*(self.getCantidadVertices()-2) 
    
    def esEuleriano(self):
        for vertice in self:
            if self.getGradoVertice(vertice) % 2 == 1:
                return False
            
        return True
    
    def esSemiEuleriano(self):
        verticesImpares = 0

        for vertice in self:
            if self.getGradoVertice(vertice) % 2 == 1:
                verticesImpares +=1

            if verticesImpares > 2:
                return False
            
        return verticesImpares == 2

    def estaConectado(self, vertice1:V, vertice2:V) -> bool:
        """Dados dos vertices del grafo, verifica que estén conectados
        
        **parameters**
            -   vertice1 (V): pertenece al grafo
            -   vertice2 (V): pertenece al grafo

        **return**
            -   (bool): Verdadero si en sus respectivos indices de la matriz de adyacencia es 1

        **excepciones**
            -   **TypeError**: si los vertices no son del tipo ingresado V
            -   **VerticeNoEncontradoError**: si al menos un vertice no pertence al grafo
        """
        self.__validarVertice(vertice1)
        self.__validarVertice(vertice2)
        return self.__adyacencia[self.__indiceVertice(vertice1)][self.__indiceVertice(vertice2)] == ADYAENCIA

    def agregarVertice(self, vertice:V):
        """Agrega un vertice al conjunto de vertices del grafo si es que no está ya en el conjunto de vertices
        
        **parameters**
            -   vertice (V): no es parte del grafo

        **excepciones**
            -   **TypeError**: si el vertice no es del tipo ingresado V
            -   **VerticeDobleError**: si el vertice ya es parte del grafo
        """
        self.__validarEntradaVertice(vertice)

        self.__vertices.update({vertice:self.getCantidadVertices()})
        self.__actualizarMatriz(self.__adyacencia, SIN_ADYACENCIA)
        self.__actualizarMatriz(self.__aristas, None)
        if self.esPesado():
            self.__actualizarMatriz(self.__pesos)

    def eliminarVertice(self, vertice:V):
        """Dado un vertice del grafo, lo elimina"""
        self.__validarVertice(vertice)
        indice = self.__indiceVertice(vertice)
        
        self.__desactualizarMatriz(self.__adyacencia, indice)
        self.__desactualizarMatriz(self.__aristas, indice)
        self.__vertices.pop(vertice)
        self.__eliminarRastro()

        if self.esPesado():
            self.__desactualizarMatriz(self.__pesos, indice)


    def conectarVertices(self, vertice1:V, vertice2:V, coneccion:E = None, peso:int = None):
        """Dados dos vertices, los conecta. Si se ingresa un dato de arista o un peso, se ingresan como datos
        
        **parameters**
            -   vertice1 (V): no debe estar conectado al vertice2
            -   vertice2 (V): no debe estar conectado al vertice1
            -   coneccion (E): por defecto None
            -   peso (int): por defecto None. Mayor que cero

        **excepciones**
            -   **TypeError**: Si al menos uno de los datos no son de ninguno de los tipos especificados
            -   **VerticeNoEncontradoError**: si alguno de los vertices no pertenece al grafo
            -   **AdyacenciaError**: Si los datos ya estan conectados
            -   **TipoGrafoIncompatible**: si se ingresa un peso siendo el grafo no pesado
            -   **PesoInvalido**: si el peso es menor o igual a cero
        """

        self.__validarConexion(vertice1,vertice2,coneccion,peso)
        self.__conectarVertices(vertice1,vertice2,ADYAENCIA,coneccion,peso)
        self.__conectarVertices(vertice2,vertice1,ADYAENCIA,coneccion,peso)
        

    def desconectarVertices(self, vertice1:V, vertice2:V):
        """Dados dos vertices del grafo, los conecta
        
        **parameters**
            -   vertice1 (V): pertenece al grafo
            -   vertice2 (V): pertenece al grafo

        **excepciones**
            -   **TypeError**: Si al menos uno de los datos no son de ninguno de los tipos especificados
            -   **VerticeNoEncontradoError**: si alguno de los vertices no pertenece al grafo
            -   **AdyacenciaError**: Si los datos no estan conectados
        """
        self.__validarDesconexion(vertice1, vertice2)
        self.__conectarVertices(vertice1, vertice2, SIN_ADYACENCIA, SIN_ADYACENCIA)
        if not self.estaConectado(vertice1, vertice2):
            self.__conectarVertices(vertice2, vertice1, SIN_ADYACENCIA, SIN_ADYACENCIA)


    #METODOS INTERNOS

    def __actualizarMatriz(self, matriz:list[list[int]], dato:int|E):
        if self.getCantidadVertices() == 1:
            matriz.append([dato])
            
        else:
            for listaAdyacencia in matriz:
                listaAdyacencia.append(dato)
            matriz.append([dato]*self.getCantidadVertices())

    def __desactualizarMatriz(self, matriz:list[list[int]], indice:int):
        for listaAdyacencia in matriz:
            listaAdyacencia.pop(indice)

        matriz.pop(indice)
        
    def __eliminarRastro(self):
        anterior = -1

        for vertice in self.__vertices:
            if self.__vertices[vertice] != anterior +1:
                self.__vertices[vertice] -= 1

            anterior = self.__vertices[vertice]

    def __indiceVertice(self,vertice:V) -> int:
        self.__validarVertice(vertice)
        return self.__vertices[vertice]

    def __conectarVertices(self, vertice1:V, vertice2:V, tipoAdyacencia:int, coneccion:E, peso:int):
        i = self.__indiceVertice(vertice1)
        j = self.__indiceVertice(vertice2)
        validarValorCompatible(i,j,"No se puede conectar un vertice consigo mismo en este tipo de grafo",AdyacenciaError)

        self.__adyacencia[i][j] = tipoAdyacencia
        self.__aristas[i][j]    = coneccion 
        
        if self.esPesado():
            self.__pesos[i][j] = peso

    #VALIDACIONES
    def __validarConexion(self, vertice1:V, vertice2:V, coneccion:E, peso:int):
        self.__validarVertice(vertice1)
        self.__validarVertice(vertice2)
        self.__validarArista(coneccion)        
        self.__vaidarPeso(peso)
        validarCondicion(self.estaConectado(vertice1, vertice2), "Estos vertices ya estan conectados", AdyacenciaError)

    def __validarDesconexion(self, vertice1:V, vertice2:V):
        self.__validarVertice(vertice1)
        self.__validarVertice(vertice2)
        validarCondicion(not self.estaConectado(vertice1, vertice2),"Estos vertices no estan conectados", AdyacenciaError)


    def __validarEntradaVertice(self, vertice:V):
        self.__tipoV.__validarEntrada__(vertice)
        validarCondicion(vertice in self.__vertices.keys(),"Este vertice ya se añadió al grafo", VerticeDobleError)

    def __validarVertice(self, vertice:V):
        self.__tipoV.__validarEntrada__(vertice)
        validarCondicion(vertice not in self.__vertices.keys(), 
                         "Este vertice no pertenece al grafo", VerticeNoEncontradoError)

    def __validarArista(self, arista:E):
        self.__tipoE.__validarEntrada__(arista,True)
                
    def __vaidarPeso(self, peso:int):
        if (self.esPesado()):
            validarTipoObjeto(int, peso, "Ingrese un peso int")
            validarNoNegativo(peso,False,"Ingrese un peso mayor que cero",PesoInvalido)
        elif (peso is not None):
            raise TipoGrafoIncompatible("Esta operacion no se puede hacer porque el grafo no está pesado")

    #ESTATICOS
    @staticmethod
    def validarGrafo(grafo:Grafo):
        validarTipoObjeto(Grafo, grafo, "Ingrese un grafo")

    @staticmethod
    def validarOperacionDeGrafo(grafo1:Grafo, grafo2:Grafo):
        Grafo.validarGrafo(grafo1)
        Grafo.validarGrafo(grafo2)

        validarCondicion(grafo1.getTipoVertice() is not grafo2.getTipoVertice(), 
                         "Ingresa dos grafos con el mismo tipo de vertices")
        validarCondicion(grafo1.getTipoArista()  is not grafo2.getTipoArista(), 
                         "Ingresa dos grafos con el mismo tipo de aristas")

    @staticmethod
    def union(grafo1:Grafo[V,E],grafo2:Grafo[V,E]) -> Grafo[V,E]:
        pass

        
    @staticmethod
    def ensamblarGrafos(grafo1:Grafo[V,E],grafo2:Grafo[V,E]) -> Grafo[V,E]:
        pass



    #GETTERS

    #Calculables
    def getCantidadVertices(self) -> int:
        return len(self.__vertices)

    def getCantidadAristas(self) -> int:
        vertices = 0

        for vertice in self.__vertices:
            vertices += self.getGradoVertice(vertice)

        return vertices // 2

    def getCantidadCaras(self) -> int:
        if self.esPlanar():
            return 2 + self.getCantidadAristas() - self.getCantidadCaras()
        else: return 0

    def getGradoVertice(self, vertice:V) -> int:
        self.__validarVertice(vertice)
        indice = self.__indiceVertice(vertice)
        grado = 0

        for adyacencia in self.__adyacencia[indice]:    
            grado += adyacencia
        
        return grado

    #Atributos
    def getVertices(self) -> set:
        vertices = set({})
        for vertice in self.__vertices:
            vertices.add(vertice)

        return vertices
    
    def getTipoVertice(self) -> type:
        return self.__tipoV.getType()
    def getTipoArista(self) -> type:
        return self.__tipoE.getType()


    #SETTERS

    def __setTiposDatos(self, tipoVertices:type, tipoAristas:type = None):
        self.__tipoV = TypeStruct(tipoVertices)
        self.__tipoE = TypeStruct(tipoAristas)
