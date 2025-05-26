from Jugador import Jugador

class MemoryGame:
    def __init__(self):
        self.root = None
        self.board = self.inicializarTablero()
        self.jugador1 = Jugador("Jugador 1")
        self.jugador2 = Jugador("Jugador 2")
        self.Primera_carta = None
        self.Primer_boton = None
        self.Segunda_carta = None
        self.Segundo_boton = None
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

    #Set de la primera carta

    def SetPrimeraCarta(self, imagen, casilla):
        self.Primera_carta = imagen
        self.Primer_boton = casilla

    # set de la segunda carta
    def SetSegundaCarta(self, imagen, casilla):
        self.Segunda_carta = imagen
        self.Segundo_boton = casilla

    #Set de root para utilizarlo con after luego
    def setRoot(self, root):
        self.root = root


    #Reinicar Cartas
    def ReiniciarCartas(self, TipoReinicio,imagenOculta):
        self.Primera_carta = None
        self.Segunda_carta = None

        if TipoReinicio == "Gane":
            pass
        elif TipoReinicio == "Fallo" :
            #Volver a ocultar cartas
            self.Primer_boton["boton"].config(image=imagenOculta)
            self.Primer_boton["revelado"] = False
            self.Segundo_boton["boton"].config(image=imagenOculta)
            self.Segundo_boton["revelado"] = False
            self.Primer_boton = None
            self.Segundo_boton = None

        

    #Deshabilitar o habilitar botones de acuerdo al turno


    def Actualizar_estado_botones(self, JugadorActual, botones_tablero1, botones_tablero2):
        #Obtener el nombre del jugador
        Nombre = JugadorActual.getNombre()
        self.cambiar_turno()

        #Desabilitar los botones del jugador que no tiene el turno y habilitar los botones del otro jugador
        if Nombre == "Jugador 1":
            for fila in botones_tablero1:
                for casilla in fila:
                    casilla["boton"].config(state="disabled")

            for fila in botones_tablero2:
                for casilla in fila:
                    casilla["boton"].config(state="normal")

        else:
            for fila in botones_tablero2:
                for casilla in fila:
                    casilla["boton"].config(state="disabled")

            for fila in botones_tablero1:
                for casilla in fila:
                    casilla["boton"].config(state="normal")




    def VerificaPareja(self,jugador, imagenOculta, botones_tablero1, botones_tablero2):
        JugadorActual = jugador
        if self.Primera_carta == self.Segunda_carta:
            JugadorActual.setParejasEncontradas()
            #self.ReiniciarCartas("Gane", imagenOculta)
            self.root.after(1000, lambda: self.ReiniciarCartas("Gane", imagenOculta))
            self.root.after(1500, lambda: self.Actualizar_estado_botones(JugadorActual,botones_tablero1, botones_tablero2))

            #Prints de prueba
            print("win")
            print(f"Fallos Jugador 1: {self.jugador1.getFallos()}")
            print(f"Fallos Jugador 2: {self.jugador2.getFallos()}")
            print(f"Wins Jugador 1: {self.jugador1.getParejasEncontradas()}")
            print(f"Wins Jugador 2: {self.jugador2.getParejasEncontradas()}")
            
        else:
            JugadorActual.setFallos()
            #self.ReiniciarCartas("Fallo", imagenOculta)
            self.root.after(1000, lambda: self.ReiniciarCartas("Fallo", imagenOculta))
            self.root.after(1500, lambda: self.Actualizar_estado_botones(JugadorActual,botones_tablero1, botones_tablero2))

            #Prints de prueba
            print("fail")
            print(f"Fallos Jugador 1: {self.jugador1.getFallos()}")
            print(f"Fallos Jugador 2: {self.jugador2.getFallos()}")
            print(f"Wins Jugador 1: {self.jugador1.getParejasEncontradas()}")
            print(f"Wins Jugador 2: {self.jugador2.getParejasEncontradas()}")

    

        