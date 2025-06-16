class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
class JugadorClasico(Jugador):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.turno = False  # Indica si es su turno
        self.ParejasEncontradas = 0
        self.Fallos = 0
        self.intentos = 0

    def getFallos(self):
        return self.Fallos
    
    def setFallos(self):
        self.Fallos += 1

    def getParejasEncontradas(self):
        return self.ParejasEncontradas
    
    def setParejasEncontradas(self):
        self.ParejasEncontradas += 1 

    def asignar_turno(self, turno): #Asigna si es su turno o no
        self.turno = turno

    def getTurno(self): #Set y get de turno
        return self.turno

    def setTurno(self, turno):
        self.turno = turno

    def getNombre(self):
        return self.nombre
    
    def incrementar_intentos(self): #Incrementa el número de intentos del jugador
        self.intentos += 1

    def getIntentos(self):
        return self.intentos
    
class JugadorPatrones(Jugador):
    def __init__(self,nombre):
        super().__init__(nombre)
        self.Secuencias = 0

    def AumentaSecuencia(self):
        self.Secuencias += 1
    
    def getSecuencias(self):
        return self.Secuencias
    
    def setSecuencias(self,num):
        self.Secuencias = num