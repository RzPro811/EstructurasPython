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
            -   *coordenadas: numeros int, float, complex u objetos con la plantilla Numerico

        **excepciones**
            -  **TypeError**: si al menos uno de los elementos no es un numero
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
            yield num

    def __validarKey(self, key:int):
        """Valida un indice para obtener un valor del vector
        
        **parameters**
            -   key (int): entre 0 y la dimension del vector - 1

        **excepciones**
            -   **TypeError**: si el parametro no es int
            -   **IndexError**: si el valor no está en el rango especificado
        """
        validarTipoObjeto(int, key, "Ingresa un indice int")
        validarRango(key,0,self.getDimension()-1, 
                     mensaje= f"Ingresa un valor entre 0 y {self.getDimension()}")

    @staticmethod
    def __validarOperacion(vector1:VectorAlgebraico, vector2:VectorAlgebraico):
        """Valida que dos vectores puedan funcionar para hacer una operacion. 
        Primero deben ambos ser Vectores, pero Algebraicos, y segundo, deben tener la misma dimension

        **parameters**
            -   vector1 (VectorAlgebraico): dimension n
            -   vector2 (VectorAlgebraico): dimension n

        **excepciones**
            -   **TypeError**: si algun parametro ingresado no es VectorAlgebraico
            -   **DimensionIncompatibleError**: si los vectores no tienen la misma dimension
        """
        validarTipoObjeto(VectorAlgebraico, vector1, "Ingresa un vector algebraíco como parametro")
        validarTipoObjeto(VectorAlgebraico, vector2, "Ingresa un vector algebraíco como parametro")

        validarValorObligatorio(vector1.getDimension(),vector2.getDimension(),
                                "Ambos vectores deben tener la misma dimension", DimensionIncompatibleError)

    #METODOS ESTATICOS
    @staticmethod
    def generarVersorCanonico(dimension:int, versorNumero:int) -> VectorAlgebraico:
        """Genera un versor caonico. Es decir, un vector cuyas componentes sean ceros y un solo uno
        
        **parameters**
            -   dimension (int): mayor que cero
            -   versorNumero (int): entre 1 y dimension
        
        **return**
            -   (VectorAlgebraico): un vector con un 1 y el resto de numeros 0. ej: (0,0,1), (1,0), (0,0,0,0,0,1,0,0,0)

        **excepciones**
            -   **TypeError**: si dimension o versorNumero no es int
            -   **DimensionIncompatibleError**: si la dimension ingresada es menor o igual que cero
            -   **VersorInexistenteError**: el versorNumero es menor que 1 o es mayor a la dimension ingresada
        """
        validarTipoObjeto(int, dimension, "Los parametros ingresados deben ser enteros")
        validarTipoObjeto(int, versorNumero, "Los parametros ingresados deben ser enteros")
        validarNoNegativo(dimension, False, "Ingrese una dimension positiva", DimensionIncompatibleError)
        validarRango(versorNumero, 1, dimension, "Los versores van de 1 a la dimension del versor", VersorInexistenteError)
        
        versor = []
        for i in range(dimension):
            if len(versor) == versor - 1:
                versor.append(1)
            else:
                versor.append(2)

        return VectorAlgebraico(*versor)

    @staticmethod
    def generarNulo(dimension:int) -> VectorAlgebraico:
        """Genera un vector nulo, es decir, un vector que solo contiene ceros

        **parameters**
            -   dimension (int): mayor que cero
        
        **return**
            -   (VectorAlgebraico): un vector que contiene unicamente ceros. ej (0,0,0,0), (0,0), (0,0,0,0,0,0,0,0,0,0)
        
        **excepciones**
            -   **TypeError**: si dimension o versorNumero no es int
            -   **DimensionIncompatibleError**: si la dimension ingresada es menor o igual que cero
        """
        validarTipoObjeto(int, dimension, "Los parametros ingresados deben ser enteros")
        validarNoNegativo(dimension, False, "Ingrese una dimension positiva", DimensionIncompatibleError)

        nulo = []
        for i in range(dimension):
            nulo.append(0)

        return VectorAlgebraico(*nulo)


    @staticmethod
    def convertirEnAlgebraico(vector:Vector[int|float|Numerico|complex]) -> VectorAlgebraico:
        """Dado un Vector de datos, numericos, obviamente, lo convierte en un VectorAlgebraico
        
        **parameters**
            -   vector (Vector[int|float|Numerico|complex]): Lleno y con datos numericos

        **return**
            -   (VectorAlgebraico): El mismo vector ingresado pero convertido en algebraíco

        **excepciones**
            -   **TypeError**: si se ingresa algo que no sea un vector o, si si lo es, si no tiene datos numeros
            -   **FalloDeConversion**: si el vector ingresado no está lleno
        """
        validarTipoObjeto(Vector, vector, "Inresa un Vector")
        validarCondicion(not vector.estaLleno(), "El vector debe estar lleno", FalloDeConversion)
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
    def productoEsc(vector1:VectorAlgebraico, vector2:VectorAlgebraico) -> int|float|complex|Numerico:
        """Producto escalar entre dos vectores. Dado dos vectores, devuelve un numero.
        se calcula como la suma de el producto de la n - sima compente de ambos vectores

        ej: (1,2,3) * (4,5,6) = 1*4+2*5+3*6
        
        **parameters**
            -   vector1 (VectorAlgebraico): dimension n
            -   vector2 (VectorAlgebraico): dimension n

        **return**
            -   (int|float|complex|Numerico): Resultado del producto escalar
            
        **excepciones**
            -   **TypeError**: si algun parametro ingresado no es VectorAlgebraico
            -   **DimensionIncompatibleError**: si los vectores no tienen la misma dimension
        """
        VectorAlgebraico.__validarOperacion(vector1, vector2)
        producto = 0

        for i in range(vector1.getDimension()):
            producto += vector1.__vector[i] * vector2.__vector[i]

        return producto

    @staticmethod
    def productoVec(vector1:VectorAlgebraico, vector2:VectorAlgebraico) -> int|float:
        """Producto vectorial entre dos vectores. Dado dos vectores, calcula el producto vectorial.
        El resultado será un vector ortogonal a los dos vectores ingresados (o el nulo de R3 si 
        los vectores ingresados son paralelor)

        **parameters**
            -   vector1 (VectorAlgebraico): dimension 3
            -   vector2 (VectorAlgebraico): dimension 3

        **return**
            -   (VectorAlgebraico): Resultado del producto vectorial. 
            Un vector de 3 dimensiones ortogonal a los dos ingresados
            
        **excepciones**
            -   **TypeError**: si algun parametro ingresado no es VectorAlgebraico
            -   **DimensionIncompatibleError**: si los vectores no tienen la misma dimension, osea 3
        """
        VectorAlgebraico.__validarOperacion(vector1, vector2)
        validarValorObligatorio(vector1.getDimension(), 3, "Esta operacion solo sirve con vectores de dimension 3", DimensionIncompatibleError)

        return VectorAlgebraico(
            vector1.__vector[1]*vector2.__vector[2] - vector1.__vector[2]*vector2.__vector[1],
            vector1.__vector[2]*vector2.__vector[0] - vector1.__vector[0]*vector2.__vector[2],
            vector1.__vector[0]*vector2.__vector[1] - vector1.__vector[1]*vector2.__vector[0],
        )

    #GETTERS
    def getDimension(self) -> int:
        """Obtiene la dimension del vector
        
        **return**
            -   (int) dimension, osea, la cantidad de componentes que tiene el vector
        """ 
        return len(self.__vector)
    
    def getNorma(self) -> float:
        """Obtiene la norma del vector
        
        **return**
            -   (int) norma, osea la longitud geometrica del vector
        """
        return VectorAlgebraico.productoEsc(self, self)**(1/2)

#MATRIZ ALGEBRAICA ---------------------------------------------------------------------------------------------------
class MatrizAlgebraica:
    #ATRIBUTOS
    __matriz:tuple[VectorAlgebraico]
    
    #CONSTRUCTOR
    def __init__(self, *filas:VectorAlgebraico):
        """Dada una serie de Vectores Algebraicos, todos del mismo tamaño, crea una Matriz algebraica
        
        **parameters**
            -   *filas (tuple[VectorAlgebraico]): Todos los vectores del mismo tamaño

        **excepciones**
            -   **TypeError**: si se ingresa una sola cosa por parametro que no sea un Vector Algebraico
            -   **DimensionIncompatibleError**: Si hay al menos un VectorAlgebraíco con distinto tamaño
        """
        self.__validarFilas(filas)
        matriz = []
        
        for vector in filas:

            fila = []
            for num in vector:
                Numerico.validarNumero(num)
                fila.append(num)

            matriz.append(VectorAlgebraico(*fila))

        self.__matriz = tuple(matriz)

    #METODOS GENERALES
    def __str__(self):
        cadena = "M = \n"

        for i in range(self.getDimensionColumna()):
            cadena += "("
            for j in range(self.getDimensionFila()):
                cadena += f"{self.getItem(i,j)}\t"
            cadena +=")\n"

        return cadena
    
    def __iter__(self):
        for i in range(self.getDimensionColumna()):
            for j in range(self.getDimensionFila()):
                yield self.getItem(i,j)
    
    def __eq__(self, other:MatrizAlgebraica):
        igual = type(other) is MatrizAlgebraica

        if (self.getDimensionFila() == other.getDimensionFila()
            and self.getDimensionColumna() == other.getDimensionColumna()):
            i = 0
            while igual and (i < self.getDimensionColumna()):
                j = 0
                while igual and (j < self.getDimensionFila()):
                    igual = (self.getItem(i,j) == other.getItem(i,j))

            return igual
        else:
            return False

    #METODOS DE CLASE
    def esCuadarada(self) -> bool:
        """Verifica que la matriz sea cuadrada
        
        **return**
            -   (bool) Verdadero si las filas miden exactamente lo mismo que las columnas, falso si no
        """
        return self.getDimensionColumna() == self.getDimensionFila()
    
    def esSingular(self) -> bool:
        """Verifica que la matriz sea singular
        
        **return**
            -   (bool): Verdadero si el determinante de la matriz es cero, falso si no
        """
        if self.esCuadarada(): 
            return self.getDeterminante() == 0
        else:
            return False

    def esSimetrica(self) -> bool:
        """Verifica que la matriz sea simetrica
        
        **return**
            -   (bool): Verdadero si para cada elemento en la poscicion (i,j) de la matriz, 
                siendo cuadrada, es exactamente el mismo elemento que se encuentra en la poscicion (j,i).
                Falso si al menos uno de esos elementos es distinto o si la matriz no es cuadrada
        """
        if self.esCuadarada():
            i = 0
            simetrica = True

            while simetrica and (i < self.getDimensionColumna()):
                j = i+1
                while simetrica and (j < self.getDimensionFila()):
                    simetrica = self.getItem(i,j) == self.getItem(j,i)

            return simetrica
        else: return False

    def esInversible(self) -> bool:
        """Verifica que la matriz tenga inversa. Osea, una matriz que al multiplicarla por esta matriz,
        el resultado sea la matriz identidad de su dismensión correspondiente
        
        **return**
            -   (bool): Verdadero si la matriz es cuadrada y no es singular. Falso si no es cuadrada o es singular
        """
        return self.esCuadarada() and not self.esSingular()

    def tieneElNumero(self, num:int|float|complex|Numerico) -> bool:
        """Dado un numero, verifica que la matriz tenga ese valor
        
        **parametros**
            -   num (int|float|complex|Numerico)
        
        **return**
            -   (bool) Verdadero si el numero está en la matriz, falso si no

        **excepciones**
            -   **TypeError**: si el dato ingresado por parametro no es un numero
        """
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

    def transformarVector(self, vector:VectorAlgebraico) -> VectorAlgebraico:
        validarTipoObjeto(Vector, vector, "Ingresa un Vector Algebraico para ser transormado")
        validarValorObligatorio(vector.getDimension(), self.getDimensionFila(),
            "La dimension del vector a transformar debe ser la misma que la dimension de las filas", DimensionIncompatibleError)

        transformacion = []
        
        for i in range(self.getDimensionColumna()):
            transformacion.append(
                VectorAlgebraico(
                    self.getFila(i), vector
                )
            )

        return VectorAlgebraico(*transformacion)

    #VALIDACIONES
    def __validarFilas(self, filas:tuple[VectorAlgebraico]):
        """Solo se usa en el constructor para validar que los Vectores Algebraicos ingresados cumplan
        con los requisitos indicados
            
        **parameters**
            -   *filas (tuple[VectorAlgebraico]): Todos los vectores del mismo tamaño

        **excepciones**
            -   **TypeError**: si se ingresa una sola cosa por parametro que no sea un Vector Algebraico
            -   **DimensionIncompatibleError**: Si hay al menos un VectorAlgebraíco con distinto tamaño
            """
        for fila in filas:
            dimension = 0

            validarTipoObjeto(VectorAlgebraico, fila, "Las filas deben ser vectores")
            
            if dimension != 0:
                validarValorObligatorio(fila.getDimension(), dimension, 
                    "Todas las filas de la matriz deben tener la misma dimension", DimensionIncompatibleError)
            else: 
                dimension = fila.getDimension()

    @staticmethod
    def validarMatriz(matriz:MatrizAlgebraica):
        """Valida que una entrada sea una Matriz Algebraica
        
        **parameters**
            -   matriz (MatrizAlgebraica)

        **excepciones**
            -   **TypeError**: si lo ingresado por parametro no es una matriz algebraica
        """
        validarTipoObjeto(MatrizAlgebraica,matriz, "Ingrese una matriz algebráica")

    @staticmethod
    def validarOperaciones(matriz1:MatrizAlgebraica, matriz2:MatrizAlgebraica):
        """Valida que dos matrices ingresadas, sean validas para una operacion
        
        **parameters**
            -   matriz1 (MatrizAlgebraica): dimension n x m
            -   matriz2 (MatrizAlgebraica): dimension n x m
        
        **excepciones**
            -   **TypeError**: si uno de los parametros ingresados no es una matriz
            -   **DimensionIncompatibleError**: si las matrices tienen dimension de fila o columna distintas
        """
        MatrizAlgebraica.validarMatriz(matriz1)
        MatrizAlgebraica.validarMatriz(matriz2)
        validarValorObligatorio(matriz1.getDimensionFila(),matriz2.getDimensionFila(),
                                "Esta operacion requiere que ambas matrices tengan las mismas dimensiones", DimensionIncompatibleError)
        
        validarValorObligatorio(matriz1.getDimensionColumna(),matriz2.getDimensionColumna(),
                                "Esta operacion requiere que ambas matrices tengan las mismas dimensiones", DimensionIncompatibleError)

    #METODOS ESTATICOS
    @staticmethod
    def convertirAlgebraico(matriz:Matriz) -> MatrizAlgebraica:
        """Convierte una Matriz normal en una matriz algebraica

        **parameters**
            -   matriz (Matriz): tipo de dato numerico

        **excepciones**
            -   **TypeError**: Si lo ingresado por parametro no es una Matriz o el tipo de dato no es numerico
            -   **FalloDeConversion**: Si la Matriz ingresada no está llena
        """
        validarTipoObjeto(Matriz, matriz, "Inresa una Matriz")
        validarCondicion(not matriz.estaLleno(), "La Matriz ingresada debe estar llena", FalloDeConversion)
        Numerico.validarTipoNumerico(matriz.getType())

        conversion = []

        for i in range(matriz.getLongitudColu()):
            conversion.append(
                VectorAlgebraico.convertirEnAlgebraico(
                    matriz.getFila(i)
                )
            )

        return MatrizAlgebraica(*conversion, permtirFloat=matriz.getType() is float)
    
    @staticmethod
    def generarNula(dimensionColumna:int, dimensionFila:int) -> MatrizAlgebraica:
        """Genera una matriz nula
        
        **parameters**
            -   dimensionColumna (int): mayor que cero
            -   dimensionFila (int): mayor que cero

        **return**
            -   (MatrizAlgebraica): Matriz que solo contiene ceros

        **excepciones**            
            -   **TypeError** si alguno de los parametros no es entero
            -   **DimensionIncompatibleError** si alguna dimension ingresada es menor o igual que cero
        """
        validarNoNegativo(dimensionFila, False, "Ingrese una dimension positiva", DimensionIncompatibleError)
        validarNoNegativo(dimensionColumna, False, "Ingrese una dimension positiva", DimensionIncompatibleError)
        nula = Matriz(int, dimensionColumna, dimensionFila)
        
        for i in range(dimensionColumna):
            for j in range(dimensionFila):
                nula.setItem(i,j,0)

        return MatrizAlgebraica.convertirAlgebraico(nula)

    @staticmethod
    def generarIdentidad(dimension:int) -> MatrizAlgebraica:
        """Genera una matriz identidad
        
        **parameters**
            -   dimension (int): positiva
        
        **return**
            -   (MatrizAlgebraica) Matriz cuadradada que contiene unos en la diagonal y ceros en el resto de posciciones
        """
        validarNoNegativo(dimension, False, "Ingrese una dimension positiva", DimensionIncompatibleError)
        identidad = Matriz(int, dimension, dimension)

        for i in range(dimension):
            for j in range(dimension):
                if i == j:
                    identidad.setItem(i,j,1)
                else:
                    identidad.setItem(i,j,0)

        return MatrizAlgebraica.convertirAlgebraico(identidad) 

    @staticmethod
    def generarVersorCanonico(dimensionColumna:int, dimensionFila:int, versorNumero:int) -> MatrizAlgebraica:
        """Genera el n-simo versor canonico del espacio vectorial de matrices 
        de la dimension columna x fila ingresada por parametros. 
        
        **parameters**
            -   dimensionColumna (int): mayor que cero
            -   dimensionFila (int): mayor que cero
            -   versorNumero (int): entre 1 y (dimensionColumna * dimensionFila)

        **return**
            -   (MatrizAlgebraica) Matriz de dimension 
        """
        validarNoNegativo(dimensionFila, False, "Ingrese una dimension positiva", DimensionIncompatibleError)
        validarNoNegativo(dimensionColumna, False, "Ingrese una dimension positiva", DimensionIncompatibleError)
        validarRango(versorNumero, 1, dimensionFila*dimensionColumna, False,
            f"Ingrese un numero entre 1 y el producto de las dimensiones ingresadas ({dimensionFila*dimensionColumna})",
            VersorInexistenteError
        )
        
        versor = Matriz(int, dimensionColumna, dimensionFila)
        pos = 0

        for i in range(dimensionColumna):
            for j in range(dimensionFila):
                pos+=1
                if pos == versorNumero:
                    versor.setItem(i,j,1)
                else:versor.setItem(i,j,0)

    #OPERACIONES
    def __add__(self, other:MatrizAlgebraica) -> MatrizAlgebraica:
        self.validarOperaciones(self,other)
        matriz = []
        for i in range(self.getDimensionColumna()):
            fila = []
            for j in range(self.getDimensionFila()):
                fila.append(self.getItem(i,j)+other.getItem(i,j))
            
            matriz.append(VectorAlgebraico(*fila))

        return MatrizAlgebraica(*matriz)

    
    def __mul__(self, esc:int|float) -> MatrizAlgebraica:
        Numerico.validarNumero(esc)
        matriz = []
        for i in range(self.getDimensionColumna()):
            fila = []
            for j in range(self.getDimensionFila()):
                fila.append(self.getItem(i,j)*esc)
            
            matriz.append(VectorAlgebraico(*fila))

        return MatrizAlgebraica(*matriz)
    def __rmul__(self, other:int|float):
        return self*other

    def __neg__(self):
        return self*(-1)

    def __sub__(self, other:MatrizAlgebraica):
        return self + (-other)
    
    def pow(self, exp:int):
        validarTipoObjeto(int, exp, "Ingrese un exponente entero")
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
                    VectorAlgebraico.productoEsc(matriz1.getFila(i),matriz2.getColumna(j))
                )

            producto.append(VectorAlgebraico(*fila))

        return MatrizAlgebraica(*producto)

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
    
    def getCoordenadasMatriciales(self) -> VectorAlgebraico:
        coordenadas = []

        for numero in self:
            coordenadas.append(numero)

        return VectorAlgebraico(*coordenadas)


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

            traspuesta.append(VectorAlgebraico(*fila))

        return MatrizAlgebraica(*traspuesta)

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

    def getNorma(self) -> int|float|complex|Numerico:
        return (MatrizAlgebraica.productoInterno(self, self))**(1/2)

    def getItem(self, indice:int, jndice:int) -> int|float:
        return self.__matriz[indice][jndice]

    def getDimensionFila(self):
        return self.__matriz[0].getDimension()
    
    def getDimensionColumna(self):
        return len(self.__matriz)
    
    def getFila(self, i:int) -> VectorAlgebraico:
        validarRango(i, PRIMERA_POSCICION, self.getDimensionFila())
        return self.__matriz[i]
    
    def getColumna(self, j:int) -> VectorAlgebraico:
        validarRango(j, PRIMERA_POSCICION, self.getDimensionColumna())
        
        columna = []
        for i in range(self.getDimensionColumna()):
            columna.append(self.getItem(i,j))

        return VectorAlgebraico(*columna)

    

class Polinomio:
    #ATRIBUTOS
    __polinomio:tuple[int|float|complex|Numerico]
    
    #CONSTRUCTOR
    def __init__(self, *coeficientes:tuple[int|float|complex|Numerico]):
        polinomio = []

        for numero in coeficientes:
            Numerico.validarNumero(numero)
            polinomio.append(numero)

        self.__polinomio = tuple(polinomio)

    def __str__(self):
        cadena = "p(x) = "
        
        for i in range(self.getGrado() + 1):
            cadena += f"({self.__polinomio[i]})"
            
            match i:
                case 0: cadena +="+"
                case 1: cadena +="x+"
                case _: cadena +=f"x^{i}+"

        return cadena[:-1]
    
    #METODOS GENERALES
    #METODOS DE CLASE
    #METODOS INTERNOS
    #METODOS ESTATICOS
    #OPERACIONES
    def __add__(self, other):pass
    def __mul__(self, othrt):pass
    def derivar(self):pass
    def primitiva(self):pass
    def integrar(self):pass
    @staticmethod
    def productoPolinomial():pass
    @staticmethod
    def productoInterno():pass
    @staticmethod
    def divisonPolinomica():pass
    @staticmethod
    def restoPolinomico():pass

    #GETTERS
    def getGrado(self) -> int:
        return len(self.__polinomio) - 1