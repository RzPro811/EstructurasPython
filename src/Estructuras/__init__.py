"""Paquete de Estructuras de Python, Hecho por RzPro para ustedes

Estructuras Incluidas:
    -   **Vector**
    -   **Matriz**
    -   **Lista**
    -   **Cola**
    -   **Pila**
    -   **Heap**
    -   **VectorAlgrebraico**
    -   **MatrizAlgebraica**
    -   **Ordenador**
    -   **Grafo**
    -   **Digrafo**

Validaciones Incluidas:
    -   **validarTipo**
    -   **validarVariosTipos**
    -   **ValidarTipoUnico**
    -   **validarNoNone**
    -   **validarValorCompatible**
    -   **validarValorObligatorio**
    -   **validarMenorQue**
    -   **validarMayorQue**
    -   **validarNoNegativo**
    -   **validarOrden**
    -   **validarRango**
    -   **validarCondicion**

Excepciones:
    -   **LlenoError**
    -   **VacioError**
    -   **ImplosionError**
    -   **MetodoInvalidoError**
    -   **LongitudNegativaError**
    -   **ErrorCursorDesactivado**
    -   **ErrorCursorEncendido**
    -   **TipoGrafoIncompatible**
    -   **OperacionGrafosInvalida**
    -   **AdyacenciaError**
    -   **VerticeDobleError**
    -   **VerticeNoEncontradoError**
    -   **NoCuadraEstaMatriz**
    -   **DimensionIncompatibleError**
    -   **Incomparable**
    -   **GeneracionNegativaError**
    -   **MaximoMinimoIntercambiados**

Extras:
    -   **Visualizador**
    -   **TypeStruct**
    -   **DataStruct**
    -   **Numerico**
    -   **FalloValidacion**
    -   **MalditoHereje**
"""

from .Heredables import TypeStruct, DataStruct
from .Lista import Lista
from .Vector import Vector, Matriz
from .__Grafo import Grafo, Digrafo
from .Ordenador import Ordenador, Visualizador
from .NoLineales import Cola, Pila, Heap
from .Validaciones import (FalloValidacion,
    validarTipo,
    validarVariosTipos,
    ValidarTipoUnico,
    validarNoNone,
    validarValorCompatible,
    validarValorObligatorio,
    validarMenorQue,
    validarMayorQue,
    validarNoNegativo,
    validarOrden,
    validarRango,
    validarCondicion,
)
from .Excepciones.Generales import LlenoError, VacioError, ImplosionError, MetodoInvalidoError, LongitudNegativaError
from .Excepciones.LinkedList import ErrorCursorDesactivado, ErrorCursorEncendido
from .Excepciones.Grafo import TipoGrafoIncompatible, OperacionGrafosInvalida, AdyacenciaError, VerticeDobleError, VerticeNoEncontradoError
from .Excepciones.Ordenador import Incomparable, GeneracionNegativaError, MaximoMinimoIntercambiados, MalditoHereje

__all__ = [
    "Lista", 
    "Vector",
    "Matriz", 
    "Grafo", 
    "Digrafo", 
    "Ordenador", 
    "Visualizador", 
    "Cola", 
    "Pila", 
    "Heap", 
    "TypeStruct", 
    "DataStruct",
    "validarTipo",
    "validarVariosTipos",
    "ValidarTipoUnico",
    "validarNoNone",
    "validarValorCompatible",
    "validarValorObligatorio",
    "validarMenorQue",
    "validarMayorQue",
    "validarNoNegativo",
    "validarOrden",
    "validarRango",
    "validarCondicion",
    "FalloValidacion",
    "LlenoError",
    "VacioError",
    "ImplosionError",
    "MetodoInvalidoError",
    "LongitudNegativaError",
    "ErrorCursorDesactivado",
    "ErrorCursorEncendido",
    "TipoGrafoIncompatible",
    "OperacionGrafosInvalida",
    "AdyacenciaError",
    "VerticeDobleError",
    "VerticeNoEncontradoError",
    "Incomparable",
    "GeneracionNegativaError",
    "MaximoMinimoIntercambiados",
    "MalditoHereje"
]

