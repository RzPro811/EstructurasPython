from .Validaciones import T, Generic, TypeStruct, validarTipo, validarRango, validarNoNegativo
from .Excepciones.Generales import *
from typing import Generator
from random import shuffle

class Vector(Generic[T], TypeStruct):
    #CONSTANTES
    __PRIMERA_POSCICION = 0

    #ATRIBUTOS
    __longitudOriginal: int
    __array: list[Generic[T]]

    #CONSTRUCTOR
    def __init__(self, tipo:type, longitud:int):
        super().__init__(tipo)
        self.__setLongitudOriginal(longitud)
        self.__array = self.__generarVector(longitud)

    #METODOS GENERALES
    def __str__(self) -> str:
        cadena = "< "

        for item in self:
            cadena += f"{item}, "

        return cadena[:-2] + " >"
        
    def __len__(self) -> int:
        return len(self.__array)
    
    def __iter__(self) -> Generator[Generic[T]] :
        for item in self.__array:
            yield item

    def __getitem__(self, key:int) -> Generic[T]:
        self.__validarIndice(key)
        return self.__array[key]
    
    def __setitem__(self, key:int, value:Generic[T]):
        self.__validarIndice(key)
        self.validarEntrada(value)
        self.__array[key] = value

    #METODOS DE CLASE
    def estaVacio(self):
        return self.getCantidadElementos() == 0
    
    def agregar():
        pass

    def quitar():
        pass

    def remover():
        pass

    def intercambiar(self, indice:int, jndice:int):
        self.__validarIndice(indice)
        self.__validarIndice(jndice)

        aux = self[indice]
        self[indice] = self[jndice]
        self[jndice] = aux

    def mezclar(self):
        shuffle(self.__array) 

    #METODOS INTERNOS
    def __generarVector(self, longitud:int) -> list[Generic[T]]:
        return [None]*longitud

    def __expandir():
        pass
    def __contraer():
        pass

    #VALIDACIONES
    def __validarIndice(self, indice:int):
        validarRango(indice, Vector.__PRIMERA_POSCICION,self.__getPoscicionFinal(),
                     mensaje= f"Ingresa un valor entre {Vector.__PRIMERA_POSCICION} y {self.__getPoscicionFinal()}")

    #GETTERS

    #Atributos Calculables
    def getLongitud(self) -> int:
        return len(self)

    def getCantidadElementos(self) -> int:
        elementos = 0

        for item in self:
            if item is not None:
                elementos +=1
        
        return elementos

    def __getPoscicionFinal(self) -> int:
        return self.getLongitud() - 1


    #Atributos reales
    def __getLongitudOriginal(self) -> int:
        return self.__longitudOriginal
    

    #SETTERS
    def __setLongitudOriginal(self, longitud:int):
        validarNoNegativo(longitud,False, "Ingrese una longitud positiva", LongitudNegativaError)
        self.__longitudOriginal = longitud


#MATRIZ-----------------------------------------------------------------------------------------------------------------------------------------
#LISTA------------------------------------------------------------------------------------------------------------------------------------------
#COLA-------------------------------------------------------------------------------------------------------------------------------------------
#PILA-------------------------------------------------------------------------------------------------------------------------------------------
#HEAP-------------------------------------------------------------------------------------------------------------------------------------------
