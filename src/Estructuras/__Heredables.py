from .__Validaciones import validarTipo, validarTipoObjeto, validarCondicion, Generic, T, FalloValidacion


#TYPE STRUCT ------------------------------------------------------------------------------------------- 
class TypeStruct:
    """Esta clase ingresa un tipo y verifica que cualquier entrada sea de ese tipo ingresado
    
    Usarla cuando estas creando una estructura de datos y necesitas que todos los datos almacen un solo tipo de datom,
    haciendo que la estructura herede TypeStruct
    """
    #ATRIBUTOS
    __tipo:type

    #CONSTRUCTOR
    def __init__(self, tipo:type):
        """Dado un tipo de objeto, setea el tipo de dato que la estructura va a recibir
        
        **parameters**
            -   **tipo** (type)

        **excepciones**
            -   **TypeError**: si el tipo ingresado no es un type
        """
        self.__setType(tipo)

    #METODOS DE CLASE
    def __validarEntrada__(self, entrada:T, permitirNone = False):
        """Dado una entrada, valida que sea del tipo ingresado, sino no lo es, lanza TypeError
        
        **parameters**
            -   **entrada** (tipo ingresado)
            -   **permitiNone** (bool): por defecto False. Si es verdadero, no saltará error si la entrada es None.
        
        **excepciones**
            -   **FalloValidacion**: si el parametro permitirNone no es una condicion bool
            -   **TypeError**: si la entrada no es del tipo ingresado. Si la condicion permitirNone es false, tambien saltará eror si la entrada es None
        """
        validarTipoObjeto(bool, permitirNone,"La condicion de permitir None debe ser booleana", FalloValidacion)
        if (self.getType() is None):
            validarCondicion(entrada is not None, "Ingresa un tipo None",TypeError)
        elif (entrada is not None) or (not permitirNone):
            validarTipoObjeto(self.getType(), entrada, "Ingresa un tipo "+self.getTypeName()) 


    def __validarEntradas__(self, *entradas:T, permitirNone = False):
        """Dado varias entradas, valida que cada una sea del tipo ingresado, sino no lo es, lanza TypeError
        
        **parameters**
            -   **entradas** (tuple[tipo ingresado])
            -   **permitiNone** (bool): por defecto False. Si es verdadero, no saltará error si alguna entrada es None.
        
        **excepciones**
            -   **FalloValidacion**: si el parametro permitirNone no es una condicion bool
            -   **TypeError**: si la entrada no es del tipo ingresado. Si la condicion permitirNone es false, tambien saltará eror si la entrada es None
        """
        validarTipoObjeto(bool, permitirNone,"La condicion de permitir None debe ser booleana", FalloValidacion)
        for entrada in entradas:
            if (entrada is not None) or (not permitirNone) and (self.getType() is None):
                validarTipoObjeto(entrada, self.getType(), "Una de las entradas ingresadas no es del tipo "+self.getTypeName())

    #GETTERS
    def getType(self) -> type:
        """Retorna el tipo de variable almacenable
        
        **return**
            -   **type** tipo de variable
        """
        return self.__tipo
    
    def getTypeName(self) -> str:
        """Retorna el nombre del tipo de variable almacenable
        
        -   **return**
            -   **str** nombre del tipo de variable
        """
        if self.getType() is None: return str(None)
        return self.getType().__name__

    #SETTERS
    def __setType(self, tipo:type):
        """Setea el tipo de variable que se va a filtrar
        
        -   **parameters**
            -   **tipo** (type)

        -   **excepciones**
            -   **TypeError**: si el tipo no es un type
        """
        if (tipo is not None):validarTipo(tipo)
        self.__tipo = tipo

#DATA STRUCT ----------------------------------------------------------------------------------------------
class DataStruct(TypeStruct,Generic[T]):
    """Heredable para crear estructuras de datos enlazadas, digase Listas, Arboles, lo que se te ocurra.
    Con esta clase se podrán crear los nodos que almacenan un unico tipo de dato
    """
    #ATRIBUTOS
    __dato:T
    __permitirNone:bool

    #CONSTRUCTOR
    def __init__(self, tipo:type, dato:T, permitirNone:bool = False):
        """Heredable para objetos que almacenan un solo dato y sirven para linkear cosas, qsy, como Arboles o Listas
        
        **parameters**
            -   tipo (type)        
            -   dato (T): del mismo tipo que el tipo
            -   permitirNone (bool): por defecto False. Si es True, entonces permitira guardar None en los DataStructs

        **excepciones**
            -   **TypeError**: si el dato ingresado no coincide con el tipo ingresado

        """
        super().__init__(tipo)
        self.__setPermitirNone(permitirNone)
        self.setDato(dato)

    #GETTERS
    def getDato(self) -> T:
        """Obtiene el dato almacenado
        
        **return**
            -   (T) dato almacenado
        """
        return self.__dato
    
    def __getPermitirNone(self) -> bool:
        """Retorna la condicion de permtir none
        
        **return**
            -   (bool) Verdadero si el dataStruct permiteNone, falso si no
        """
        return self.__permitirNone
    
    #SETTERS
    def setDato(self, dato:T):
        """Almacena el dato en la estructura
        
        **parameters**
            -   dato (T)
            
        **excepciones**
            -   **TypeError**: si el dato ingresado no corresponde con el tipo ingresado
        """
        self.__validarEntrada__(dato,self.__getPermitirNone())
        self.__dato = dato

    def __setPermitirNone(self, permitir:bool):
        """Setea si se permite o no el None
        
        **parameters**
            -   permitirNone (bool): por defecto False. Si es True, entonces permitira guardar None en los DataStructs
        """
        self.__permitirNone = permitir

