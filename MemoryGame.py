from Jugador import Jugador

class MemoryGame:
    def __init__(self):
        self.board = self.inicializarTablero()
        self.jugador1 = Jugador("Jugador 1")
        self.jugador2 = Jugador("Jugador 2")
        self.jugadores = [self.jugador1, self.jugador2]
        self.turno_actual = 0


    def inicializarTablero(self):
        board = []
        for _ in range(6):
            row = ["" for _ in range(6)]
            board.append(row)
        return board

    def obtener_jugador_actual(self):
        """Devuelve el jugador cuyo turno es actualmente."""
        return self.jugadores[self.turno_actual]

    def cambiar_turno(self):
        """Cambia el turno entre los jugadores."""
        self.turno_actual = 1 - self.turno_actual

    def reiniciar(self):
        """Reinicia el juego."""
        self.__init__()