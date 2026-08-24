from typing import Generic, TypeVar
from enum import Enum

T = TypeVar("T")

PRIMERA_POSCICION = 0
NO_ENCONTRADO = -1
#CLASES DE VERIFICACION -----------------------------------------------------------------------------------
class FalloValidacion(Exception):
    def __init__(self, *args):
        """Usar cuando falla la validacion"""
        super().__init__(*args)

#VALIDACIONES OMNICIENTES --------------------------------------------------------------------------------
def crearMensaje(default:str, reemplazo:str = None) -> str:
    """Crea el mensaje por default para la validacion

    **parameters**:
        -   default (str): mensaje por defecto
        -   reemplazo (str): mensaje por el cual se reemplaza el mensaje por default (none por defecto)

    **return**:
        -   (str) mensaje para la validacion
    
    **excepciones**:
        -   **FalloValidacion** si ninguo de los parametros es string o None   
    """
    if reemplazo is None:
        if default is not None:
            if not isinstance(default, str):
                raise FalloValidacion("Ingrese un mensaje valido")
        return default
    else:
        if not isinstance(reemplazo, str):
            raise FalloValidacion("Ingrese un mensaje valido")
        return reemplazo
    
def validarError(error:Exception):
    """Valida que se haya ingresado un error para la validación
    
    **parameters**:
        -   error (type) hereda de Exception

    **excepciones**:
        -   **FalloValidacion**: si el error ingresado no es un tipo heredado de Exception, osea, no es un error
    """
    if not issubclass(error, Exception):
        raise FalloValidacion("Ingrese un error que sea valido")
    

#VALIDACIONES MENORES ------------------------------------------------------------------------------------

def validarTipo(tipo:type, mensaje:str = None, error:Exception = TypeError):
    """Valida que se haya ingresado un tipo type, o enum
    
    **parameters**:
        -   **tipo** (type): tipo que se validara si es tipo
        -   **mensaje** (str): mensaje que se emitirá al saltar error, por defecto None
        -   **error** (Exception): por defecto TypeError
    **excepciones**:
        -   **FalloValidacion**: si no se cumplen con las condiciones previamente establecidas
    """
    mensaje = crearMensaje("Ingresa un tipo type", mensaje)
    validarError(error)
    
    if not isinstance(tipo, type) and not isinstance(tipo, Enum):
        raise error(mensaje)

def validarTipoObjeto(tipo:type, objeto:T, mensaje:str = None, error:Exception = TypeError):
    """Valida que un objeto sea de un tipo ingresado
    
    **parameters**:
        -   tipo (type)
        -   objeto (Generic): debe ser del tipo ingresado por parametro
        -   mensaje (str): por defecto None
        -   error (Exception): por defecto TypeError

    **excepciones**:
        -   **FalloValidacion**: si no se cumplen con las condiones previamente establecidas
    """
    
    validarError(error)
    validarTipo(tipo, "ingresa un tipo type", FalloValidacion)
    mensaje = crearMensaje("Ingresa un objeto del tipo "+tipo.__name__, mensaje)

    if not isinstance(objeto, tipo):
        raise error(mensaje)
    
def ValidarTipoUnico(iterable, mensaje:str = "Ingresa una lista de elementos del mismo tipo", error:Exception = TypeError):
    crearMensaje(mensaje)
    validarError(error)

    tipo = None
    for item in iterable:
        if tipo is None:
            tipo = type(item)
        else:
            validarTipoObjeto(tipo,item,mensaje,error)

    return tipo

def validarVariosTipos(objeto:T, *tipos:type, mensaje:str = None, error:Exception = TypeError):
    """"""
    validarError(error)
    mensaje = crearMensaje("El objeto inresado no es de ningun tipo ingresado",mensaje)
    validarTipoObjeto(type, tipos[0], "Ingresa tipos de objetos", FalloValidacion)
    ValidarTipoUnico(tipos, "Inrgesa tipos de objetos", FalloValidacion)

    lanzarError = True
    i = 0
    while (i < len(tipos)) and lanzarError:
        lanzarError = not isinstance(objeto, tipos[i])
        i+=1

    if lanzarError:
        raise error(mensaje)

def validarTiposPorHerencia(hijo:type, *padres:tuple[type], mensaje:str = None, error:Exception = TypeError):
    validarError(error)
    mensaje = crearMensaje(mensaje, f"Ingresa un tipo que herede de {padres}")

    if not issubclass(hijo, padres):
        raise error(mensaje)
    
def validarNoNegativo(numero: int, incluyeCero:bool = True, mensaje:str = None, error:Exception = ValueError):
    """Valida que un numero ingresado no sea un valor negativo
    
    **parameters**:
        -   **numero** (int): mayor o igual que cero
        -   **incluyeCero** (bool): por defecto true. Si es false, se verificará que el numero tampoco sea cero
        -   **mensaje** (str): por defecto None
        -   **error** (Exception): por defecto ValueError

    **excepciones**:
        -   **FalloValidacion**: si no se cumplen con las condiones previamente establecidas
    """
    validarError(error)
    mensaje = crearMensaje("Ingresa un valor positivo", mensaje)
    validarTipoObjeto(int, numero, "El numero ingresado no es entero", FalloValidacion)
    validarTipoObjeto(bool, incluyeCero, "La condicion incluye cero no es booleana", FalloValidacion)

    if incluyeCero: 
        if (numero < 0):
            raise error(mensaje)
    else:
        if (numero <= 0):
            raise error(mensaje)

def validarOrden(numeroMenor:int, numeroMayor:int, mensaje:str = None, error:Exception = ValueError):
    """Dado dos numeros enteros, valida que el primer numero sea menor que el segundo
    
    **parameters**:
        -   **numeroMenor** (int): menor que el siguiente
        -   **numeroMayor** (int): mayor que el anterior
        -   **mensaje** (str): por defecto None
        -   **error** (Exception): por defecto ValueError

    **excepciones**:
        -   **FalloValidacion**: si no se cumplen con las condiones previamente establecidas
    """
    validarError(error)
    mensaje = crearMensaje("Ingrese un numero valido")
    validarTipoObjeto(int, numeroMenor, "El parametro ingresado no es un numero entero",FalloValidacion)
    validarTipoObjeto(int, numeroMayor, "El parametro ingresado no es un numero entero",FalloValidacion)

    if (numeroMenor > numeroMayor):
        raise error(mensaje)

def validarRango(valor:int, minimo:int, maximo:int, incluyeExtremos:bool = True, mensaje:str = None, error:Exception = IndexError):
    """Dado dos numeros enteros, valida que el primer numero sea menor que el segundo
    
    **parameters**:
        -   **valor** (int)
        -   **minimo** (int): menor que el maximo
        -   **maximo** (int): mayor que el minimo
        -   **mensaje** (str): por defecto None
        -   **error** (Exception): por defecto ValueError

    **excepciones**:
        -   **FalloValidacion**: si no se cumplen con las condiones previamente establecidas
    """
    validarError(error)
    mensaje = crearMensaje(f"Ingrese un numero entre {minimo} y {maximo}", mensaje)
    validarTipoObjeto(int, valor , "Ingrese un numero entero por parametro", FalloValidacion)
    validarTipoObjeto(int, minimo, "Ingrese un numero entero por parametro", FalloValidacion)
    validarTipoObjeto(int, maximo, "Ingrese un numero entero por parametro", FalloValidacion)
    validarTipoObjeto(bool, incluyeExtremos, "La condicion ingresada no es un booleano", FalloValidacion)
    validarOrden(minimo, maximo, "El parametro maximo es menor que el parametro minimo", FalloValidacion)

    if incluyeExtremos:
        if (valor < minimo) or (valor > maximo):
            raise error(mensaje)
    else:
        if (valor <= minimo) or (valor >= maximo):
            raise error(mensaje)

def validarCondicion(condicion:bool, mensaje:str = None, error:Exception = RuntimeError):
    """Dada una condicion, si es verdadera, lanza error
    
    **parameters**
        -   **condicion** (bool): si es verdadero, lanza error
        -   **mensaje** (str): por defecto None
        -   **error** (Exception): por defecto RuntimeError

    **excepciones**:
        -   **FalloValidacion**: si no se cumplen con las condiones previamente establecidas
    """
    validarError(error)
    mensaje = crearMensaje(f"se ha hallado una condicion incompatible", mensaje)
    validarTipoObjeto(bool, condicion, "Ingresa una condicion booleana", FalloValidacion)

    if condicion: raise error(mensaje)

def validarMayorQue(valor:int, minimo:int, incluirExtremo:bool = True, mensaje = None, error:Exception = ValueError):
    validarError(error)
    mensaje = crearMensaje(f"ingrese un valor mayor que {minimo}", mensaje)
    validarTipoObjeto(int, valor , "Ingrese un numero entero por parametro", FalloValidacion)
    validarTipoObjeto(int, minimo , "Ingrese un numero entero por parametro", FalloValidacion)
    validarTipoObjeto(bool, incluirExtremo, "Ingresa una condicion booleana", FalloValidacion)

    if (valor <= minimo) and ((valor != minimo) or not incluirExtremo):
        raise error(mensaje)
   
def validarMenorQue(valor:int, maximo:int, incluirExtremo:bool = True, mensaje = None, error:Exception = ValueError):
    validarError(error)
    mensaje = crearMensaje(f"ingrese un valor menor que {maximo}", mensaje)
    validarTipoObjeto(int, valor , "Ingrese un numero entero por parametro", FalloValidacion)
    validarTipoObjeto(int, maximo, "Ingrese un numero entero por parametro", FalloValidacion)
    validarTipoObjeto(bool, incluirExtremo, "Ingresa una condicion booleana", FalloValidacion)

    if (valor >= maximo) and ((valor != maximo) or not incluirExtremo):
        raise error(mensaje)

def validarValorCompatible(valor:int, valorIncompatible:int, mensaje:str = None, error:Exception = ValueError):
    validarError(error)
    mensaje = crearMensaje(f"ingrese un valor distinto de {valorIncompatible}", mensaje)
    validarTipoObjeto(int, valor , "Ingrese un numero entero por parametro", FalloValidacion)
    validarTipoObjeto(int, valorIncompatible , "Ingrese un numero entero por parametro", FalloValidacion)
    
    if valor == valorIncompatible: raise error(mensaje)

def validarValorObligatorio(valor:int, valorObligatorio:int, mensaje:str = None, error:Exception = ValueError):
    validarError(error)
    mensaje = crearMensaje(f"ingrese un valor distinto de {valorObligatorio}", mensaje)
    validarTipoObjeto(int, valor , "Ingrese un numero entero por parametro", FalloValidacion)
    validarTipoObjeto(int, valorObligatorio , "Ingrese un numero entero por parametro", FalloValidacion)
    
    if valor != valorObligatorio: raise error(mensaje)

def validarNoNone(dato:T, mensaje:str = None, error:Exception = TypeError):    
    validarError(error)
    mensaje = crearMensaje(f"ingrese un valor distinto de None", mensaje)
    
    if dato is None:
        raise error(mensaje)

def filtrarElNulo(*datos:T) -> T:
    for item in datos:
        if item is not None: return item