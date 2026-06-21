class LongitudNegativaError(RuntimeError):
    def __init__(self, *args):
        """Usar si la longitud ingresada es negativa o cero"""
        super().__init__(*args)

class VacioError(RuntimeError):
    def __init__(self, *args):
        """Usar si tu estructura se queda vacía"""
        super().__init__(*args)

class LlenoError(RuntimeError):
    def __init__(self, *args):
        """Usar si tu estructura se llenó"""
        super().__init__(*args)