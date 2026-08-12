from .Heredables import TypeStruct, DataStruct, Generic, T
from .Validaciones import validarTipoObjeto, validarCondicion
from .Vector import Vector
from .Excepciones.Generales import ElementoNoEncontrado


#SEMILLA -------------------------------------------------------------------------------------------------------------
class SemillaBin(DataStruct, Generic[T]):
    """# SEMILLA BINARIA
    
    Hecha para crear arboles binarios
    No hay mucho misterio
    """
    #ATRIBUTOS
    __izquierda:SemillaBin[T]
    __derecha:SemillaBin[T]

    #CONSTRUCTOR
    def __init__(self, tipo:type, dato:T):
        """Dado un tipo de dato y un dato, crea una semilla binaria sin hijos
        
        **parameters**
            -   tipo (type)
            -   dato (T)

        **excepciones**
            -   **TypeError** si el parametro del tipo T no es type o el dato ingresado no es del tipo ingresado T
        """
        super().__init__(tipo, dato, False)
        self.setIzquierda(None)
        self.setDerecha(None)

    #METODOS DE CLASE
    def tieneHijoIzq(self) -> bool:
        """Verifica que la semilla tenga hijo izquierdo
        
        **return**
            -   (bool) Verdadero si el hijo izquierdo no es None, falso si sí
        """
        return self.getIzquierda() is not None

    def tieneHijoDer(self) -> bool:
        """Verifica que la semilla tenga hijo derecho
        
        **return**
            -   (bool) Verdadero si el hijo derecho no es None, falso si sí
        """
        return self.getDerecha() is not None

    def tieneHijos(self) -> bool:
        """Verifica que la semilla tenga hijos
        
        **return**
            -   (bool) Verdadero si la semilla tiene al menos un hijo, falso si no tiene ninguno
        """
        return self.tieneHijoDer() or self.tieneHijoIzq()

    def tieneAmbosHijos(self) -> bool:
        """Verifica que la semilla tenga ambos hijos
        
        **return**
            -   (bool) Verdadero si tiene los dos hijos, falso si no tiene al menos uno
        """
        return self.tieneHijoIzq() and self.tieneHijoDer()

    def desconectar(self):
        """Desconecta la semillas hijas de esta semilla"""
        self.setIzquierda(None)
        self.setDerecha(None)

    #VALIDACIONES
    @staticmethod
    def validarSemilla(semilla:SemillaBin):
        """Valida que una semilla sea una semilla
        
        **parameters**
            -   semilla (SemillaBin): puede ser None

        **excepciones**
            -   **TypeError**: si el parametro ingresado no es una semiila**
        """
        if semilla is not None:
            validarTipoObjeto(SemillaBin, semilla, "Ingresa una semilla")

    @staticmethod
    def validarTiposSemilla(semilla1:SemillaBin, semilla2:SemillaBin):
        SemillaBin.validarSemilla(semilla1)
        SemillaBin.validarSemilla(semilla2)
        validarCondicion(issubclass(semilla1.getType(), semilla2.getType()) or issubclass(semilla2.getType(), semilla1.getType()),
                         "Ingresa dos semillas con el mismo tipo de Dato", TypeError)
        
    #METODOS ESTATICOS
    @staticmethod
    def intercambiarDatos(semilla1:SemillaBin, semilla2:SemillaBin):
        SemillaBin.validarTiposSemilla(semilla1, semilla2)

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

    def getCantidadDescendientes(self) -> int:
        if not self.tieneHijos():
            return 0
        if self.tieneAmbosHijos():
            return 2 + self.getDerecha().getCantidadDescendientes() + self.getIzquierda().getCantidadDescendientes()
        return 1+self.getUnicoHijo().getCantidadDescendientes()

    def getUnicoHijo(self) -> SemillaBin[T]:
        validarCondicion(self.tieneAmbosHijos() or not self.tieneHijos(), 
                         "Este metodo funciona solo si la semilla tiene solamente un hijo")
        if self.tieneHijoDer(): return self.getDerecha()
        else: return self.getIzquierda()

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
    __cantidadElementos:int

    #CONSTRUCTOR
    def __init__(self, tipo:type, metodo:function = None):
        super().__init__(tipo)

        self.__setMetodo(metodo)
        self.__setRaiz(None)
        self.__iniciarConteo()

    #METODOS GENERALES
    def __iter__(self):
        yield from self.__recorridoIterativo(self.__getRaiz())

    #METODOS DE CLASE
    def estaElItem(self, item:T) -> bool:
        return self.__buscar(item, self.__getRaiz())
    
    def estaEquilibrado(self) -> bool:
        return self.__getRaiz().getEquilibrio() == 0

    def estaVacio(self) -> bool:
        return self.getCantidadElementos() == 0

    def agregar(self, item:T):
        self.__validarEntrada__(item)

        if self.estaVacio():
            self.__setRaiz(self.__generarSemilla(item))
        else:
            self.__insertarDato(item, self.__getRaiz())
        
        self.__agregarItem()
        

    def remover(self, item:T):
        self.__validarEntrada__(item)
        self.__quitarItem()

    def mapear(self) -> Vector[T]:
        vector = Vector(self.getType(), self.getCantidadElementos()) 
        lista = []
        self.__recorrerArbol(self.__getRaiz(), lista)

        for i in range(self.getCantidadElementos()):
            vector[i] = lista[i]

        return vector


    #METODOS INTERNOS
    def __buscar(self, item:T, semilla:SemillaBin[T]) -> bool:
        if semilla == None:
            return False

        if item == semilla.getDato():
            return True

        if self.__menorIgual(item, semilla.getDato()):
            return self.__buscar(item, semilla.getIzquierda())

        return self.__buscar(item, semilla.getDerecha())
            
    def __generarSemilla(self, dato:T) -> SemillaBin[T]:
        return SemillaBin(self.getType(), dato)

    def __colocarDato(self, item:T, semilla:SemillaBin[T]):
        insercion = self.__generarSemilla(item)

        if self.__menorIgual(item, semilla.getDato()):
            semilla.setIzquierda(insercion)
        else:
            semilla.setDerecha(insercion)

    def __seleccionarHijo(self, item:T, semilla:SemillaBin[T]) -> SemillaBin[T]:
        if self.__menorIgual(item, semilla.getDato()):
            return semilla.getIzquierda()
        else:
            return semilla.getDerecha()

    def __colocarIzq(self, item:T, semilla:SemillaBin[T]):
        if semilla.getIzquierda() is not None:
            self.__insertarDato(item, semilla.getIzquierda())
        else:
            semilla.setIzquierda(self.__generarSemilla(item))
    
    def __colocarDer(self, item:T, semilla:SemillaBin[T]):
        if semilla.getDerecha() is not None:
            self.__insertarDato(item, semilla.getDerecha())
        else:
            semilla.setDerecha(self.__generarSemilla(item))

    def __insertarDato(self, item:T, semilla:SemillaBin[T]):
        if item == semilla.getDato():
            self.__quitarItem()
        elif semilla.tieneAmbosHijos():
            self.__insertarDato(item, self.__seleccionarHijo(item, semilla))
        elif not semilla.tieneHijos():
            self.__colocarDato(item, semilla)
        elif self.__menorIgual(item, semilla.getDato()):
            self.__colocarIzq(item, semilla)
        else:
            self.__colocarDer(item, semilla)

    def __recorrerArbol(self, semilla:SemillaBin[T], lista:list):
        if semilla.getIzquierda() is not None:
            self.__recorrerArbol(semilla.getIzquierda(),lista)

        lista.append(semilla.getDato())

        if semilla.getDerecha() is not None:
            self.__recorrerArbol(semilla.getDerecha(),lista)

    def __recorridoIterativo(self, semilla:SemillaBin[T]):
        yield semilla.getDato()

        if semilla.tieneHijoIzq():yield from self.__recorridoIterativo(semilla.getIzquierda())
        if semilla.tieneHijoDer():yield from self.__recorridoIterativo(semilla.getDerecha())


    def __iniciarConteo(self):
        self.__cantidadElementos = 0

    def __agregarItem(self):
        self.__cantidadElementos +=1

    def __quitarItem(self):
        self.__cantidadElementos -=1

    def __estaMasOMenosEquilibrado(self) -> bool:
        return self.__getRaiz().getEquilibrio() in (-1, 0, 1)

    def __hayMetodo(self) -> bool:
        return self.__ordenamiento is not None

    def __menorIgual(self, item1:T, item2:T) -> bool:
        if self.__hayMetodo(): return self.__metodo(item1) <= self.__metodo(item2)
        return item1 <= item2

    def __metodo(self, entrada:T) -> object:
        return self.__ordenamiento(entrada)

    #VALIDACIONES
    def __buscarSemilla(self, item:T, semilla:SemillaBin[T]) -> SemillaBin[T]: 
        if semilla is None:
            raise ElementoNoEncontrado(f"El objeto ingresado ({item}) no se encuentra almacenado en el árbol")

        if item == semilla.getDato():
            return semilla

        if self.__menorIgual(item, semilla.getDato()):
            return self.__buscarSemilla(item, semilla.getIzquierda())

        return self.__buscarSemilla(item, semilla.getDerecha())
        

    #METODOS ESTATICOS
    @staticmethod
    def union(arbol1:ArbolBin[T], arbol2:ArbolBin[T]) -> ArbolBin[T]:
        union = ArbolBin(arbol1.getType(), arbol1.__ordenamiento)

        for item in arbol1:
            union.agregar(item)

        for item in arbol2:
            union.agregar(item)

        return union

    @staticmethod
    def interseccion(arbol1:ArbolBin[T], arbol2:ArbolBin[T]) -> ArbolBin[T]:
        interseccion = ArbolBin(arbol1.getType(), arbol1.__ordenamiento)

        for item in arbol1:
            if item in arbol2:
                interseccion.agregar(item)

        return interseccion

    
    #GETTERS
    def getCantidadHijos(self, item:T) -> int:
        return self.__buscarSemilla(item,self.__getRaiz()).getCantidadDescendientes()

    def getSubarbol(self, item:T) -> ArbolBin[T]:
        raiz = self.__buscarSemilla(item, self.__getRaiz())
        subarbol = ArbolBin(self.getType())

        subarbol.__setRaiz(raiz)
        subarbol.__cantidadElementos = raiz.getCantidadDescendientes()

        return subarbol

    def __getRaiz(self) -> SemillaBin:
        return self.__raiz

    def getCantidadElementos(self) -> int:
        return self.__cantidadElementos
    
    #SETTERS
    def __setRaiz(self, raiz:SemillaBin):
        if SemillaBin is not None: SemillaBin.validarSemilla(raiz)
        self.__raiz = raiz

    def __setMetodo(self, metodo:function):
        if metodo is not None:validarCondicion(callable(metodo))
        self.__ordenamiento = metodo        