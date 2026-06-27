class AdyacenciaError(RuntimeError):
    def __init__(self, *args):
        """Usar si hay un error relacionado a la adyacencia entre vertices"""
        super().__init__(*args)

class VerticeDobleError(RuntimeError):
    def __init__(self, *args):
        """Usar cuando se agregan un mismo dato dos veces en un grafo"""
        super().__init__(*args)

class VerticeNoEncontradoError(RuntimeError):
    def __init__(self, *args):
        """Usar si no se encontró un vertice"""
        super().__init__(*args)

class TipoGrafoIncompatible(RuntimeError):
    def __init__(self, *args):
        """Usar si el tipo de grafo no es compatible con un metodo"""
        super().__init__(*args)

class PesoInvalido(RuntimeError):
    def __init__(self, *args):
        """Usar si se ingresa un valor de Peso invalido"""
        super().__init__(*args)