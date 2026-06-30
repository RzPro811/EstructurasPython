class DimensionIncompatibleError(RuntimeError):
    def __init__(self, *args):
        """Usar si dos elementos algebráicos pertenecen a distitas dimensiones"""
        super().__init__(*args)