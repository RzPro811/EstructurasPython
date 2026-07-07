class NodoInvalidoError(RuntimeError):
    def __init__(self, *args):
        """Usar cuando hay un Nodo que no es nodo realmente"""
        super().__init__(*args)

class ErrorCursorDesactivado(RuntimeError):
    def __init__(self, *args):
        """Usar cuando el cursor de la lista está desactivado"""
        super().__init__(*args)
    
class ErrorCursorEncendido(RuntimeError):
    def __init__(self, *args):
        """Usar cuando el cursor de la lista esté prendido"""
        super().__init__(*args)