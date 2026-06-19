from Validaciones import T, Generic, TypeStruct, validarTipo, validarRango, validarNoNegativo
from Excepciones.Generales import *

class Vector(Generic[T], TypeStruct):
    #ATRIBUTOS
    __longitudOriginal: int
    __array: list[Generic[T]]

    #CONSTRUCTOR
    #METODOS GENERALES
    #METODOS DE CLASE
    #VALIDACIONES
    #GETTERS
    def __getLongitudOriginal(self) -> int:
        return self.__longitudOriginal
    
    #SETTERS
    def __setLongitudOriginal(self, longitud:int):
        validarNoNegativo(longitud,False, "Ingrese una longitud positiva")
