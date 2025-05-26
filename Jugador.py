class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.turno = False  # Indica si es su turno
        self.ParejasEncontradas = 0
        self.Fallos = 0

    def getFallos(self):
        return self.Fallos
    
    def setFallos(self):
        self.Fallos += 1

    def getParejasEncontradas(self):
        return self.ParejasEncontradas
    
    def setParejasEncontradas(self):
        self.ParejasEncontradas += 1 


    #Asigna si es su turno o no
    def asignar_turno(self, turno):
        """Asigna si es su turno o no."""
        self.turno = turno

    #Set y get de turno
    def getTurno(self):
        return self.turno

    def setTurno(self, turno):
        self.turno = turno

    def getNombre(self):
        return self.nombre