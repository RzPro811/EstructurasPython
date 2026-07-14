class DimensionIncompatibleError(RuntimeError):
    def __init__(self, *args):
        """Usar si dos elementos algebráicos pertenecen a distitas dimensiones"""
        super().__init__(*args)

class NoCuadraEstaMatriz(RuntimeError):
    def __init__(self, *args):
        """Usar si la operacion requiere una matriz cuadrada, pero no se está usando una"""
        super().__init__(*args)

class VersorInexistenteError(RuntimeError):
    def __init__(self, *args):
        """Usar si se quiere generar un versor pero se hace mal"""
        super().__init__(*args)

class FalloDeConversion(RuntimeError):
    def __init__(self, *args):
        """Usar si hay un fallo en la conversion de un Vector o Matriz a algebraico"""
        super().__init__(*args)