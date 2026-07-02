from .Validaciones import (TypeStruct, DataStruct, TypeVar, Generic, ValidarTipoUnico, validarValorCompatible, 
                           validarCondicion, validarTipoObjeto, validarNoNegativo)
from .Excepciones.Grafo import *
from .Excepciones.Generales import VacioError
from .Algebra import Matriz, MatrizAlgebraica, PRIMERA_POSCICION
from typing import Generator, Dict, Tuple, Optional
import matplotlib.pyplot as plt
import networkx as nx

V = TypeVar("V")
E = TypeVar("E")

SIN_ADYACENCIA = 0
ADYAENCIA = 1
ANTIADYACENCIA = -1 

class Cursor(DataStruct, Generic[V]):
    pass

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

    def __validarVertice(self, vertice:V):
        """Valida un vertice para el funcionamiento del grafo
        
        **parameters**
            -   vertice (V): pertenece al grafo
        
        **excepciones**
            -   **TypeError**: si el vertice no es del tipo ingresado V
            -   **VerticeNoEncontradoError**: si el vertice no pertenece al grafo
        """
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
    def generarGrafoInconexo(vertices:set[V]) -> Grafo[V,None]:
        """Dado un conjunto de vertices, genera un grafo inconexo, 
        es decir, un grafo cuyos vertices no estan conectados
        
        **parameters**
            -   vertices (set[V]): no vacío

        **return**
            -   (Grafo[V]): grafo inconexo

        **excepciones**
            -   **TypeError**: si lo que se ingreso no fue un conjunto o si alguno de los elementos tiene un tipo de dato distinto
            -   **VacioError**: si el conjunto está vacío
        """
        validarTipoObjeto(set, vertices, "Ingresa un set de datos")
        validarValorCompatible(len(vertices),0,"Ingrese un set no vacio", VacioError)
        tipo = ValidarTipoUnico(vertices)

        inconexo = Grafo(tipo)

        for elemento in vertices:
            inconexo.agregarVertice(elemento)

        return inconexo
    
    @staticmethod
    def generarGrafoPath(vertices:set[V]): 
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
        path = Grafo.generarGrafoInconexo(vertices)

        anterior = None
        for vertice in path:
            if anterior is not None:
                path.conectarVertices(vertice, anterior)

            anterior = vertice

        return path

    @staticmethod
    def generarGrafoCircuito(vertices:set[V]): 
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
        circuito = Grafo.generarGrafoInconexo(vertices)

        primero = None
        anterior = None
        for vertice in circuito:
            if anterior is not None:
                circuito.conectarVertices(vertice, anterior)
            else: primero = vertice

            anterior = vertice

        circuito.conectarVertices(vertice,primero)

        return circuito

    @staticmethod
    def generarGrafoCompleto(vertices:set[V]):
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
        completo = Grafo.generarGrafoInconexo(vertices)

        for vertice1 in completo:
            for vertice2 in completo:
                if (vertice1 != vertice2) and not completo.estaConectado(vertice1,vertice2):
                    completo.conectarVertices(vertice1,vertice2)

        return completo



    #GETTERS

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

    #VISUALIZAR
    def visualizar(self):
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
        except Exception:
            raise ImportError("Instale networkx y matplotlib para usar este metodo") 

        G = nx.Graph()
        
        self.__crearVisuales(G)
        pos = nx.spring_layout(G)

        nx.draw(
            G, pos,
            with_labels= True,
            node_color="#04cec4", node_size=1500,
            edge_color="#000000"
        )
        
        plt.show()

    def __crearVisuales(self, visual:nx.Graph):
        for vertice in self:
            visual.add_node(vertice)
        visual.add_edges_from(self.__visualizarConexiones(visual))

    def __visualizarConexiones(self,visual:nx.Graph):
        conexiones = {}

        for vertice1 in self:
            for vertice2 in self:
                if self.estaConectado(vertice1,vertice2) and ((vertice2, vertice1) not in conexiones.keys()):
                    conexiones.update(
                        {(vertice1,vertice2):self.__etiquetaArista(vertice1,vertice2)}
                    )

        return conexiones 

    #lo hecho por la IA
    def verGrafo(self, tamanioVertices: int = 1800, mostrar: bool = True) -> None:
        """Genera y muestra una visualización interactiva del grafo.

        Args:
            tamanioVertices (int): Tamaño de los nodos en la visualización.
            mostrar (bool): Si es True, muestra la ventana. Si es False, solo prepara la figura.
        """
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
        except Exception as error:
            raise ImportError("Instale networkx y matplotlib para usar este metodo") from error

        self.__crearVisualizacion(tamanioVertices)
        self.__dibujarVisualizacion()
        self.__configurarInteraccion()

        if mostrar:
            plt.show()

    def __crearVisualizacion(self, tamanioVertices: int) -> None:
        """Prepara la estructura interna necesaria para dibujar el grafo."""
        self.__tamanioVertices = tamanioVertices
        self.__grafoVisualizacion = nx.Graph()
        self.__grafoVisualizacion.add_nodes_from(self.getVertices())
        self.__etiquetasAristas: Dict[Tuple[V, V], str] = {}

        for vertice1 in self:
            for vertice2 in self:
                if self.estaConectado(vertice1, vertice2) and ((vertice2, vertice1) not in self.__grafoVisualizacion.edges):
                    self.__grafoVisualizacion.add_edge(vertice1, vertice2)
                    self.__etiquetasAristas[(vertice1, vertice2)] = self.__etiquetaArista(vertice1, vertice2)

        self.__posicionVisualizacion: Dict[V, Tuple[float, float]] = {}
        posiciones = nx.circular_layout(self.__grafoVisualizacion, scale=1.2)
        for vertice in self:
            self.__posicionVisualizacion[vertice] = posiciones[vertice]

    def __dibujarVisualizacion(self) -> None:
        """Dibuja el grafo en una ventana de Matplotlib."""
        self.__figura, self.__eje = plt.subplots()
        self.__eje.clear()
        nx.draw(
            self.__grafoVisualizacion,
            pos=self.__posicionVisualizacion,
            with_labels=True,
            node_size=self.__tamanioVertices,
            node_color="#4bd5e7",
            edge_color="#000000",
            width=1.5,
            ax=self.__eje,
        )

        if self.__etiquetasAristas:
            nx.draw_networkx_edge_labels(
                self.__grafoVisualizacion,
                pos=self.__posicionVisualizacion,
                edge_labels=self.__etiquetasAristas,
                ax=self.__eje,
                font_size=9,
            )

        self.__eje.set_title("Grafo")
        self.__figura.canvas.draw_idle()

    def __configurarInteraccion(self) -> None:
        """Registra los eventos de ratón para permitir mover los nodos."""
        self.__nodoSeleccionado: Optional[V] = None
        self.__figura.canvas.mpl_connect("button_press_event", self.__alHacerClick)
        self.__figura.canvas.mpl_connect("motion_notify_event", self.__alMoverRaton)
        self.__figura.canvas.mpl_connect("button_release_event", self.__alSoltarClick)

    def __alHacerClick(self, evento: object) -> None:
        """Selecciona un nodo cuando el usuario hace clic sobre él."""
        if getattr(evento, "inaxes", None) is None:
            return
        if getattr(evento, "xdata", None) is None or getattr(evento, "ydata", None) is None:
            return

        for nodo, posicion in self.__posicionVisualizacion.items():
            distancia = (evento.xdata - posicion[0]) ** 2 + (evento.ydata - posicion[1]) ** 2
            if distancia < 0.1:
                self.__nodoSeleccionado = nodo
                return

        self.__nodoSeleccionado = None

    def __alMoverRaton(self, evento: object) -> None:
        """Actualiza la posición del nodo seleccionado mientras se arrastra."""
        if self.__nodoSeleccionado is None:
            return
        if getattr(evento, "inaxes", None) is None:
            return
        if getattr(evento, "xdata", None) is None or getattr(evento, "ydata", None) is None:
            return

        self.__posicionVisualizacion[self.__nodoSeleccionado] = (evento.xdata, evento.ydata)
        self.__eje.clear()
        nx.draw(
            self.__grafoVisualizacion,
            pos=self.__posicionVisualizacion,
            with_labels=True,
            node_size=self.__tamanioVertices,
            node_color="#4bd5e7",
            edge_color="#000000",
            width=1.5,
            ax=self.__eje,
        )

        if self.__etiquetasAristas:
            nx.draw_networkx_edge_labels(
                self.__grafoVisualizacion,
                pos=self.__posicionVisualizacion,
                edge_labels=self.__etiquetasAristas,
                ax=self.__eje,
                font_size=9,
            )

        self.__eje.set_title("Grafo")
        self.__figura.canvas.draw_idle()

    def __alSoltarClick(self, evento: object) -> None:
        """Deselecciona el nodo cuando el usuario suelta el botón del ratón."""
        self.__nodoSeleccionado = None

    def __etiquetaArista(self, vertice1: V, vertice2: V) -> str:
        """Devuelve la etiqueta visible para una arista.

        Si la arista tiene datos asociados, se muestran como texto. Si no,
        se devuelve una cadena vacía para no mostrar nada.
        """
        
        if not self.esPesado():
            return ""

        dato = self.__aristas.getItem(
            self.__indiceVertice(vertice1),
            self.__indiceVertice(vertice2)
        )

        return str(dato)


 

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

    def conectarVertices(self, vertice1, vertice2, coneccion = None, peso = None):
        super().__conectarVertices__(vertice1, vertice2, ADYAENCIA, coneccion, peso)

    def desconectarVertices(self, vertice1, vertice2):
        super().__conectarVertices__(vertice1, vertice2, SIN_ADYACENCIA, None, SIN_ADYACENCIA)

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