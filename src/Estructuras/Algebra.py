from .Vector import Vector, Matriz, PRIMERA_POSCICION
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
    __permitirFloat:bool
    #CONSTRUCTOR
    def __init__(self, *filas:VectorAlgebraico, permtirFloat:bool = False):
        self.__validarFilas(*filas, permtirFloat=permtirFloat)

        self.__permitirFloat = permtirFloat
        if permtirFloat:
            self.__matriz = self.__matriz = Matriz(float,len(filas), filas[0].getDimension())
        else: self.__matriz = Matriz(int,len(filas), filas[0].getDimension())
        
        for i in range(len(filas)):
            for j in range(filas[0].getDimension()):
                if permtirFloat:
                    self.__matriz.setItem(i,j,float(filas[i][j]))
                else:
                    self.__matriz.setItem(i,j,filas[i][j])
                

    #METODOS GENERALES
    def __str__(self):
        return "M :\n"+str(self.__matriz)
        
    #METODOS DE CLASE

    def tieneFloat(self):
        return self.__permitirFloat
    
    def esCuadarada(self):
        return self.__matriz.esCuadrada()

    #METODOS INTERNOS
    #VALIDACIONES
    
    def __validarFilas(self, *filas:VectorAlgebraico, permtirFloat:bool):
        validarTipoObjeto(bool, permtirFloat, "Ingrese una condicion booleana", TypeError)

        anteriorFila:VectorAlgebraico = None
        
        for fila in filas:
            validarTipoObjeto(VectorAlgebraico,fila, "Las filas de la matriz algebraica deben ser vectores algebraicos")
            if anteriorFila == None:
                fila = anteriorFila
            else:
                validarValorObligatorio(fila.getDimension(),anteriorFila.getDimension(),
                                        "Todas las filas deben tener la misma dimension", DimensionIncompatibleError)
            
    

    @staticmethod
    def validarMatriz(matriz:MatrizAlgebraica):
        validarTipoObjeto(MatrizAlgebraica,matriz, "Ingrese una matriz algebráica")

    @staticmethod
    def validarOperaciones(matriz1:MatrizAlgebraica, matriz2:MatrizAlgebraica):
        MatrizAlgebraica.validarMatriz(matriz1)
        MatrizAlgebraica.validarMatriz(matriz2)
        validarValorObligatorio(matriz1.getDimensionFila(),matriz2.getDimensionFila(),
                                "Esta operacion requiere que ambas matrices tengan las mismas dimensiones", DimensionIncompatibleError)
        
        validarValorObligatorio(matriz1.getDimensionColumna(),matriz2.getDimensionColumna(),
                                "Esta operacion requiere que ambas matrices tengan las mismas dimensiones", DimensionIncompatibleError)

    #OPERACIONES
    def __add__(self, other:MatrizAlgebraica) -> MatrizAlgebraica:
        self.validarOperaciones(self,other)
        resultado = []

        for i in range(self.getDimensionColumna()):
            fila = []
            for j in range(self.getDimensionFila()):
                fila.append(self.getItem(i,j)+other.getItem(i,j))
            
            resultado.append(VectorAlgebraico(*fila, permitirFloat=self.tieneFloat() or other.tieneFloat()))
        
        return MatrizAlgebraica(*resultado, permtirFloat=self.tieneFloat() or other.tieneFloat())

    def __mul__(self, other:int|float) -> MatrizAlgebraica:
        resultado = []
        tieneFloat = False

        for i in range(self.getDimensionColumna()):
            fila = []
            for j in range(self.getDimensionFila()):
                fila.append(self.__matriz.getItem(i,j) * other)

            if not tieneFloat:
                tieneFloat = self.tieneFloat() or isinstance(other,float)

            resultado.append(VectorAlgebraico(*fila,permitirFloat= tieneFloat))
        
        return MatrizAlgebraica(*resultado, permtirFloat= tieneFloat)
    def __rmul__(self, other:int|float):
        return self*other

    def __neg__(self):
        return self*(-1)

    def __sub__(self, other:MatrizAlgebraica):
        return self + (-other)
        
    

    #GETTERS
    def getTraza(self):
        validarCondicion(not self.esCuadarada(), "La traza solo funciona para matrices cuadradas", DimensionIncompatibleError)

        traza = 0

        for i in range(self.getDimensionFila()):
            traza += self.getItem(i,i)

        return traza

    def getTraspuesta(self):
        traspuesta = []

        for i in range(self.getDimensionFila()):
            fila = []
            for j in range(self.getDimensionColumna()):
                fila.append(self.getItem(j,i))

            traspuesta.append(VectorAlgebraico(*traspuesta, permitirFloat = self.tieneFloat()))

        return MatrizAlgebraica(*traspuesta, permtirFloat= self.tieneFloat())

    def getDeterminante(self) -> int|float:
        validarCondicion(self.esCuadarada(), "El determinante solo funciona para matrices cuadradas", DimensionIncompatibleError)

        if self.getDimensionColumna() == 1:
            return self.getItem(1,1)

    def getItem(self, indice:int, jndice:int) -> int|float:
        return self.__matriz.getItem(indice,jndice)

    def getDimensionFila(self):
        return self.__matriz.getLongitudFila()
    
    def getDimensionColumna(self):
        return self.__matriz.getLongitudColu()
    
    def getItem(self, i, j):
        return self.__matriz.getItem(i,j)