from .__Validaciones import (TypeVar,  ValidarTipoUnico, validarValorCompatible, 
                           validarCondicion, validarTipoObjeto, validarTiposPorHerencia)
from .__Heredables import TypeStruct, Generic
from .__Excepciones.Grafo import *
from .__Excepciones.Generales import VacioError
from .__Vector import Matriz, Vector, PRIMERA_POSCICION
from typing import Generator

try:
    from matplotlib import pyplot as plt
    from matplotlib.backend_bases import MouseEvent
    from matplotlib.axes import Axes
    import networkx as nx
except ImportError:
    pass

V = TypeVar("V")
E = TypeVar("E")

SIN_ADYACENCIA = 0
ADYAENCIA = 1
ANTIADYACENCIA = -1 
DISTANCIA_ACEPTADA = 0.25
MARGEN = 0.5


nodoSeleccionado = None
#Grafo ------------------------------------------------------------------------------------------------------------
class Grafo(Generic[V,E]):
    #CONSTANTES
    
    #listas de elementos
    __vertices:dict[V,int]
    __aristas:Matriz[E]
    
    #configuracion del grafo
    __adyacencia:Matriz[int]

    #tipos de datos
    __tipoV:TypeStruct 
    __tipoE:TypeStruct

    #CONSTRUCTOR
    def __init__(self, tipoVertices:type, tipoAristas:type = None):
        """Construye un grafo dado un tipo de vertices
        
        **parameters**
            -   tipoVertices (type)
            -   tipoAristas (type): por default None. Setea un tipo de dato para almacenar cosas en las aristas de los grafos
            -   pesado (bool): por default False. Si es True, el grafo será un grafo pesado.  

        **excepciones**
            -   **TypeError**: Si ninguno de los datos ingresados es del tipo correspondiente  
        """
        self.__setTiposDatos(tipoVertices, tipoAristas)
        
        self.__vertices = {}
        

    #METODOS GENERALES 
    def __iter__(self) -> Generator[V]:
        """Cada iteracion retorna un vertice"""
        for vertice in self.__vertices:
            yield vertice
        
    #METODOS DE CLASE
    def esPesado(self) -> bool:
        """Verifica que el grafo esté pesado
        
        **return**
            -   (bool) Verdadero si el tipo de vertice no es None, falso si si
        """
        return self.getTipoArista() is not None

    def esConexo(self) -> bool:
        conexo = True
        recorrido = []
        i = PRIMERA_POSCICION

        while conexo and i < self.getCantidadVertices() - 1:
            conexo = False

            for vertice in self:
                if len(recorrido) == 0: 
                    recorrido.append(vertice)
                if self.estaConectado(vertice,recorrido[i]):
                    conexo = True
                if (vertice not in recorrido):
                    recorrido.append(vertice)

            i+=1

        return conexo

    def esPlanar(self) -> bool:
        """Verifica que un grafo sea planar. Es decir, que se pueda graficar sin que se crucen ninguna aristas
        
        **return**
            -   (bool) Verdadero si cumple que la cantidad de aristas es mayor a 3 * (cantidad de vertices - 2),
            (si es el caso, el grafo es planar). Falso si no
        """
        return self.getCantidadAristas() <= 3*(self.getCantidadVertices()-2) 
    
    def esEuleriano(self) -> bool:
        """Verifica que el grafo sea euleriano. Es decir, que el grado de todos los vertices sea par.
        
        **return**
            -   (bool) Verdadero si todos los vertices tienen grado par, falso si al menos uno es impar
        """
        for vertice in self:
            if self.getGradoVertice(vertice) % 2 == 1:
                return False
            
        return True
    
    def esSemiEuleriano(self) -> bool:
        """Verifica que el grafo sea semieuleriano. Es decir, que solo haya dos vertices de grafo impar
        
        **return**
            -   (bool) Verdadero si solo dos vertices tienen grado impar, falso si no
        """
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
        return self.__adyacencia.getItem(self.__indiceVertice(vertice1),self.__indiceVertice(vertice2)) == ADYAENCIA

    def tieneConexion(self, vertice:V) -> bool:
        self.__validarVertice(vertice)

        for vertex in self:
            if self.estaConectado(vertice, vertex):
                return True

        return False

    def existeCamintoEntre(self, vertice1:V, vertice2:V) -> bool:
        self.__validarVertice(vertice1, vertice2)

        vertices = self.getVertices()
        hayCamino = True
        i = PRIMERA_POSCICION
        recorrido = [vertice1]

        while hayCamino and (vertice2 not in recorrido):
            hayCamino = False

            for vertice in vertices:
                if self.estaConectado(vertice, recorrido[i]) and (vertice not in recorrido):
                    hayCamino = True
                    recorrido.append(vertice)

            i+=1

        return hayCamino

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

        if self.getCantidadVertices() == 1:
            self.__crearMatrices()
        else:
            self.__actualizarMatrices()

    def eliminarVertice(self, vertice:V):
        """Dado un vertice del grafo, lo elimina
        
        **parameters**
            -   vertice (V): Tiene que estar en el grafo

        **excepciones**
            -   **TypeError** si la entrada no es un objeto del tipo ingresado V+
            -   **VerticeNoEncontradoError** si el vertice no es parte del grafo
        """
        self.__validarVertice(vertice)
        
        if self.getCantidadVertices() == 1:
            self.__destruirMatrices()
        else:
            self.__desactualizarMatrices(vertice)
        
        self.__vertices.pop(vertice)
        self.__eliminarRastro()

    def conectarVertices(self, vertice1:V, vertice2:V, coneccion:E = None):
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

        self.__validarConexion(vertice1,vertice2,coneccion)
        self.__conectarVertices__(vertice1,vertice2,ADYAENCIA,coneccion)
        self.__conectarVertices__(vertice2,vertice1,ADYAENCIA,coneccion)
        

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

        self.__conectarVertices__(vertice1, vertice2, SIN_ADYACENCIA, None, SIN_ADYACENCIA)
        self.__conectarVertices__(vertice2, vertice1, SIN_ADYACENCIA, None, SIN_ADYACENCIA)

    def esVertice(self,vertice:V) -> bool:
        """Pregunta si un elemento en la matriz es vertice del grafo
        
        **parameters**
            -   vertice (V)

        **return**
            -   (bool) verdadero si este dato es vertice del grafo, falso si no
        
        **excepciones**
            -   **TypeError**: si el vertice no es del tipo ingresado V

        """
        validarTipoObjeto(self.getTipoVertice(),vertice)
        return vertice in self.getVertices()


    #METODOS INTERNOS
    def __crearMatrices(self):
        """Inicializa las matrices cuando sea necesario crearlas"""
        self.__adyacencia = Matriz(int, PRIMERA_POSCICION+1, PRIMERA_POSCICION+1)
        self.__adyacencia.setItem(PRIMERA_POSCICION, PRIMERA_POSCICION,SIN_ADYACENCIA)

        if self.esPesado():
            self.__aristas = Matriz(self.getTipoArista(),PRIMERA_POSCICION+1, PRIMERA_POSCICION+1)

    def __actualizarMatrices(self):
        """Añadice una fila y una columna a las respectivas matrices de la matriz"""
        self.__adyacencia.expandirMatriz(datoInicial= SIN_ADYACENCIA)
        

        if self.esPesado():
            self.__aristas.expandirMatriz(datoInicial= None)

    def __desactualizarMatrices(self, vectice:V):
        """Dado un vertice, elimina su respectiva fila y columna de las matrices de la lista
        
        **parameters**
            -   vertice (V): pertenece al grafo

        **excepciones**
            -   **TypeError**: si el vertice no es del tipo ingresado V
            -   **VerticeNoEncontradoError**: si el vertice no pertenece al grafo
        """
        indice = self.__indiceVertice(vectice)

        self.__adyacencia.contraerMatriz(indice, indice)

        if self.esPesado():
            self.__aristas.contraerMatriz(indice, indice)
    
    def __destruirMatrices(self):
        """Elimina las matrices del grafo"""
        self.__adyacencia = None

        if self.esPesado():
            self.__aristas = None
        
    def __eliminarRastro(self):
        """Si un vertice es eliminado, este metodo se encarga de corregir los indices de cada vertice"""
        anterior = -1

        for vertice in self.__vertices:
            if self.__vertices[vertice] != anterior +1:
                self.__vertices[vertice] -= 1

            anterior = self.__vertices[vertice]

    def __indiceVertice(self,vertice:V) -> int:
        """Dado un vertice del grafo, retorna el indice del vertice
        
        **parameters**
            -   vertice (V): pertenece al grafo
            
        **return**
            -   (int): indice del vertice

        **excepciones**
            -   **TypeError**: si el vertice no es del tipo ingresado V
            -   **VerticeNoEncontradoError**: si el vertice no pertenece al grafo
        """
        self.__validarVertice(vertice)
        return self.__vertices[vertice]

    def __conectarVertices__(self, vertice1:V, vertice2:V, tipoAdyacencia:int, coneccion:E):
        """Dado dos vertices, un tipo de ayacencia, un dato de arista, y un peso, conecta los dos vertices ingresados
        ingresando el tipo de Adyacencia en la matriz de adyacencia, la coneccion en la matriz de aristas,
        y el peso en la matriz de pesos
        
        **parameters**
            -   vertice1 (V): pertenece al grafo
            -   vertice2 (V): pertenece al grafo
            -   tipoAdyacencia (int): 0 (SIN ADYACENCIA) o 1 (ADYACENCIA)
            -   coneccion (E)

        **Excepciones**
            -   **AdyacenciaError**: si los dos vertices ingresados son el mismo vertice
        """
        i = self.__indiceVertice(vertice1)
        j = self.__indiceVertice(vertice2)
        validarValorCompatible(i,j,"No se puede conectar un vertice consigo mismo en este tipo de grafo",AdyacenciaError)

        self.__adyacencia.setItem(i,j, tipoAdyacencia)

        if self.esPesado():
            self.__aristas.setItem(i,j,coneccion)

    
    def __cargarConexion(self, grafoDonante:Grafo[V,E]):
        """Dado un grafo con los mismos tipo de vertices, 
        ingresa todos los vertices y aristas del otro grafo en este grafo
        
        **parametros**
            -   grafoDonante (Grafo[V,E])
        """
        for vertice in grafoDonante:
            if not self.esVertice(vertice):
                self.agregarVertice(vertice)

        for vertice1 in grafoDonante:
            for vertice2 in grafoDonante:
                if grafoDonante.estaConectado(vertice1,vertice2) and not self.estaConectado(vertice1, vertice2):
                    self.conectarVertices(vertice1, vertice2)

    #VALIDACIONES
    def __validarConexion(self, vertice1:V, vertice2:V, coneccion:E):
        """Hace las validaciones necesarias para conectar dos vertices
        
        **parameters**
            -   vertice1 (V): pertenece al grafo y no está conectado a vertice2
            -   vertice2 (V): pertenece al grafo y no está conectado a vertice1
            -   coneccion (E): puede ser None

        **excepciones**
            -   **TypeError** si ninguno de las entradas tiene el tipo de dato correspondiente
            -   **VerticeNoEncontradoError** si alguno de los vertices no pertece al grafo
            -   **AdyacenciaError** si los vertices ya están conectados
            -   **TipoGrafoIncompatible** si el grafo no es pesado y se ingreso un peso
        """
        self.__validarVertice(vertice1)
        self.__validarVertice(vertice2)
        self.__validarArista(coneccion)
        validarCondicion(self.estaConectado(vertice1, vertice2), "Estos vertices ya estan conectados", AdyacenciaError)

    def __validarDesconexion(self, vertice1:V, vertice2:V):
        """Realiza las validaciones necesarias para desconectar dos vertices
        
        **parameters**
            -   vertice1 (V): pertenece al grafo y está conectado a vertice2
            -   vertice2 (V): pertenece al grafo y está conectado a vertice1
    
        **excepciones**
            -   **TypeError**: si alguno de los vertices no es del tipo ingresado V
            -   **VerticeNoEncontradoError** si alguno de los vertices no pertece al grafo
            -   **AdyacenciaError** si los vertices no están conectados
        """
        self.__validarVertice(vertice1)
        self.__validarVertice(vertice2)
        validarCondicion(not self.estaConectado(vertice1, vertice2),"Estos vertices no estan conectados", AdyacenciaError)


    def __validarEntradaVertice(self, vertice:V):
        """Valida el ingreso de un nuevo vertice
        
        **parameters**
            -   vertice (V): no pertence al grafo

        **excepciones**
            -   **TypeError**: si el vertice no es del tipo ingresado V
            -   **VerticeDobleError**: si el vertice ya está en el grafo
        """
        self.__tipoV.__validarEntrada__(vertice)
        validarCondicion(vertice in self.__vertices.keys(),"Este vertice ya se añadió al grafo", VerticeDobleError)

    def __validarVertice(self, *vertices:V):
        """Valida un vertice para el funcionamiento del grafo
        
        **parameters**
            -   vertice (V): pertenece al grafo
        
        **excepciones**
            -   **TypeError**: si el vertice no es del tipo ingresado V
            -   **VerticeNoEncontradoError**: si el vertice no pertenece al grafo
        """
        for vertice in vertices:
            self.__tipoV.__validarEntrada__(vertice)
            validarCondicion(vertice not in self.__vertices.keys(), 
                            "Este vertice no pertenece al grafo", VerticeNoEncontradoError)

    def __validarArista(self, arista:E):
        """Valida que un dato ingresado sea una arista valida
        
        **parameters**
            -   arista (E): puede ser None
        
        **excepciones**
            -   **TypeError**: si el dato ingresado no es del tipo ingresado E
        """
        self.__tipoE.__validarEntrada__(arista,True)

    def __validarPeso(self):
        validarCondicion(not self.esPesado(), 
                         "Para este metodo, es necesario que el grafo esté pesado, osea que el tipo E no sea None", TipoGrafoIncompatible)
        validarTiposPorHerencia(self.getTipoArista(), int, float, 
                                mensaje= "Para este metodo, el tipo de arista E debe ser un numero real (int, float o Numerico)", error= PesoInvalido)

    #ESTATICOS
    @staticmethod
    def validarGrafo(grafo:Grafo):
        """Dado un grafo, valida que sea un grafo
        
        **parameters**
            -   grafo (Grafo)

        **excepciones**
            -   **TypeError** si el parametro ingresado no es un Grafo
        """
        validarTipoObjeto(Grafo, grafo, "Ingrese un grafo")

    @staticmethod
    def validarOperacionDeGrafo(grafo1:Grafo, grafo2:Grafo):
        """Dado dos grafos, valida que sean compatibles para realizar las respectivas operaciones
        
        **parameters**
            -   grafo1 (Grafo[V,E])
            -   grafo2 (Grafo[V,E])

        **excepciones**
            -   **TypeError** si al menos un parametro no es un grafo
            -   **OperacionGrafosInvalida** si los tipos de los vertices y las aristas de ambos grafos no son los mismos
        """
        Grafo.validarGrafo(grafo1)
        Grafo.validarGrafo(grafo2)

        validarCondicion(grafo1.getTipoVertice() is not grafo2.getTipoVertice(), 
                         "Ingresa dos grafos con el mismo tipo de vertices", OperacionGrafosInvalida)
        validarCondicion(grafo1.getTipoArista()  is not grafo2.getTipoArista(), 
                         "Ingresa dos grafos con el mismo tipo de aristas", OperacionGrafosInvalida)

    @staticmethod
    def union(grafo1:Grafo[V,E],grafo2:Grafo[V,E]) -> Grafo[V,E]:
        """Dado dos grafos, devuelve la union entre los dos grafos
        
        **parameters**
            -   grafo1 (Grafo[V,E])
            -   grafo2 (Grafo[V,E])

        **excepciones**
            -   **TypeError**: Si alguno de los parametros ingresados no es un grafo
            -   **OperacionGrafosInvalida**: si los grafos ingresados no tienen el mismo tipo de Vertice o Arista
        """
        Grafo.validarOperacionDeGrafo(grafo1, grafo2)

        grafo = Grafo(grafo1.getTipoVertice(),grafo1.getTipoArista())
        grafo.__cargarConexion(grafo1)
        grafo.__cargarConexion(grafo2)
        
        return grafo
        
    @staticmethod
    def ensamblar(grafo1:Grafo[V,E],grafo2:Grafo[V,E]) -> Grafo[V,E]:
        """Dado dos grafos, devuelve un grafo ensamblado de los dos grafos anteriores. 
        Es decir, que cada vertice de un grafo, esta conectado cada vertice del otro grafo
        
        **parameters**
            -   grafo1 (Grafo[V,E])
            -   grafo2 (Grafo[V,E])

        **excepciones**
            -   **TypeError**: Si alguno de los parametros ingresados no es un grafo
            -   **OperacionGrafosInvalida**: si los grafos ingresados no tienen el mismo tipo de Vertice o Arista
        """
        grafo = Grafo.union(grafo1, grafo2)
    
        for vertice1 in grafo1:
            for vertice2 in grafo2:
                if not grafo.estaConectado(vertice1, vertice2):
                    grafo.conectarVertices(vertice1, vertice2)

        return grafo
    
    @staticmethod
    def generarGrafoInconexo(vertices:set[V], tipoAristas:type = None) -> Grafo[V,E]:
        """Dado un conjunto de vertices, genera un grafo inconexo, 
        es decir, un grafo cuyos vertices no estan conectados
        
        **parameters**
            -   vertices (set[V]): no vacío
            -   tipoAristas (E): por defecto None

        **return**
            -   (Grafo[V,E]): grafo inconexo

        **excepciones**
            -   **TypeError**: si lo que se ingreso no fue un conjunto o si alguno de los elementos tiene un tipo de dato distinto
            -   **VacioError**: si el conjunto está vacío
        """
        validarTipoObjeto(set, vertices, "Ingresa un set de datos")
        validarValorCompatible(len(vertices),0,"Ingrese un set no vacio", VacioError)
        tipo = ValidarTipoUnico(vertices)

        inconexo = Grafo(tipo, tipoAristas)

        for elemento in vertices:
            inconexo.agregarVertice(elemento)

        return inconexo
    
    @staticmethod
    def generarGrafoPath(vertices:set[V], datoAristaInicial:E = None): 
        """Dado un conjunto de vertices, genera un grafo path, 
        es decir, un grafo cuyos vertices forman un camino con principio y fin
        
        **parameters**
            -   vertices (set[V]): no vacío

        **return**
            -   (Grafo[V]): grafo path

        **excepciones**
            -   **TypeError**: si lo que se ingreso no fue un conjunto o si alguno de los elementos tiene un tipo de dato distinto
            -   **VacioError**: si el conjunto está vacío
        """
        if datoAristaInicial is not None: tipoArista = type(datoAristaInicial)
        else:   tipoArista = None

        path = Grafo.generarGrafoInconexo(vertices, tipoArista)

        anterior = None
        for vertice in path:
            if anterior is not None:
                path.conectarVertices(vertice, anterior, datoAristaInicial)

            anterior = vertice

        return path

    @staticmethod
    def generarGrafoCircuito(vertices:set[V], datoAristaInicial:E = None): 
        """Dado un conjunto de vertices, genera un grafo circuito, 
        es decir, un grafo cuyos vertices forman un camino euleriano hamiltoniano (un ciclo cerrado)
        
        **parameters**
            -   vertices (set[V]): no vacío

        **return**
            -   (Grafo[V]): grafo circuito

        **excepciones**
            -   **TypeError**: si lo que se ingreso no fue un conjunto o si alguno de los elementos tiene un tipo de dato distinto
            -   **VacioError**: si el conjunto está vacío
        """
        if datoAristaInicial is not None: tipoArista = type(datoAristaInicial)
        else:   tipoArista = None
        circuito = Grafo.generarGrafoInconexo(vertices, tipoArista)
        
        primero = None
        anterior = None
        for vertice in circuito:
            if anterior is not None:
                circuito.conectarVertices(vertice, anterior,datoAristaInicial)
            else: primero = vertice

            anterior = vertice

        circuito.conectarVertices(vertice,primero, datoAristaInicial)

        return circuito

    @staticmethod
    def generarGrafoCompleto(vertices:set[V], datoAristaInicial:E = None):
        """Dado un conjunto de vertices, genera un grafo completo, 
        es decir, un grafo donde cada vertice estan conectados con todos los demas vertices
        
        **parameters**
            -   vertices (set[V]): no vacío

        **return**
            -   (Grafo[V]): grafo completo

        **excepciones**
            -   **TypeError**: si lo que se ingreso no fue un conjunto o si alguno de los elementos tiene un tipo de dato distinto
            -   **VacioError**: si el conjunto está vacío
        """
        if datoAristaInicial is not None: tipoArista = type(datoAristaInicial)
        else:   tipoArista = None
        completo = Grafo.generarGrafoInconexo(vertices, tipoArista)

        for vertice1 in completo:
            for vertice2 in completo:
                if (vertice1 != vertice2) and not completo.estaConectado(vertice1,vertice2):
                    completo.conectarVertices(vertice1,vertice2,datoAristaInicial)

        return completo



    #GETTERS

    #internos
    def getAdyacencia(self, vertice1:V, vertice2:V) -> E:
        """Dado dos vertices conectados, devueve e dato almacenado en la arista
        
        **parameters**
            -   vertice1 (V)
            -   vertice2 (V)

        **return**
            -   (E) elemento almacenado en la arista correspondiente
        """
        return self.__aristas.getItem(
            self.__indiceVertice(vertice1),
            self.__indiceVertice(vertice2)
        )
    
    #Calculables
    def getCantidadVertices(self) -> int:
        """Obtiene la cantidad de vertices
        
        **return**
            -   (int) la cantidad de vertices del grafo
        """
        return len(self.__vertices)

    def getCantidadAristas(self) -> int:
        """Obtiene la cantidad de Aristas.
        Usa la formula 2|E| = sum(grado(v)) donde v es cada vertice y E son las aristaas
        
        **return**
            -   (int) la cantidad de atistas del grafo
        """
        vertices = 0

        for vertice in self.__vertices:
            vertices += self.getGradoVertice(vertice)

        return vertices // 2

    def getCantidadCaras(self) -> int:
        """Obtiene la cantidad de Caras... si el grafo es planar, si no lo es directamente devuelve cero
        Usando la formula de Euler |F| + |V| - |E| = 2

        **return**
            -   (int) cantidad de caras
        """
        if self.esPlanar():
            return 2 + self.getCantidadAristas() - self.getCantidadCaras()
        else: return 0

    def getGradoVertice(self, vertice:V) -> int:
        """Dado un vertice, retorna el grado del vertice. Osea, a cuantas aristas salen del vertice
        
        **parameters**
            -   vertice (V): pertenece al grafo
        
        **return**
            -   (int) cantidad de aristas que salen del vertice

        **excepciones**
            -   **TypeError**: si el vertice no es del tipo ingresado V
            -   **VerticeNoEncontradoError**: si el vertice no pertenece al grafo
        """
        self.__validarVertice(vertice)
        indice = self.__indiceVertice(vertice)
        grado = 0

        for adyacencia in self.__adyacencia[indice]:    
            grado += adyacencia
        
        return grado

    #Atributos
    def getVertices(self) -> set[V]:
        """Obtiene un conjuntos con todos los vertices del grafo
        
        **return**
            -   (set[V]) conjunto de vertices del grafo
        """
        vertices = set({})
        for vertice in self.__vertices:
            vertices.add(vertice)

        return vertices
    
    def getTipoVertice(self) -> type:
        """Obtiene el tipo de vertices
        
        **return**
            -   (type) tipo V
        """
        return self.__tipoV.getType()
    
    def getTipoArista(self) -> type:
        """Obtiene el tipo de aristas
        
        **return**
            -   (type) tipo E
        """
        return self.__tipoE.getType()

   #SETTERS
    def __setTiposDatos(self, tipoVertices:type, tipoAristas:type = None):
        """Setea el tipo de datos del vertices y aristas
        
        **parameters**
            -   tipoVertices (type): tipo V
            -   tipoAristas (type): tipo E, por defecto None

        **excepciones**
            -   **TypeError** si alguno de los tipos ingresados no es type
        """
        self.__tipoV = TypeStruct(tipoVertices)
        self.__tipoE = TypeStruct(tipoAristas)

    
    #RECORRER GRAFO 
    def mapearGrafo(self, inicio:V) -> Vector[V]:
        """Mapea el grafo y devuelve un vector con los vertices en orden de conexidad"""
        self.__validarVertice(inicio)
        vector = self.__vectorDijkstra()
        vector[PRIMERA_POSCICION] = inicio
        vertices = self.getVertices()
        vertices.remove(inicio)
        j = 1

        for i in range(self.getCantidadVertices()-2):
            conexo = False

            for vertice in self:  

                if self.estaConectado(vector[i], vertice):
                    conexo = True 

                if (vertice in vertices): 
                    vector[j] = vertice
                    vertices.remove(vertice)
                    j+=1

            if not conexo:
                vector[j] = vertices.pop()
                j+=1

        return vector

    def __preparativosPrim(self, inicio:V) -> tuple[Grafo[V,E], Vector[V]]:
        arbol = Grafo.generarGrafoInconexo(self.getVertices(), self.getTipoArista())
        vector = self.mapearGrafo(inicio)
        
        return arbol, vector

    def arbolGeneradorMinimo(self, inicio:V) -> Grafo[V,E]:
        self.__validarPeso()
        self.__validarVertice(inicio)
        validarCondicion(not self.esConexo(), "Este Algoritmo funciona solo con grafos conexos", TipoGrafoIncompatible)

        arbol, vertices = self.__preparativosPrim(inicio)

        for i in range(self.getCantidadVertices() - 1):
            conexionesNoPermitidas = []
            j = 0
            while (j < self.getCantidadVertices()):
                pesoMinimo, vertice = None, None
                

    def __vectorDijkstra(self) -> Vector[V]:
        return Vector(self.getTipoVertice(), self.getCantidadVertices())

    def __vectorVisitadosDijsktra(self, inicio, fin) -> Vector[V]:
        vector = self.mapearGrafo()

    def caminoMasCorto(self, inicio:V, fin:V) -> Grafo[V,E]:
        self.__validarVertice(inicio, fin)
        self.__validarPeso()

        camino = Grafo(self.getTipoVertice(),self.getTipoArista())

        visitados = self.__vectorDijkstra()
        noVisitados = self.mapearGrafo(inicio)
        i = 0

    #VISUALIZAR
    def __dibujarGrafo__(self, G:nx.Graph|nx.DiGraph, pos:dict[str, tuple[float, float]], ax:Axes):    
        nx.draw(
            G, pos = pos, ax= ax,
            with_labels=True,
            node_size=1200,
            node_color= "skyblue",
            edge_color= "black",
            font_size= 12,
        )
        if self.esPesado():
            nx.draw_networkx_edge_labels(G, pos, edge_labels= self.__etiquetarAristas__(), ax= ax)

    def __redibujar(self, G:nx.Graph, pos:dict[str, tuple[float, float]], ax:Axes,xLim:tuple[float, float], yLim:tuple[float, float]):
        ax.cla()
        self.__dibujarGrafo__(G, pos, ax)
        ax.set_xlim(min(xLim) - MARGEN, max(xLim) + MARGEN)
        ax.set_ylim(min(yLim) - MARGEN, max(yLim) + MARGEN)
        ax.figure.canvas.draw_idle()

    def __etiquetarAristas__(self):
        etiquetas = {}

        for vertice1 in self:
            for vertice2 in self:
                if (self.estaConectado(vertice1, vertice2) and (vertice2, vertice1) not in etiquetas):
                    etiquetas.update({(vertice1, vertice2):self.getAdyacencia(vertice1, vertice2)})
        
        return etiquetas
    

    def __registrarAristas__(self, G:nx.Graph):        
        for vertice1 in self.__vertices:
            G.add_node(vertice1)
            for vertice2 in self.__vertices:
                if self.estaConectado(vertice1, vertice2) and (vertice2, vertice1):
                    G.add_edge(vertice1,vertice2)

    def __distanciaEuleriana(self,x1:float, y1:float, x2:float, y2:float) -> float:
        return ((x1-x2)**2 + (y1-y2)**2)**(1/2)

    def __calcularDistanciaNodo(self,pos:dict[str, tuple[float, float]], xCord:float, yCord:float) -> float:
        for nodo in pos:
            xPos, yPos = pos[nodo]
            if None not in (xCord,yCord):
                if self.__distanciaEuleriana(xPos,yPos,xCord, yCord) <= DISTANCIA_ACEPTADA:
                    return nodo
                
        return None
        
    def __onPress(self,evento:MouseEvent, pos:dict[str, float]):
        global nodoSeleccionado
        nodoSeleccionado = self.__calcularDistanciaNodo(pos, evento.xdata, evento.ydata)

    def __onMove(self, evento:MouseEvent, G:nx.Graph, pos:dict[str, tuple[float, float]], ax:Axes, 
            xLim:tuple[float, float], yLim:tuple[float, float]):
        global nodoSeleccionado
        coordenadas = (evento.xdata,evento.ydata)

        if (nodoSeleccionado is not None) and (None not in coordenadas):
            pos[nodoSeleccionado] = coordenadas

        self.__redibujar(G, pos, ax, xLim, yLim)

    def __onRelease(self,evento:MouseEvent):
        global nodoSeleccionado
        nodoSeleccionado = None

    def __crearGrafoNx__(self):
        return nx.Graph()

    def visualizar(self):

        G = self.__crearGrafoNx__()

        self.__registrarAristas__(G)

        fig, ax = plt.subplots()

        pos = nx.spring_layout(G)

        xLim = [x for x, y in pos.values()]
        yLim = [y for x, y in pos.values()]
        
        ax.set_autoscale_on(False)
        ax.set_xlim(min(xLim) - MARGEN, max(xLim) + MARGEN)
        ax.set_ylim(min(yLim) - MARGEN, max(yLim) + MARGEN)

        fig.canvas.mpl_connect("button_press_event", lambda evento: self.__onPress(evento, pos))
        fig.canvas.mpl_connect("motion_notify_event", lambda evento: self.__onMove(evento, G, pos, ax, xLim, yLim))
        fig.canvas.mpl_connect("button_release_event", self.__onRelease)
        
        self.__dibujarGrafo__(G, pos, ax)

        plt.show()



#Digrafo ------------------------------------------------------------------------------------------------------
class Digrafo(Grafo,Generic[V,E]):
    #CONSTRUCTOR
    def __init__(self, tipoVertices:V, tipoAristas:E = None):
        """Construye un digrafo dado un tipo de vertices
        
        **parameters**
            -   tipoVertices (type)
            -   tipoAristas (type): por default None. Setea un tipo de dato para almacenar cosas en las aristas de los grafos
            -   pesado (bool): por default False. Si es True, el grafo será un grafo pesado.  

        **excepciones**
            -   **TypeError**: Si ninguno de los datos ingresados es del tipo correspondiente  
        """
        super().__init__(tipoVertices, tipoAristas)
        
    #METODOS DE CLASE

    def conectarVertices(self, vertice1, vertice2, coneccion = None):
        super().__conectarVertices__(vertice1, vertice2, ADYAENCIA, coneccion)

    def desconectarVertices(self, vertice1, vertice2):
        super().__conectarVertices__(vertice1, vertice2, SIN_ADYACENCIA, None)

    #GETTERS
    
    def getGrafoSuyacente(self) -> Grafo[V,E]:
        """Retorna el grafo que sería el digrafo si no estuviera orientado
        
        **return**
            -   (Grafo[V,E]) el digrafo sin direcciones
        """
        grafo = Grafo.generarGrafoInconexo(self.getVertices()) 

        for vertice1 in self.getVertices():
            for vertice2 in self.getVertices():
                if self.estaConectado(vertice1, vertice2):
                    grafo.conectarVertices(vertice1, vertice2)

        return grafo
    
    #VISUALIZACION

    def __crearGrafoNx__(self):
        return nx.DiGraph()
    
    def __registrarAristas__(self, G:nx.DiGraph):
        for vertice1 in self:
            G.add_node(vertice1)
            for vertice2 in self:
                if self.estaConectado(vertice1, vertice2):
                    G.add_edge(vertice1,vertice2)
        
    def __dibujarGrafo__(self, G, pos, ax):
        nx.draw(
            G, pos = pos, ax= ax,
            with_labels=True,
            node_size=1200,
            node_color= "skyblue",
            edge_color= "black",
            font_size= 12,
            arrows = True,
        )
        if self.esPesado():
            nx.draw_networkx_edge_labels(G, pos, edge_labels= self.__etiquetarAristas__(), ax= ax)

    
    def __etiquetarAristas__(self):
        etiquetas = {}

        for vertice1 in self:
            for vertice2 in self:
                if (self.estaConectado(vertice1, vertice2)):
                    etiquetas.update({(vertice1, vertice2):self.getAdyacencia(vertice1, vertice2)})
        
        return etiquetas
    
