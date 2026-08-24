class Incomparable(RuntimeError):
    def __init__(self, *args):
        """Usar si el objeto en una lista o vector, el tipo de objeto es incomparable"""
        super().__init__(*args)

class GeneracionNegativaError(RuntimeError):
    def __init__(self, *args):
        """Usar si al generar una lista o vector se genera con un numero negativo"""
        super().__init__(*args)

class MaximoMinimoIntercambiados(RuntimeError):
    def __init__(self, *args):
        """Usar si al generar una lista o vector, el numero maximo que puede aparecer es menor al numero minimo"""
        super().__init__(*args)

class MalditoHereje(RuntimeError):
    def __init__(self, *args):
        """Esto es solo un chiste que se fue de mambo mambo omatsuri mambo"""
        super().__init__(*args)