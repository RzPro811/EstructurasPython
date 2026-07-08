class DimensionIncompatibleError(RuntimeError):
    def __init__(self, *args):
        """Usar si dos elementos algebráicos pertenecen a distitas dimensiones"""
        super().__init__(*args)

class NoCuadraEstaMatriz(RuntimeError):
    def __init__(self, *args):
        """Usar si la operacion requiere una matriz cuadrada, pero no se está usando una"""
        super().__init__(*args)