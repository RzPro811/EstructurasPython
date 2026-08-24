from .__Heredables import TypeStruct, DataStruct, Generic, T
from .__Validaciones import validarTipoObjeto, validarCondicion, filtrarElNulo
from .__Vector import Vector, Generator
from .__Excepciones.Generales import ElementoNoEncontrado


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
    def __init__(self, tipo:type, dato:T) -> SemillaBin:
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
    def intercambiarIzq(self) -> None:
        """Intercambia el dato con las semilla hija izquierda
        
        **excepciones**
            -   **ElementoNoEncontrado**: si esta semilla no tiene hijo izquierdo
        """
        validarCondicion(not self.tieneHijoIzq(), "Esta semilla no tiene hijo izquierdo", ElementoNoEncontrado)
        SemillaBin.intercambiarDatos(self, self.getIzquierda())
    
    def intercambiarDer(self) -> None:
        """Intercambia el dato con las semilla hija derecha

        **excepciones**
            -   **ElementoNoEncontrado**: si esta semilla no tiene hijo derecho
        """
        validarCondicion(not self.tieneHijoDer(), "Esta semilla no tiene hijo derecho", ElementoNoEncontrado)
        SemillaBin.intercambiarDatos(self, self.getDerecha())

    def desconectar(self) -> None:
        """Desconecta la semillas hijas de esta semilla"""
        self.setIzquierda(None)
        self.setDerecha(None)

    def desconectarIzq(self) -> None:
        """Desconecta la semilla a la izquierda"""
        self.setIzquierda(None)

    def desconectarDer(self) -> None:
        """Desconecta la semilla a la derecha"""
        self.setDerecha(None)

    #VALIDACIONES
    @staticmethod
    def validarSemilla(semilla:SemillaBin) -> None:
        """Valida que una semilla sea una semilla
        
        **parameters**
            -   semilla (SemillaBin): puede ser None

        **excepciones**
            -   **TypeError**: si el parametro ingresado no es una semiila**
        """
        if semilla is not None:
            validarTipoObjeto(SemillaBin, semilla, "Ingresa una semilla")

    @staticmethod
    def validarTiposSemilla(semilla1:SemillaBin, semilla2:SemillaBin) -> None:
        """Dado dos semillas binarias, valida que tengan el mismo tipo de datos
            
        **parameters**
            -   semilla1 (SemillaBin[T])
            -   semilla2 (SemillaBin[T])

        **excepciones**
            -   **TypeError**: si el parametro ingresado no es una semilla o si no tienen el mismo tipo de dato
        """
        SemillaBin.validarSemilla(semilla1)
        SemillaBin.validarSemilla(semilla2)
        validarCondicion(not issubclass(semilla1.getType(), semilla2.getType()) and not issubclass(semilla2.getType(), semilla1.getType()),
                         "Ingresa dos semillas con el mismo tipo de Dato", TypeError)
        
    #METODOS ESTATICOS
    @staticmethod
    def intercambiarDatos(semilla1:SemillaBin[T], semilla2:SemillaBin[T]) -> None:
        """Dado dos semillas, del mismo tipo de dato, intercambian los datos almacenados en sí
        
        **parameters**
            -   semilla1 (SemillaBin[T])
            -   semilla2 (SemillaBin[T])

        **excepciones**
            -   **TypeError**: si el parametro ingresado no es una semilla o si no tienen el mismo tipo de dato
        """
        SemillaBin.validarTiposSemilla(semilla1, semilla2)

        dato = semilla1.getDato()
        semilla1.setDato(semilla2.getDato())
        semilla2.setDato(dato)
        
    #FLAGS
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

    #GETTERS
    def getEquilibrio(self) -> int:
        """Obtiene el nivel de equilibrio de la semilla: si la semilla está equilibrada, devuelve 0;
        si esta desequilibrada a la izquierda, devuelve un numero negativo; si lo está a la derecha,
        devuelve un entero positivo

        **return**
            -   (bool) grado de equilibrio
        """
        if not self.tieneHijos():
            return 0

        if self.tieneAmbosHijos():
            return self.getIzquierda().getEquilibrio() + self.getDerecha().getEquilibrio()

        if self.tieneHijoIzq():
            return -1 + self.getIzquierda().getEquilibrio()

        return 1 + self.getDerecha().getEquilibrio()

    def getIzquierda(self) -> SemillaBin[T]:
        """Retonra la semilla hija de la izquierda
        
        **return**
            -   (SemillaBin[T]) semilla Izquierda
        """
        return self.__izquierda

    def getDerecha(self) -> SemillaBin[T]:
        """Retorna la semilla hija de la derecha

        **return**
            -   (SemillaBin[T]) semilla Derecha           
        """
        return self.__derecha

    #SETTERS
    def setIzquierda(self, izquierda:SemillaBin[T]) -> None:
        """Setea la semilla hija izquierda
        
        **parameters**
            -   izquierda (SemillaBin[T]): Mismo tipo de dato, puede ser null
        """
        SemillaBin.validarSemilla(izquierda)
        self.__izquierda = izquierda

    def setDerecha(self, derecha:SemillaBin[T]) -> None:
        """Setea la semilla hija izquierda
        
        **parameters**
            -   izquierda (SemillaBin[T]): Mismo tipo de dato, puede ser null
        """
        SemillaBin.validarSemilla(derecha)
        self.__derecha = derecha


#ARBOL --------------------------------------------------------------------------------------------------------------
class ArbolBin(Generic[T], TypeStruct):
    #ATRIBUTOS
    __raiz:SemillaBin[T]
    __ordenamiento:function
    __cantidadElementos:int

    #CONSTRUCTOR
    def __init__(self, tipo:type, metodo:function = None) -> ArbolBin[T]:
        """Dado un tipo de dato, crea un arbol binario que almacene tal información y la ordene automaticamente
        
        **parameters**
            -   tipo (type)
            -   metodo (function): por defecto None. Tipo de metodo para ordenar los datos
        """
        super().__init__(tipo)

        self.__setMetodo(metodo)
        self.__setRaiz(None)
        self.__iniciarConteo()

    #METODOS GENERALES
    def __iter__(self) -> Generator[T]:
        yield from self.__recorridoPreorden(self.__getRaiz())

    #METODOS DE CLASE
    def agregar(self, item:T) -> None:
        self.__validarEntrada__(item)

        if self.estaVacio():
            self.__setRaiz(self.__generarSemilla(item))
        else:
            self.__insertarDato(item, self.__getRaiz())
        
        self.__agregarItem()
        
    def remover(self, item:T):
        self.__validarEntrada__(item)

        if (self.getCantidadElementos() == 1):
            validarCondicion(self.__getRaiz().getDato() != item, "Este elemento no se encuentra en el arbol", ElementoNoEncontrado)
            self.__setRaiz(None)
        else:
            self.__buscarYBorrar(item, self.__getRaiz(), self.__getRaiz())    
        self.__quitarItem()

    def mapear(self) -> Vector[T]:
        vector = Vector(self.getType(), self.getCantidadElementos()) 
        lista = []
        self.__recorridoInorden(self.__getRaiz(), lista)

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

    def __recorridoInorden(self, semilla:SemillaBin[T], lista:list):
        if semilla.getIzquierda() is not None:
            self.__recorridoInorden(semilla.getIzquierda(),lista)

        lista.append(semilla.getDato())

        if semilla.getDerecha() is not None:
            self.__recorridoInorden(semilla.getDerecha(),lista)

    def __recorridoPreorden(self, semilla:SemillaBin[T]):
        yield semilla.getDato()

        if semilla.tieneHijoIzq():yield from self.__recorridoPreorden(semilla.getIzquierda())
        if semilla.tieneHijoDer():yield from self.__recorridoPreorden(semilla.getDerecha())

    def __buscarYBorrar(self, item:T, semilla:SemillaBin[T], padre:SemillaBin[T]) -> None:
        if (semilla == None):
            raise ElementoNoEncontrado(f"El elemento ingresado ({item}) no pertenece a este arbol")
        if (semilla.getDato() == item):
            self.__regresion(semilla, padre)
        elif (self.__menorIgual(item, semilla.getDato())):
            self.__buscarYBorrar(item, semilla.getIzquierda(),semilla)
        else:
            self.__buscarYBorrar(item, semilla.getDerecha(), semilla)

    def __regresion(self, semilla:SemillaBin[T], padre:SemillaBin[T]) -> None:
        if (not semilla.tieneHijos()):
            try:
                padre.desconectarIzq()
            except:
                padre.desconectarDer()

        elif (semilla.tieneHijoIzq()):
            semilla.intercambiarIzq()
            self.__regresion(semilla.getIzquierda(), semilla)
        else:
            semilla.intercambiarDer()
            self.__regresion(semilla.getDerecha(), semilla)

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

    def __cantidadHijos(self, semilla:SemillaBin[T], cantidad:int) -> int:
        if semilla.tieneAmbosHijos():
            cantidad +=2
        elif semilla.tieneHijos():
            cantidad += self.__cantidadHijos(
                filtrarElNulo(semilla.getIzquierda(), semilla.getDerecha()), cantidad
            ) + 1
        return cantidad

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

    @staticmethod
    def diferencia(arbol1:ArbolBin[T], arbol2:ArbolBin[T]) -> ArbolBin[T]:
        diferencia = ArbolBin(arbol1.getType(), arbol1.__ordenamiento)

        for item in arbol1:
            if item not in arbol2:
                diferencia.agregar(item)

        return diferencia
    
    #FLAGS    
    def estaElItem(self, item:T) -> bool:
        """Dado un item, verifica que se encuentre almacenado en el árbol
        
        **parameters**
            -   item (T)

        **return**
            -   (bool) Verdadero si el item está en el árbol, falso si no
        """ 
        self.__validarEntrada__(item)
        return self.__buscar(item, self.__getRaiz())
    
    def estaEquilibrado(self) -> bool:
        """Verifica que el árbol esté equilibrado
        
        **return**
            -   (bool) Verdadero si el nivel de equilibrio es cero, falso si no
        """
        return self.__getRaiz().getEquilibrio() == 0

    def estaVacio(self) -> bool:
        """Verifica que el árbol esté vacío
        
        **return**
            -   (bool) Verdadero si la cantidad de elementos en el árbol es exactamente cero, falso si no
        """
        return self.getCantidadElementos() == 0

    #GETTERS
    def getCantidadHijos(self, item:T) -> int:
        
        return self.__cantidadHijos(self.__buscarSemilla(item,self.__getRaiz()), 0)

    def getSubarbol(self, item:T) -> ArbolBin[T]:
        raiz = self.__buscarSemilla(item, self.__getRaiz())
        subarbol = ArbolBin(self.getType())

        subarbol.__setRaiz(raiz)
        subarbol.__cantidadElementos = self.__cantidadHijos(raiz,0)

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