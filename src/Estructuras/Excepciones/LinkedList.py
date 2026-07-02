class NodoInvalidoError(RuntimeError):
    def __init__(self, *args):
        """Usar cuando hay un Nodo que no es nodo realmente"""
        super().__init__(*args)