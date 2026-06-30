from .Vector import Vector, Matriz
from .Validaciones import validarTipoObjeto, validarCondicion, validarRango,validarValorObligatorio, FalloValidacion
from .Excepciones.Algebraicos import *

class VectorAlgebraico:
    #ATRIBUTOS
    __vector:Vector[int]

    #CONSTRUCTORES
    def __init__(self, *coordenadas:int, permitirFloat:bool = False):
        """Crea un vector algebraíco, dado una serie de numeros
        
        **parameters**
            -   *coordenadas (int): serie de numeros del vector, se ingresan en ese orden
            -   permitirFloar (bool): Por defecto Falso, si es Verdadero, los numeros se almacenan como flotantes

        **excepciones**
            -  **TypeError**: si al menos uno de los elementos no es int. Si permitirFloat es falso, tambien si no es float
        """
        self.__validarEntradas(coordenadas, permitirFloat)

        if permitirFloat:
            self.__vector = Vector(float, len(coordenadas))
            for i in range(len(coordenadas)):
                self.__vector[i] = float(coordenadas[i])
            
        else:
            self.__vector = Vector(int, len(coordenadas))
            for i in range(len(coordenadas)):
                self.__vector[i] = coordenadas[i]
            

    #MEOTODOS GENERALES
    def __str__(self):
        return "v = "+str(self.__vector) 
    
    def __getitem__(self, key) -> int|float:
        self.__validarKey(key)
        return self.__vector[key]

    
    #METODOS DE CLASE
    def tieneFloat(self):
        return self.__vector.getType() is float

    #VALIDACIONES
    def __validarEntradas(self, coordenadas:tuple[int], permtirFloat:bool):
        validarTipoObjeto(bool, permtirFloat, "Ingrese una condicion booleana", TypeError)

        if permtirFloat: mensaje = "Ingresa numeros int o float"
        else: mensaje = "Ingresa numeros int unicamente"

        for numero in coordenadas:  
            validarCondicion(
                (not isinstance(numero, int)) and (not isinstance(numero, float) or not permtirFloat),
                mensaje, TypeError 
            )

    def __validarEntradaUnica(self, entrada:int|float, permitirFloat:bool = True):
        self.__validarEntradas((entrada, ),permitirFloat)

    def __validarKey(self, key:int):
        validarTipoObjeto(int, key, "Ingresa un indice int")
        validarRango(key,0,self.getDimension()-1, 
                     mensaje= f"Ingresa un valor entre 0 y {self.getDimension()}")

    @staticmethod
    def __validarOperacion(vector1:VectorAlgebraico, vector2:VectorAlgebraico):
        validarTipoObjeto(VectorAlgebraico, vector1, "Ingresa un vector algebraíco como parametro")
        validarTipoObjeto(VectorAlgebraico, vector2, "Ingresa un vector algebraíco como parametro")

        validarCondicion(vector1.getDimension() != vector2.getDimension(), 
                         "Ingrese dos vectores con la misma dimension", DimensionIncompatibleError)

    #OPERACIONES

    def __add__(self, other:VectorAlgebraico) -> VectorAlgebraico:
        resultado = []

        for i in range(self.getDimension()):
            resultado.append(self.__vector[i] + other.__vector[i])

        return VectorAlgebraico(*resultado, permitirFloat= (self.tieneFloat() or other.tieneFloat()))
    
    def __mul__(self, esc:int|float) -> VectorAlgebraico:
        self.__validarEntradaUnica(esc)

        resultado = []

        for i in range(self.getDimension()):
            resultado.append(self.__vector[i]*esc)

        return VectorAlgebraico(*resultado, permitirFloat = isinstance(esc,float))
    def __rmul__(self, other:int|float) -> VectorAlgebraico:
        return self*other
    
    def __neg__(self) -> VectorAlgebraico:
        return self*(-1)
    
    def __truediv__(self, other:int|float) -> VectorAlgebraico:
        self.__validarEntradaUnica(other)
        return self * (1/other)

    def __floordiv__(self, other:int|float) -> VectorAlgebraico:
        self.__validarEntradaUnica(other, self.tieneFloat())
        resultado = []
        
        for i in range(self.getDimension()):
            resultado.append(self.__vector[i]//other)

        return VectorAlgebraico(*resultado, self.tieneFloat())
    
    @staticmethod
    def productoEsc(vector1:VectorAlgebraico, vector2:VectorAlgebraico) -> int|float:
        VectorAlgebraico.__validarOperacion(vector1, vector2)
        producto = 0

        for i in range(vector1.getDimension()):
            producto += vector1.__vector[i] * vector2.__vector[i]

        return producto

    @staticmethod
    def productoVec(vector1:VectorAlgebraico, vector2:VectorAlgebraico) -> int|float:
        validarCondicion(vector1.getDimension() != 3, "Esta operacion solo sirve con vectores de dimension 3", DimensionIncompatibleError)
        validarCondicion(vector2.getDimension() != 3, "Esta operacion solo sirve con vectores de dimension 3", DimensionIncompatibleError)

        return VectorAlgebraico(
            vector1.__vector[1]*vector2.__vector[2] - vector1.__vector[2]*vector2.__vector[1],
            vector1.__vector[2]*vector2.__vector[0] - vector1.__vector[0]*vector2.__vector[2],
            vector1.__vector[0]*vector2.__vector[1] - vector1.__vector[1]*vector2.__vector[0],
            permitirFloat= vector1.tieneFloat() or vector2.tieneFloat()
        )

    #GETTERS
    def getDimension(self) -> int: 
        return len(self.__vector)
    
    def getNorma(self) -> float:
        return VectorAlgebraico.productoEsc(self, self)**(1/2)

class MatrizAlgebraica:
    #ATRIBUTOS
    __matriz:Matriz
    #CONSTRUCTOR
    def __init__(self, *filas:VectorAlgebraico, permtirFloat:bool = False):
        self.__validarFilas(filas, permtirFloat=permtirFloat)

        self.__matriz = Matriz(int,len(filas), len(filas[0]))
        for i in range(len(filas)):
            for j in range(len(filas[0])):
                self.__matriz[i][j] = filas[i][j]


    #METODOS GENERALES
    #METODOS DE CLASE
    #METODOS INTERNOS
    #VALIDACIONES
    
    def __validarFilas(self, *filas:VectorAlgebraico, permtirFloat:bool):
        validarTipoObjeto(bool, permtirFloat, "Ingrese una condicion booleana", TypeError)
        anteriorFila:VectorAlgebraico = None
        if permtirFloat: mensaje = "Ingresa numeros int o float"
        else: mensaje = "Ingresa numeros int unicamente"
        for fila in filas:
            validarTipoObjeto(VectorAlgebraico,fila, "Las filas de la matriz algebraica deben ser vectores algebraicos")
            if anteriorFila == None:
                fila = anteriorFila
            else:
                validarValorObligatorio(fila.getDimension(),anteriorFila.getDimension(),
                                        "Todas las filas deben tener la misma dimension", DimensionIncompatibleError)
            for numero in fila:    
                validarCondicion(
                    (not isinstance(numero, int)) and (not isinstance(numero, float) or not permtirFloat),
                    mensaje, TypeError 
                )



    #OPERACIONES
    #GETTERS