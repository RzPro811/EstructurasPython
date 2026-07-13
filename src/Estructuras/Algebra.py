from .Vector import Vector, Matriz, PRIMERA_POSCICION
from .Validaciones import validarTipoObjeto, validarCondicion, validarRango,validarValorObligatorio, validarVariosTipos, validarNoNegativo
from .Excepciones.Algebraicos import *
from .Heredables import Numerico

class VectorAlgebraico:
    #ATRIBUTOS
    __vector:tuple[Numerico|int|float|complex]

    #CONSTRUCTORES
    def __init__(self, *coordenadas:int):
        """Crea un vector algebraíco, dado una serie de numeros
        
        **parameters**
            -   *coordenadas (int): serie de numeros del vector, se ingresan en ese orden
            -   permitirFloar (bool): Por defecto Falso, si es Verdadero, los numeros se almacenan como flotantes

        **excepciones**
            -  **TypeError**: si al menos uno de los elementos no es int. Si permitirFloat es falso, tambien si no es float
        """
        vector = []
        for numero in coordenadas:
            Numerico.validarNumero(numero)
            vector.append(numero)

        self.__vector = tuple(vector)
            

    #MEOTODOS GENERALES
    def __str__(self):
        return "v = "+str(self.__vector) 
    
    def __getitem__(self, key) -> int|float:
        self.__validarKey(key)
        return self.__vector[key]

    def __iter__(self):
        for num in self.__vector:
            return num

    def __validarKey(self, key:int):
        validarTipoObjeto(int, key, "Ingresa un indice int")
        validarRango(key,0,self.getDimension()-1, 
                     mensaje= f"Ingresa un valor entre 0 y {self.getDimension()}")

    @staticmethod
    def __validarOperacion(vector1:VectorAlgebraico, vector2:VectorAlgebraico):
        validarTipoObjeto(VectorAlgebraico, vector1, "Ingresa un vector algebraíco como parametro")
        validarTipoObjeto(VectorAlgebraico, vector2, "Ingresa un vector algebraíco como parametro")

        validarValorObligatorio(vector1.getDimension(),vector2.getDimension(),
                                "Ambos vectores deben tener la misma dimension", DimensionIncompatibleError)

    #METODOS ESTATICOS
    def sonLinealmenteIndependientes(vector1, vector2) -> bool:pass

    def convertirEnAlgebraico(vector:Vector[int|float|Numerico|complex]) -> VectorAlgebraico:
        validarTipoObjeto(Vector, vector, "Inresa un Vector")
        validarCondicion(not vector.estaLleno(), "El vector debe estar lleno")
        validarVariosTipos(vector[0], int, float, complex, Numerico,
                           mensaje= "Ingrese un vector con tipo de dato de dato numerico")

        algebraico = []
        for elemento in vector:
            algebraico.append(elemento)

        return VectorAlgebraico(*algebraico)

    #OPERACIONES

    def __add__(self, other:VectorAlgebraico) -> VectorAlgebraico:
        VectorAlgebraico.__validarOperacion(self, other)
        resultado = []

        for i in range(self.getDimension()):
            resultado.append(self.__vector[i] + other.__vector[i])

        return VectorAlgebraico(*resultado)
    
    def __mul__(self, esc:int|float|complex|Numerico) -> VectorAlgebraico:
        Numerico.validarNumero(esc)

        resultado = []

        for i in range(self.getDimension()):
            resultado.append(self.__vector[i]*esc)

        return VectorAlgebraico(*resultado)
    def __rmul__(self, other:int|float) -> VectorAlgebraico:
        return self*other
    
    def __neg__(self) -> VectorAlgebraico:
        return self*(-1)
    
    def __truediv__(self, esc:int|float) -> VectorAlgebraico:
        Numerico.validarNumero(esc)
        return self * (1/esc)

    def __floordiv__(self, esc:int|float) -> VectorAlgebraico:
        Numerico.validarNumero(esc)
        resultado = []
        
        for i in range(self.getDimension()):
            resultado.append(self.__vector[i]//esc)

        return VectorAlgebraico(*resultado)
    
    @staticmethod
    def productoEsc(vector1:VectorAlgebraico, vector2:VectorAlgebraico) -> int|float:
        VectorAlgebraico.__validarOperacion(vector1, vector2)
        producto = 0

        for i in range(vector1.getDimension()):
            producto += vector1.__vector[i] * vector2.__vector[i]

        return producto

    @staticmethod
    def productoVec(vector1:VectorAlgebraico, vector2:VectorAlgebraico) -> int|float:
        VectorAlgebraico.__validarOperacion(vector1, vector2)
        validarValorObligatorio(vector1.getDimension(), 3, "Esta operacion solo sirve con vectores de dimension 3", DimensionIncompatibleError)

        return VectorAlgebraico(
            vector1.__vector[1]*vector2.__vector[2] - vector1.__vector[2]*vector2.__vector[1],
            vector1.__vector[2]*vector2.__vector[0] - vector1.__vector[0]*vector2.__vector[2],
            vector1.__vector[0]*vector2.__vector[1] - vector1.__vector[1]*vector2.__vector[0],
        )

    #GETTERS
    def getDimension(self) -> int: 
        return len(self.__vector)
    
    def getNorma(self) -> float:
        return VectorAlgebraico.productoEsc(self, self)**(1/2)

#MATRIZ ALGEBRAICA ---------------------------------------------------------------------------------------------------
class MatrizAlgebraica:
    #ATRIBUTOS
    __matriz:tuple[VectorAlgebraico]
    
    #CONSTRUCTOR
    def __init__(self, *filas:VectorAlgebraico):
        matriz = []
        
        dimension = 0
        for vector in filas:
            validarTipoObjeto(VectorAlgebraico, vector, "Las filas deben ser vectores")
            
            if dimension is not 0:
                validarValorObligatorio(vector.getDimension(), dimension, 
                    "Todas las filas de la matriz deben tener la misma dimension", DimensionIncompatibleError)
            else: dimension = vector.getDimension()

            fila = []
            for num in vector:
                Numerico.validarNumero(num)
                fila.append(num)

            matriz.append(VectorAlgebraico(*fila))

        self.__matriz = tuple(fila)

    #METODOS GENERALES
    def __str__(self):
        return "M :\n"+str(self.__matriz)
        
    #METODOS DE CLASE
    def esCuadarada(self) -> bool:
        return self.getDimensionColumna() == self.getDimensionFila()
    
    def tieneElNumero(self, num:int|float|complex|Numerico) -> bool:
        Numerico.validarNumero(num)

        encontrado = False
        i = 0

        while not encontrado and (i < self.getDimensionColumna()):
            j = 0
            while not encontrado and (j < self.getDimensionFila()):
                if self.getItem(i,j) == num:
                    encontrado = True
                else:
                    j+=1
            i+=1

        return encontrado

    #VALIDACIONES            
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

    @staticmethod
    def convertirAlgebraico(matriz:Matriz) ->MatrizAlgebraica:
        validarTipoObjeto(Matriz, matriz, "Inresa un Vector")
        validarCondicion(not issubclass(matriz.getType(), int) and not issubclass(matriz.getType(), float),
                         "Inregse un vector con valores numericos", TypeError)
        conversion = []

        for i in range(matriz.getLongitudColu()):
            conversion.append(
                VectorAlgebraico.convertirEnAlgebraico(
                    matriz.getFila(i)
                )
            )

        return MatrizAlgebraica(*conversion, permtirFloat=matriz.getType() is float)

    @staticmethod
    def generarIdentidad(dimension:int):
        identidad = Matriz(int, dimension, dimension)

        for i in range(dimension):
            for j in range(dimension):
                if i == j:
                    identidad.setItem(i,j,1)
                else:
                    identidad.setItem(i,j,0)

        return MatrizAlgebraica.convertirAlgebraico(identidad) 

    #OPERACIONES
    def __add__(self, other:MatrizAlgebraica) -> MatrizAlgebraica:
        self.validarOperaciones(self,other)
        pass
    
    def __mul__(self, esc:int|float) -> MatrizAlgebraica:
        Numerico.validarNumero(esc)
        pass
    def __rmul__(self, other:int|float):
        return self*other

    def __neg__(self):
        return self*(-1)

    def __sub__(self, other:MatrizAlgebraica):
        return self + (-other)
    
    def pow(self, exp:int):
        validarTipoObjeto(int, exp, "Inrese un exponente entero")
        validarNoNegativo(exp,True,"El exponente debe ser positivo o cero")

        if exp == 0:
            return MatrizAlgebraica.generarIdentidad(self.getDimensionFila())

        return MatrizAlgebraica.productoMatricial(
            self, self.pow(exp-1)
        ) 
        
    @staticmethod
    def productoMatricial(matriz1:MatrizAlgebraica, matriz2:MatrizAlgebraica) -> MatrizAlgebraica:
        validarValorObligatorio(matriz1.getDimensionFila(), matriz2.getDimensionColumna(), 
                "La dimension de la fila de la primera matriz debe ser igual que la dimension de las columnas de la segunda matriz", DimensionIncompatibleError)
        producto = []    

        for i in range(matriz1.getDimensionColumna()):
            fila = []
            for j in range(matriz2.getDimensionFila()):
                fila.append(
                    VectorAlgebraico.productoEsc(matriz1.getFila(i),matriz2.getColumna(j),
                    )
                )

            producto.append(VectorAlgebraico(*fila, permitirFloat= matriz1.tieneFloat() or matriz2.tieneFloat()))

        return MatrizAlgebraica(*producto, permtirFloat= matriz1.tieneFloat() or matriz2.tieneFloat())

    @staticmethod
    def productoInterno(matriz1:MatrizAlgebraica, matriz2:MatrizAlgebraica):
        MatrizAlgebraica.validarOperaciones(matriz1,matriz2)
        return MatrizAlgebraica.productoMatricial(matriz1, matriz2.getTraspuesta()).getTraza()

    #GETTERS
    def __getSubmatriz(self, filaDejada:int, columnaDejada:int) -> MatrizAlgebraica:
        submatriz = []

        for i in range(self.getDimensionFila()):
            if i != filaDejada:
                fila = []
                
                for j in range(self.getDimensionFila()):
                    if j != columnaDejada:
                        fila.append(self.getItem(i,j))
                
                submatriz.append(VectorAlgebraico(*fila,permitirFloat=self.__permitirFloat))

        return MatrizAlgebraica(*submatriz, permtirFloat= self.__permitirFloat)
    

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
        validarCondicion(not self.esCuadarada(), "El determinante solo funciona para matrices cuadradas", DimensionIncompatibleError)

        if self.getDimensionColumna() == 1:
            return self.getItem(PRIMERA_POSCICION, PRIMERA_POSCICION)

        signoCoeficiente = 1
        determinante = 0

        for i in range(self.getDimensionFila()):
            determinante += signoCoeficiente * self.getItem(PRIMERA_POSCICION,i) * self.__getSubmatriz(PRIMERA_POSCICION,i).getDeterminante()
            signoCoeficiente*=-1

        return determinante

    def getItem(self, indice:int, jndice:int) -> int|float:
        return self.__matriz[indice][jndice]

    def getDimensionFila(self):
        return self.__matriz[0].getDimension()
    
    def getDimensionColumna(self):
        return len(self.__matriz)
    
    def getFila(self, i:int) -> VectorAlgebraico:
        return self.__matriz[i]
    
    def getColumna(self, j:int) -> VectorAlgebraico:
        pass
    

class Polinomio:
    #ATRIBUTOS
    __polinomio:tuple[int]