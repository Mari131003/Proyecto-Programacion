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
        self.SecuenciaActual = 1
        self.PasoActual = 0
        self.actualizar_puntuacion = None

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

    #Obtener jugador
    def obtenerJugador(self):
        return self.jugador
    
    #Obtener funciones importantes
    def RecibirFunciones(self,funcion1):
        self.actualizar_puntuacion = funcion1
            
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
        CantBotones = len(botones_copia) - 1

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
                if self.SecuenciaActual == 16:
                    pass
                else:
                    self.jugador.AumentaSecuencia()
                    self.actualizar_puntuacion()
                    self.PasoActual = 0
                    self.SecuenciaActual += 1
                    self.root.after(1500, self.MostrarPatron)




