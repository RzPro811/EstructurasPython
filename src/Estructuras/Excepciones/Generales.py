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

class MetodoInvalidoError(RuntimeError):
    def __init__(self, *args):
        """Usar cuando un metodo es invalido"""
        super().__init__(*args)

class ImplosionError(RuntimeError):
    def __init__(self, *args):
        """Usar para expansiones en negativo (tenes que verlo para entenderlo)"""
        super().__init__(*args)