from .Validaciones import TypeStruct, DataStruct, TypeVar, Generic, validarValorCompatible, validarCondicion, validarRango, validarTipoObjeto, validarNoNegativo, Enum
from .Excepciones.Grafo import *
from typing import Generator

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
        """Dado un vertice del grafo, lo elimina
        
        **parameters**
            -   vertice (V): Tiene que estar en el grafo

        **excepciones**
            -   **TypeError** si la entrada no es un objeto del tipo ingresado V+
            -   **VerticeNoEncontradoError** si el vertice no es parte del grafo
        """
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

        self.__conectarVertices(vertice1, vertice2, SIN_ADYACENCIA, None, SIN_ADYACENCIA)
        self.__conectarVertices(vertice2, vertice1, SIN_ADYACENCIA, None, SIN_ADYACENCIA)


    #METODOS INTERNOS

    def __actualizarMatriz(self, matriz:list[list[int]], dato:int|E):
        """"""
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

    
    def __cargarConexion(self, grafoDonante:Grafo[V,E]):
        for vertice in grafoDonante:
            self.agregarVertice(vertice)

        for vertice1 in grafoDonante:
            for vertice2 in grafoDonante:
                if grafoDonante.estaConectado(vertice1,vertice2) and not self.estaConectado(vertice1, vertice2):
                    self.conectarVertices(vertice1, vertice2)


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

    #CURSOR
    class Cursor:
        __dato:V


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
        Grafo.validarOperacionDeGrafo(grafo1, grafo2)

        grafo = Grafo(grafo1.getTipoVertice(),grafo1.getTipoArista())
        grafo.__cargarConexion(grafo1)
        grafo.__cargarConexion(grafo2)
        
        return grafo
        
    @staticmethod
    def ensamblar(grafo1:Grafo[V,E],grafo2:Grafo[V,E]) -> Grafo[V,E]:
        grafo = Grafo.union(grafo1, grafo2)
    
        for vertice1 in grafo1:
            for vertice2 in grafo2:
                if not grafo.estaConectado(vertice1, vertice2):
                    grafo.conectarVertices(vertice1, vertice2)

        return grafo

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

    def visualizar(self, titulo: str = None, mostrar_pesos: bool = True, mostrar_nombres: bool = True, figsize: tuple[int, int] = (8, 6), font_size: int = 12):
        """Muestra una visualización del grafo usando matplotlib. """
        try:
            import matplotlib.pyplot as plt
        except ImportError as error:
            raise ImportError("matplotlib no está instalado. Instale matplotlib para visualizar el grafo.") from error

        try:
            import networkx as nx
        except ImportError:
            nx = None

        vertices = list(self.__vertices.keys())
        if len(vertices) == 0:
            raise ValueError("El grafo no tiene vertices para visualizar.")

        dirigido = isinstance(self, Digrafo)
        titulo = titulo or ("Digrafo" if dirigido else "Grafo")

        def obtener_etiqueta_origen_destino(origen, destino):
            origen_indice = self.__indiceVertice(origen)
            destino_indice = self.__indiceVertice(destino)
            etiqueta = None
            if self.__aristas[origen_indice][destino_indice] is not None:
                etiqueta = str(self.__aristas[origen_indice][destino_indice])
            if self.esPesado() and mostrar_pesos:
                peso = self.__pesos[origen_indice][destino_indice]
                if etiqueta is None:
                    etiqueta = str(peso)
                else:
                    etiqueta = f"{etiqueta} ({peso})"
            return etiqueta

        if nx is not None:
            grafo = nx.DiGraph() if dirigido else nx.Graph()
            grafo.add_nodes_from(vertices)
            edge_labels = {}

            for i, origen in enumerate(vertices):
                for j, destino in enumerate(vertices):
                    if not dirigido and j <= i:
                        continue
                    if self.estaConectado(origen, destino):
                        etiqueta = obtener_etiqueta_origen_destino(origen, destino)
                        grafo.add_edge(origen, destino)
                        if etiqueta is not None:
                            edge_labels[(origen, destino)] = etiqueta

            pos = nx.spring_layout(grafo)
            fig, ax = plt.subplots(figsize=figsize)
            ax.set_title(titulo)
            ax.axis("off")

            edges = nx.draw_networkx_edges(grafo, pos, ax=ax, edge_color="gray", arrows=dirigido)
            nodes = nx.draw_networkx_nodes(grafo, pos, ax=ax, node_color="skyblue", node_size=700)
            labels = nx.draw_networkx_labels(grafo, pos, ax=ax, font_size=font_size) if mostrar_nombres else {}
            edge_labels_artists = {}
            if edge_labels:
                edge_labels_artists = nx.draw_networkx_edge_labels(
                    grafo,
                    pos,
                    edge_labels=edge_labels,
                    ax=ax,
                    font_color="red",
                    font_size=max(font_size - 2, 8),
                )

            class NodoArrastrable:
                def __init__(self, grafo, pos, nodes, labels, edges, edge_labels):
                    self.grafo = grafo
                    self.pos = pos
                    self.nodes = nodes
                    self.labels = labels
                    self.edges = edges
                    self.edge_labels = edge_labels
                    self.selected = None

                def _distancia(self, p1, p2):
                    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

                def presionar(self, event):
                    if event.inaxes != ax or event.xdata is None or event.ydata is None:
                        return
                    click = (event.xdata, event.ydata)
                    mejor = None
                    mejor_dist = float("inf")
                    for nodo, coords in self.pos.items():
                        d = self._distancia(coords, click)
                        if d < mejor_dist:
                            mejor_dist = d
                            mejor = nodo
                    if mejor is not None and mejor_dist < 0.02:
                        self.selected = mejor

                def mover(self, event):
                    if self.selected is None or event.inaxes != ax or event.xdata is None or event.ydata is None:
                        return
                    self.pos[self.selected] = (event.xdata, event.ydata)
                    offsets = [self.pos[nodo] for nodo in self.grafo.nodes()]
                    self.nodes.set_offsets(offsets)
                    if mostrar_nombres:
                        for nodo, texto in self.labels.items():
                            x, y = self.pos[nodo]
                            texto.set_position((x, y))
                    if isinstance(self.edges, (list, tuple)):
                        for idx, arco in enumerate(self.edges):
                            if hasattr(arco, "set_positions"):
                                u, v = list(self.grafo.edges())[idx]
                                arco.set_positions(self.pos[u], self.pos[v])
                    else:
                        segmentos = []
                        for u, v in self.grafo.edges():
                            x1, y1 = self.pos[u]
                            x2, y2 = self.pos[v]
                            segmentos.append([(x1, y1), (x2, y2)])
                        self.edges.set_segments(segmentos)
                    for (u, v), texto in self.edge_labels.items():
                        xm, ym = ((self.pos[u][0] + self.pos[v][0]) / 2, (self.pos[u][1] + self.pos[v][1]) / 2)
                        texto.set_position((xm, ym))
                    fig.canvas.draw_idle()

                def soltar(self, event):
                    self.selected = None

            drag = NodoArrastrable(grafo, pos, nodes, labels, edges, edge_labels_artists)
            fig.canvas.mpl_connect("button_press_event", drag.presionar)
            fig.canvas.mpl_connect("motion_notify_event", drag.mover)
            fig.canvas.mpl_connect("button_release_event", drag.soltar)

            plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
            plt.show()
            return

        import math
        from matplotlib import patches

        posiciones = {}
        angulo = 2 * math.pi / len(vertices)
        for i, vertice in enumerate(vertices):
            posiciones[vertice] = (math.cos(i * angulo), math.sin(i * angulo))

        plt.figure(figsize=figsize)
        for vertice, (x, y) in posiciones.items():
            plt.scatter([x], [y], s=500, color="skyblue", zorder=2)
            if mostrar_nombres:
                plt.text(x, y, str(vertice), ha="center", va="center", fontsize=font_size, zorder=3)

        for i, origen in enumerate(vertices):
            for j, destino in enumerate(vertices):
                if not dirigido and j <= i:
                    continue
                if self.estaConectado(origen, destino):
                    x1, y1 = posiciones[origen]
                    x2, y2 = posiciones[destino]
                    etiqueta = obtener_etiqueta_origen_destino(origen, destino)
                    if dirigido:
                        flecha = patches.FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=20, color="gray", linewidth=1.5, shrinkA=15, shrinkB=15)
                        plt.gca().add_patch(flecha)
                    else:
                        plt.plot([x1, x2], [y1, y2], color="gray", linewidth=1.5, zorder=1)
                    if etiqueta is not None:
                        xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
                        plt.text(xm, ym, etiqueta, color="red", fontsize=max(font_size - 2, 8), ha="center", va="center", zorder=4)

        plt.title(titulo)
        plt.axis("off")
        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        plt.show()


    #SETTERS

    def __setTiposDatos(self, tipoVertices:type, tipoAristas:type = None):
        self.__tipoV = TypeStruct(tipoVertices)
        self.__tipoE = TypeStruct(tipoAristas)





#Digrafo ------------------------------------------------------------------------------------------------------
class Digrafo(Grafo,Generic[E,V]):
    #CONSTRUCTOR
    def __init__(self, tipoVertices, tipoAristas = None, pesado = False):
        super().__init__(tipoVertices, tipoAristas, pesado)
        
    #METODOS DE CLASE

    def conectarVertices(self, vertice1, vertice2, coneccion = None, peso = None):
        self.__conectarVertices(vertice1, vertice2, ADYAENCIA, coneccion, peso)

    def desconectarVertices(self, vertice1, vertice2):
        self.__conectarVertices(vertice1, vertice2, SIN_ADYACENCIA, None, SIN_ADYACENCIA)