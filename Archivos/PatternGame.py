import tkinter as tk
from tkinter import messagebox
from Jugador import Jugador
import threading
import time
import random

class PatternGame:
    def __init__(self):
        self.root = None
        self.board = self.inicializarTablero()
        self.jugador = Jugador("Jugador")
        self.botones = []
        self.Patron = []
        self.SecuenciaActual = 3
        self.PasoActual = 0
        self.actualizar_puntuacion = None
        self.mostrar_ventana_victoria = None
        self.mostrar_ventana_game_over = None
        self.actualizar_tiempo = None

        #Tiempo
        self.ejecutando = False
        self.hilo_cronometro = None
        self.cronometro_activo = True
        self.tiempo_restante = 12

    #SETS Y GETS

    #Botones
    def SetBotones(self,botones):
        self.botones = botones

    #Secuencia actual
    def getSecuenciaActual(self):
        return self.SecuenciaActual
    
    def setSecuenciaActual(self, num):
        self.setSecuenciaActual += num

    def AumentaPasoActual(self):
        """Aumenta el paso actual (cuantos botones ha tocado el jugador) """
        self.PasoActual += 1

    def setRoot(self, root):
        """Establece root para ser utilizada en la clase"""
        self.root = root

    #get de jugador
    def getJugador(self):
        return self.jugador
    
    #Obtener funciones importantes
    def RecibirFunciones(self, funcion1, funcion2, funcion3, funcion4):
        self.actualizar_puntuacion = funcion1
        self.mostrar_ventana_victoria = funcion2
        self.actualizar_tiempo = funcion3
        self.mostrar_ventana_game_over = funcion4


    # get tiempo restante
    def getTiempoRestante(self):
        return self.tiempo_restante


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
            if not self.ejecutando:
                break

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
        self.actualizar_tiempo()

    def detener_cronometro_completamente(self):
        """Detiene completamente el cronómetro y limpia el hilo"""
        self.ejecutando = False
        self.tiempo_restante = 12
        if self.hilo_cronometro and self.hilo_cronometro.is_alive():
            self.hilo_cronometro.join()
        self.hilo_cronometro = None

    def pausar_cronometro(self):
        """Pausa en cronometro"""
        self.ejecutando = False

    def tiempo_agotado(self):
        """Llama a la funcion game over y pausa el cronometro"""
        self.detener_cronometro_completamente()
        SecuenciasCompletadas = self.jugador.getSecuencias()
        self.mostrar_ventana_game_over(SecuenciasCompletadas)


    #JUEGO

    def inicializarTablero(self):
        """Inicializa el tablero"""
        board = []
        for _ in range(4):
            row = ["" for _ in range(4)]
            board.append(row)
        return board
    
    def EstablecerPatron(self):
        """Establece el patron para el juego"""
        botones_copia = self.botones.copy()
        random.shuffle(botones_copia)
        CantBotones = len(botones_copia)
        for i in range(CantBotones):
            Boton = botones_copia[i]
            self.Patron += Boton
        random.shuffle(self.Patron)
        

    def MostrarPatron(self):
        """Muestra el patron al inicio de cada secuencia"""
        def mostrar_boton(indice):
            if indice < self.SecuenciaActual:
                # Obtener el botón actual del patrón
                boton_actual = self.Patron[indice]
                
                # Cambiar el color del botón para "mostrarlo"
                boton_actual['boton'].config(bg=boton_actual['color'])
                self.root.after(500, lambda: ocultar_boton(indice))
            else:
                self.iniciar_cronometro()
            
        def ocultar_boton(indice):
            # Restaurar color original
            boton_actual = self.Patron[indice]
            boton_actual['boton'].config(bg='#5D00AF') 
            
            # Mostrar siguiente boton luego de una pausa
            self.root.after(700, lambda: mostrar_boton(indice + 1))
            
        
        mostrar_boton(0)


    def VerificaSecuencia(self,boton):
        """Verifica si el boton presionado es parte de la secuencia en el orden indicado"""
        indice = self.PasoActual - 1
        if boton == self.Patron[indice]:
            return True
        else:
            return False
        
    def IniciaSecuencia(self):
        """Verifica si se ha completado la secuencia y vuelve a mostrarla en pantalla sumandole 1 a la secuencia actual"""
        if self.PasoActual == self.SecuenciaActual:

            #Detenemos el tiempo
            self.pausar_cronometro()
            self.tiempo_restante = 12
            self.actualizar_tiempo()

            if self.SecuenciaActual == 16:
                self.detener_cronometro_completamente()
                self.mostrar_ventana_victoria()
            else:
                self.jugador.AumentaSecuencia()
                self.actualizar_puntuacion()
                self.PasoActual = 0
                self.SecuenciaActual += 1
                self.root.after(1500, self.MostrarPatron)

    def reiniciar(self):
        self.detener_cronometro_completamente()
        self.jugador.setSecuencias(0)
        self.botones = []
        self.Patron = []
        self.SecuenciaActual = 3
        self.PasoActual = 0






