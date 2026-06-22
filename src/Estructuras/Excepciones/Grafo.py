class AdyacenciaError(RuntimeError):
    def __init__(self, *args):
        """Usar si hay un error relacionado a la adyacencia entre vertices"""
        super().__init__(*args)

