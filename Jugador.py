class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.turno = False  # Indica si es su turno

    def asignar_turno(self, turno):
        """Asigna si es su turno o no."""
        self.turno = turno

    def getTurno(self):
        return self.turno

    def setTurno(self, turno):
        self.turno = turno