import tkinter as tk
from tkinter import messagebox
from Jugador import Jugador
import threading
import time

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
        self.tiempo_restante = 10
        self.ImagenOculta = None
        self.botones_tablero1 = None
        self.botones_tablero2 = None
        self.CantCartas = 0
        self.actualizar_marcadores = None
        self.CrearVentanaGane = None
        self.HayDosJugadores = True

        #Tiempo
        self.ejecutando = False
        self.hilo_cronometro = None
        self.cronometro_activo = True
        self.marcador_tiempo1 = None
        self.marcador_tiempo2 = None
        

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
        """Reinicia el juego"""

        #Reinicia variables principales
        self.board = self.inicializarTablero()
        self.detener_cronometro_completamente()
        self.jugador1 = Jugador("Jugador 1")
        self.jugador2 = Jugador("Jugador 2")
        self.Primera_carta = None
        self.Primer_boton = None
        self.Segunda_carta = None
        self.Segundo_boton = None
        self.jugadores = [self.jugador1, self.jugador2]
        self.turno_actual = 0
        self.tiempo_restante = 10
        self.HayDosJugadores = True

        # Reiniciar variables de cronómetro
        self.ejecutando = False
        self.hilo_cronometro = None
        self.cronometro_activo = True

    #SETS Y GETS
    #Cartas
    def SetPrimeraCarta(self, imagen, casilla):
        """Establece el boton y la imagen de la primera carta"""
        self.Primera_carta = imagen
        self.Primer_boton = casilla

    def SetSegundaCarta(self, imagen, casilla):
        """Establece el boton y la imagen de la segunda carta"""
        self.Segunda_carta = imagen
        self.Segundo_boton = casilla

    def AumentaCartas(self, cant):
        """Aumenta la cantidad de cartas reveladas"""
        self.CantCartas += cant

    def SetCartas(self, Cartas):
        """Establece la cantidad de cartas reveladas"""
        self.CantCartas = Cartas

    def getCantCartas(self):
        """Retorna la cantidad de cartas reveladas"""
        return self.CantCartas

    #Root
    def setRoot(self, root):
        """Establece root para ser utilizada en la clase"""
        self.root = root

    #Marcadores, tableros y ventanas
    def setMarcadores(self,Marcador1,Marcador2):
        """Establecemos los marcadores de tiempo"""
        self.marcador_tiempo1 = Marcador1
        self.marcador_tiempo2 = Marcador2

    def Recibir_ActualizarMarcadores(self,funcion):
        """Recibe la funcion para actualizar los marcadores"""
        self.actualizar_marcadores = funcion

    def setImagenOculta(self, Imagen):
        """Establece la imagen oculta (para botones)"""
        self.ImagenOculta = Imagen

    def setTableros(self, botones_tablero1, botones_tablero2):
        """Establece los botones de cada tablero"""
        self.botones_tablero1 = botones_tablero1
        self.botones_tablero2 = botones_tablero2

    def Recibir_VentanasGane(self,funcion):
        """Recibe la funcion de las ventanas del gane"""
        self.CrearVentanaGane = funcion


    #TIEMPO

    def iniciar_cronometro(self):
        """Inicia el cronometro del jugador actual"""
        # Detener cronómetro anterior completamente
        self.detener_cronometro_completamente()
        
        # Reiniciar el tiempo
        self.ejecutando = True

        #Crear Hilo
        self.hilo_cronometro = threading.Thread(target=self.ejecutar_cronometro)
        self.hilo_cronometro.daemon = True
        self.hilo_cronometro.start()


    def ejecutar_cronometro(self):
        """Permite que el tiempo avance, ejecutando el cronometro del jugador"""
        while self.ejecutando and self.tiempo_restante > 0:
            time.sleep(1)
            if self.ejecutando:
                self.tiempo_restante -= 1
                try:
                    if self.root and self.root.winfo_exists():
                        self.root.after(0, self.actualizar_display)
                except (tk.TclError, RuntimeError):
                    break 
        if self.tiempo_restante <= 0 and self.ejecutando:
            try:
                if self.root and self.root.winfo_exists():
                    self.root.after(0, self.tiempo_agotado)
            except (tk.TclError, RuntimeError):
                pass
    def actualizar_display(self):
        """Actualiza el tiempo en pantalla cada segundo"""
        if self.turno_actual == 0:
            self.marcador_tiempo1.config(text=f"Tiempo: {self.tiempo_restante}s")
        else:
            self.marcador_tiempo2.config(text=f"Tiempo: {self.tiempo_restante}s")
        
    def pausar_cronometro(self):
        self.ejecutando = False

    def tiempo_agotado(self):
        """Establece el fallo y reinicia los botones"""
        jugador_actual = self.obtener_jugador_actual()
        self.pausar_cronometro()
    
        #Reiniciar botones
        jugador_actual.setFallos()
        jugador_actual.incrementar_intentos()
        self.cambiar_turno()
        self.pausar_cronometro()
        self.root.after(1000, lambda: self.ReiniciarCartas("Tiempo Agotado"))
        self.root.after(1500, lambda: [
                self.Actualizar_estado_botones(jugador_actual),
                self.actualizar_marcadores()])  # Evento para actualizar marcadores
        self.CantCartas = 0

    def detener_cronometro_completamente(self):
        """Detiene completamente el cronómetro y limpia el hilo"""
        self.tiempo_restante = 10
        self.ejecutando = False
        if self.hilo_cronometro and self.hilo_cronometro.is_alive():
            self.hilo_cronometro.join()
        self.hilo_cronometro = None

    def Acierto(self):
        """Permite que el jugador siga jugando y suma 7 segundos a su cronometro"""
        if self.ejecutando:
            self.tiempo_restante += 7

        # Actualiza el cronometro en pantalla
        if self.root:
            self.root.after(0, self.actualizar_display)


    #Reiniciar Cartas
    def ReiniciarCartas(self, TipoReinicio):
        self.Primera_carta = None
        self.Segunda_carta = None

        if TipoReinicio == "Gane":
            pass
        elif TipoReinicio == "Fallo" :
            #Volver a ocultar cartas
            self.Primer_boton["boton"].config(image = self.ImagenOculta)
            self.Primer_boton["revelado"] = False
            self.Segundo_boton["boton"].config(image = self.ImagenOculta)
            self.Segundo_boton["revelado"] = False
            self.Primer_boton = None
            self.Segundo_boton = None
        else:
            #Oculta la primera carta
            self.Primer_boton["boton"].config(image = self.ImagenOculta)
            self.Primer_boton["revelado"] = False
            self.Primer_boton = None


    def Actualizar_estado_botones(self, JugadorActual):
        """Deshabilitar o habilitar botones de acuerdo al turno"""
        #Obtener el nombre del jugador
        Nombre = JugadorActual.getNombre()

        if Nombre == "Jugador 1":
            self.marcador_tiempo1.config(text="Tiempo: 10s")
            for fila in self.botones_tablero1:
                for casilla in fila:
                    casilla["boton"].config(state="disabled")

            for fila in self.botones_tablero2:
                for casilla in fila:
                    casilla["boton"].config(state="normal")

        else:
            self.marcador_tiempo2.config(text="Tiempo: 10s")
            for fila in self.botones_tablero2:
                for casilla in fila:
                    casilla["boton"].config(state="disabled")

            for fila in self.botones_tablero1:
                for casilla in fila:
                    casilla["boton"].config(state="normal")

    def Deshabilitar_botones(self):
        """Deshabilita todos los botones"""
        for fila in self.botones_tablero2:
            for casilla in fila:
                casilla["boton"].config(state="disabled")

        for fila in self.botones_tablero1:
            for casilla in fila:
                casilla["boton"].config(state="disabled")


    def VerificaPareja(self,jugador):
        """Verifica si el jugador ha encontrado a la pareja o no"""
        JugadorActual = jugador
        if self.Primera_carta == self.Segunda_carta:
            self.Acierto()
            JugadorActual.incrementar_intentos()
            JugadorActual.setParejasEncontradas()
            self.root.after(1000, lambda: self.ReiniciarCartas("Gane"))


        else:
            if self.HayDosJugadores:
                self.cambiar_turno()

            JugadorActual.setFallos()
            JugadorActual.incrementar_intentos()
            self.pausar_cronometro()
            self.root.after(1000, lambda: self.ReiniciarCartas("Fallo"))

            if self.HayDosJugadores:
                self.root.after(1500, lambda: [
                    self.Actualizar_estado_botones(JugadorActual),
                    self.root.event_generate("<<UpdateMarkers>>")  # Evento para actualizar marcadores
                ])

            else:
                self.tiempo_restante = 10
                self.actualizar_marcadores()
                self.actualizar_display()

    def VerificarTerminaJuego(self):
        """Verifica si ya los jugadores encontraron todas las parejas"""
        ParejasJugador1 = self.jugador1.getParejasEncontradas()
        ParejasJugador2 = self.jugador2.getParejasEncontradas()

        if ParejasJugador1 == 18 and ParejasJugador2 == 18 :
            self.detener_cronometro_completamente()
            self.actualizar_marcadores()
            self.Deshabilitar_botones()
            self.VerificaGanador()

        elif ParejasJugador1 == 18 or ParejasJugador2 == 18:
            if self.HayDosJugadores:
                self.HayDosJugadores = False
                self.detener_cronometro_completamente()
                jugadorActual=self.obtener_jugador_actual()
                self.Actualizar_estado_botones(jugadorActual)
                self.cambiar_turno()
                self.actualizar_marcadores()

            
    def VerificaGanador(self):
        """Verifica quien fue el jugador ganador"""
        IntentosJugador1 = self.jugador1.getIntentos()
        IntentosJugador2 = self.jugador2.getIntentos()
        if IntentosJugador1 > IntentosJugador2:
            ganador = "Jugador 2"

        elif IntentosJugador1 == IntentosJugador2:
            ganador = "Empate"

        else:
            ganador = "Jugador 1"  
        
        # Crear ventana de ganador
        self.CrearVentanaGane(ganador,IntentosJugador1, IntentosJugador2)
        

            