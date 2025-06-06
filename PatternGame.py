import tkinter as tk
from tkinter import messagebox
from Jugador import Jugador
import threading
import time
import random

class PatternGame:
    def __init__(self):
        self.root = None
        self.jugador = Jugador("Jugador")
        self.botones = []
        self.Patron = []
        self.SecuenciaActual = 3
        self.PasoActual = 0
        self.actualizar_puntuacion = None
        self.mostrar_ventana_victoria = None
        self.mostrar_ventana_game_over = None
        self.actualizar_tiempo = None
        self.actualizar_tiempo_casillas = None
        self.habilitar_botones = None
        self.deshabilitar_botones = None 

        #Cronometro (general)
        self.ejecutando = False
        self.hilo_cronometro = None
        self.tiempo_restante = 12

        #Cronometro (Entre casillas)
        self.ejecutando_casillas = False
        self.hilo_cronometro_casillas = None
        self.tiempo_restante_casillas = 2.1

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
    def RecibirFunciones(self, funcion1, funcion2, funcion3, funcion4, funcion5, funcion6,funcion7):
        """Recibe funciones importantes para llamarlas posteriormente"""
        self.actualizar_puntuacion = funcion1
        self.actualizar_tiempo = funcion2
        self.actualizar_tiempo_casillas = funcion3
        self.mostrar_ventana_victoria = funcion4
        self.mostrar_ventana_game_over = funcion5
        self.deshabilitar_botones = funcion6
        self.habilitar_botones = funcion7


    # get tiempo restante (cronometros)

    def getTiempoRestante(self):
        return self.tiempo_restante
    
    def getTiempoRestanteCasillas(self):
        return self.tiempo_restante_casillas
        

    #TIEMPO

    #Cronometro general

    def iniciar_cronometro_general(self):
        """Inicia el cronometro del jugador actual"""
        # Detener cronómetro anterior completamente
        self.detener_cronometro_completamente_general()
        
        # Reiniciar el tiempo
        self.ejecutando = True

        #Crear Hilo
        self.hilo_cronometro = threading.Thread(target=self.ejecutar_cronometro_general)
        self.hilo_cronometro.daemon = True
        self.hilo_cronometro.start()

    def ejecutar_cronometro_general(self):
        """Permite que el tiempo avance, ejecutando el cronometro del jugador"""
        while self.ejecutando and self.tiempo_restante > 0:
            time.sleep(1)
            if not self.ejecutando:
                break

            self.tiempo_restante -= 1
            try:
                if self.root and self.root.winfo_exists():
                    self.root.after(0, self.actualizar_display_general)
            except (tk.TclError, RuntimeError):
                break 

        if self.tiempo_restante <= 0 and self.ejecutando:
            try:
                if self.root and self.root.winfo_exists():
                    self.root.after(0, self.tiempo_agotado_general)
            except (tk.TclError, RuntimeError):
                pass
            
    def actualizar_display_general(self):
        """Actualiza el tiempo en pantalla cada segundo"""
        self.actualizar_tiempo()

    def detener_cronometro_completamente_general(self):
        """Detiene completamente el cronómetro y limpia el hilo"""
        self.ejecutando = False
        self.tiempo_restante = 12
        if self.hilo_cronometro and self.hilo_cronometro.is_alive():
            self.hilo_cronometro.join(timeout=0.5)
        self.hilo_cronometro = None

    def pausar_cronometro_general(self):
        """Pausa el cronometro"""
        self.ejecutando = False

    def tiempo_agotado_general(self):
        """Llama a la funcion game over y pausa el cronometro"""
        self.detener_todos_cronometros()
        SecuenciasCompletadas = self.jugador.getSecuencias()
        self.mostrar_ventana_game_over(SecuenciasCompletadas)

    #Cronometro entre casillas

    def iniciar_cronometro_casillas(self):
        """Inicia el cronómetro de 2 segundos entre casillas"""
        self.detener_cronometro_casillas()
        
        self.ejecutando_casillas = True
        self.tiempo_restante_casillas = 2.1
        self.esperando_casilla = True

        self.hilo_cronometro_casillas = threading.Thread(target=self.ejecutar_cronometro_casillas)
        self.hilo_cronometro_casillas.daemon = True
        self.hilo_cronometro_casillas.start()

    def ejecutar_cronometro_casillas(self):
        """Ejecuta el cronómetro entre casillas"""
        while self.ejecutando_casillas and self.tiempo_restante_casillas > 0:
            time.sleep(0.1)  
            if not self.ejecutando_casillas:
                break

            self.tiempo_restante_casillas -= 0.1
            self.tiempo_restante_casillas = round(self.tiempo_restante_casillas, 1)
      
            try:
                if self.root and self.root.winfo_exists():
                    self.root.after(0, self.actualizar_display_casillas)
            except (tk.TclError, RuntimeError):
                break 

        if self.tiempo_restante_casillas <= 0 and self.ejecutando_casillas:
            try:
                if self.root and self.root.winfo_exists():
                    self.root.after(0, self.tiempo_agotado_casillas)
            except (tk.TclError, RuntimeError):
                pass

    def actualizar_display_casillas(self):
        """Actualiza el tiempo entre casillas en pantalla"""
        self.actualizar_tiempo_casillas()

    def pausar_cronometro_casillas(self):
        """Pausa en cronometro"""
        self.ejecutando_casillas = False

    def detener_cronometro_casillas(self):
        """Detiene el cronómetro entre casillas"""
        self.tiempo_restante_casillas = 2.0
        self.ejecutando_casillas = False
        self.esperando_casilla = False
        if self.hilo_cronometro_casillas and self.hilo_cronometro_casillas.is_alive():
            self.hilo_cronometro_casillas.join(timeout=0.5)
        self.hilo_cronometro_casillas = None

    def tiempo_agotado_casillas(self):
        """Se ejecuta cuando se agota el tiempo entre casillas"""
        self.detener_todos_cronometros()
        SecuenciasCompletadas = self.jugador.getSecuencias()
        self.mostrar_ventana_game_over(SecuenciasCompletadas)

    #Control general de cronometros

    def detener_todos_cronometros(self):
        """Detiene ambos cronómetros completamente"""
        self.detener_cronometro_completamente_general()
        self.detener_cronometro_casillas()

    #JUEGO
    
    def EstablecerPatron(self):
        """Establece el patron para el juego"""
        #Ordenamiento de forma aleatoria
        botones_copia = self.botones.copy()
        random.shuffle(botones_copia)

        CantBotones = len(botones_copia)
        for i in range(CantBotones):
            Boton = botones_copia[i]
            self.Patron += Boton

        #Volvemos a ordenarlos aleatoriamente (asegura aleatoriedad)
        random.shuffle(self.Patron)
        

    def MostrarPatron(self):
        """Muestra el patron al inicio de cada secuencia"""

        self.deshabilitar_botones()

        def mostrar_boton(indice):
            if indice < self.SecuenciaActual:
                # Obtener el botón actual del patrón
                boton_actual = self.Patron[indice]
                
                # Cambiar el color del botón para "mostrarlo"
                boton_actual['boton'].config(bg=boton_actual['color'])
                self.root.after(500, lambda: ocultar_boton(indice))
            else:
                #Inicia cronometros
                self.habilitar_botones()
                self.iniciar_cronometro_general()
                self.iniciar_cronometro_casillas()
            
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
            self.pausar_cronometro_casillas()
            return True
        else:
            return False
        
    def IniciaSecuencia(self):
        """Verifica si se ha completado la secuencia y vuelve a mostrarla en pantalla sumandole 1 a la secuencia actual"""
        if self.PasoActual == self.SecuenciaActual:

            #Detenemos los cronometros
            #Cronometro general
            self.pausar_cronometro_general()
            self.tiempo_restante = 12
            self.actualizar_tiempo()

            #Cronometro casillas
            self.pausar_cronometro_casillas()
            self.tiempo_restante_casillas = 2.0
            self.actualizar_tiempo_casillas()

            #Verifica si ya se ha completado el patron de la matriz completa
            if self.SecuenciaActual == 16:
                self.detener_cronometro_completamente_general()
                self.detener_cronometro_casillas()
                self.mostrar_ventana_victoria()
            else:
                #Inicia una nueva secuencia
                self.jugador.AumentaSecuencia()
                self.actualizar_puntuacion()
                self.PasoActual = 0
                self.SecuenciaActual += 1
                self.root.after(1500, self.MostrarPatron)

        else:
            #Inicia el cronometro de casillas para esperar siguiente
            self.iniciar_cronometro_casillas()

    def reiniciar(self):
        """Reinicia el juego y detiene los cronometros"""
        self.detener_todos_cronometros()
        self.jugador.setSecuencias(0)
        self.botones = []
        self.Patron = []
        self.SecuenciaActual = 3
        self.PasoActual = 0






