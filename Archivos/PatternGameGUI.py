import tkinter as tk
from tkinter import PhotoImage, font
from PIL import Image, ImageTk 
import pygame
import os
import random
from PatternGame import PatternGame


class PatternGameGUI:
    def __init__(self, root, music_callback=None, return_callback=None):
        self.root = root
        self.music_callback = music_callback
        self.return_callback = return_callback
        self.root.protocol("WM_DELETE_WINDOW", self.return_to_main)
        self.root.title("Juego de Patrones")
        self.root.configure(bg="#F4E1FF")
        self.game = PatternGame()
        self.centrar_ventana()

        #Musica
        if self.music_callback:
            self.music_callback("musica/audiopatrones.mp3")
        
        # Variables de juego
        self.BOTON_ANCHO = 8
        self.BOTON_ALTO = 4
        self.colores = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", "#E1BAFF",
               "#FFBAFF", "#D4C5B9", "#B3E5FC", "#F8BBD9", "#C8E6C8", "#DDB3FF", 
               "#FF9E9E", "#FFCCCB", "#B3C6E7", "#C8E6A0"]
        
        self.botones = [[None for _ in range(4)] for _ in range(4)]
        
        # Variables de marcadores
        self.puntuacion = 0
        self.tiempo_restante = 12
        
        # Variables de los widgets de marcadores
        self.label_titulo = None
        self.label_puntuacion = None
        self.label_tiempo = None
        self.boton_inicio = None
        
        self.crear_interfaz()
        self.enviarRoot()

    def enviarRoot(self):
        """Enviar Root a game"""
        self.game.setRoot(self.root)

    def iniciar_juego(self):
        """Función que inicia el juego"""
        self.habilitar_botones()
        if self.boton_inicio:
            self.boton_inicio.config(text="¡INICIADO!", bg="#5D00AF")
        #Mostrar el primer patron
        self.game.MostrarPatron()


    def return_to_main(self):
        """Cambia la música y ejecuta callback para volver al menú principal"""
        if self.music_callback:
            self.music_callback("musica/pantallaprincipal.mp3")
        if self.return_callback:
            self.return_callback()

    def centrar_ventana(self):
        """Centra la ventana en el centro exacto de la pantalla"""
        # Configurar tamaño de la ventana
        window_width = 600
        window_height = 700
        
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcular posición para centrar
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Establecer geometría y centrar
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)

    def marcadores(self):
        """Crea el tablero superior con título, puntuación y tiempo"""
        # Frame principal para los marcadores
        frame_marcadores = tk.Frame(self.root, bg="#EBD4FF", relief="ridge", bd=2)
        frame_marcadores.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="ew")
        frame_marcadores.grid_columnconfigure(0, weight=1)
        frame_marcadores.grid_columnconfigure(1, weight=1)
        frame_marcadores.grid_columnconfigure(2, weight=1)
        
        # Título del juego
        self.label_titulo = tk.Label(
            frame_marcadores,
            text="Pattern Game",
            font=("Arial", 20, "bold"),
            fg="#5D00AF",
            bg="#EBD4FF"
        )
        self.label_titulo.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Marcador de puntuación
        frame_puntuacion = tk.Frame(frame_marcadores, bg="#E5B7FF", relief="sunken", bd=2)
        frame_puntuacion.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        tk.Label(frame_puntuacion, text="Puntuación", 
                font=("Arial", 12, "bold"), bg="#E5B7FF").pack()
        self.label_puntuacion = tk.Label(
            frame_puntuacion,
            text=str(self.puntuacion),
            font=("Arial", 16, "bold"),
            bg="#E5B7FF",
            fg="#5D00AF"
        )
        self.label_puntuacion.pack()
        
        # Botón de inicio central
        self.boton_inicio = tk.Button(
            frame_marcadores,
            text="INICIO",
            command=self.iniciar_juego,
            bg="#5D00AF",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=20,
            pady=5
        )
        self.boton_inicio.grid(row=1, column=1, padx=10, pady=5)
        
        # Marcador de tiempo
        frame_tiempo = tk.Frame(frame_marcadores, bg="#E5B7FF", relief="sunken", bd=2)
        frame_tiempo.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        
        tk.Label(frame_tiempo, text="Tiempo Restante", 
                font=("Arial", 12, "bold"), bg="#E5B7FF").pack()
        self.label_tiempo = tk.Label(
            frame_tiempo,
            text=str(self.tiempo_restante),
            font=("Arial", 16, "bold"),
            bg="#E5B7FF",
            fg="#5D00AF"
        )
        self.label_tiempo.pack()

    def crear_interfaz(self):
        """Esta funcion crea la matriz con botones"""
        # Crear los marcadores superiores
        self.marcadores()

        # Tablero 4x4 - Asignar colores aleatorios
        colores_patron = self.colores.copy()
        random.shuffle(colores_patron)
        
        for i in range(4):
            for j in range(4):
                color_asignado = colores_patron[i * 4 + j]
                btn = tk.Button(
                    self.root,
                    text="",  
                    width=self.BOTON_ANCHO,
                    height=self.BOTON_ALTO,
                    command=lambda r=i, c=j: self.presionar_boton(r, c),
                    bg="#5D00AF", 
                    activebackground="#5D00AF",
                    font=("Arial", 20, "bold"),
                    relief="raised",
                    bd=3
                )
                btn.grid(row=i+2, column=j, padx=5, pady=5)
                
                self.botones[i][j] = {
                    "boton": btn,
                    "color": color_asignado,
                    "revelado": False
                }

        #Enviar los botones para establecer el patron
        self.game.SetBotones(self.botones)
        self.game.EstablecerPatron()


        # Configurar grid para que los botones se expandan
        for i in range(2, 6): 
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.root.grid_columnconfigure(j, weight=1)

        #Iniciar con los botones deshabilitados
        self.deshabilitar_botones()

        tk.Button(
            self.root,
            text="Reiniciar Juego",
            command=self.reiniciar_juego,
            bg="#5D00AF",
            fg='white',
            font=("Helvetica", 10, "bold")
        ).grid(row=6, column=0, columnspan=4, pady=10)

        tk.Button(
            self.root,
            text="Volver al Menú",
            command=self.return_to_main,
            bg="#5D00AF",
            fg='white',
            font=("Helvetica", 10, "bold")
        ).grid(row=7, column=0, columnspan=4, pady=10)

        self.EnviarFunciones()

    def deshabilitar_botones(self):
        """Deshabilita todos los botones del tablero"""
        for i in range(4):
            for j in range(4):
                btn = self.botones[i][j]["boton"]
                btn.config(state="disabled")

    def habilitar_botones(self):
        """Habilita todos los botones del tablero"""
        for i in range(4):
            for j in range(4):
                btn = self.botones[i][j]["boton"]
                btn.config(state="normal")

    def presionar_boton(self, fila, columna):
        """Esta funcion verifica si el boton presionado esta en el orden correcto de la secuencia"""
        boton_info = self.botones[fila][columna]
        btn = boton_info["boton"]
        
        # Revelar el color 
        btn.config(
            bg=boton_info["color"],
            text=""
        )
        
        # oculta el color
        def OcultarBoton():
            btn.config(
                bg="#5D00AF",
                text=""
            )

        self.root.after(500, OcultarBoton)
        
        #Aumenta el paso en el que se encuentra el jugador
        self.game.AumentaPasoActual()

        #Verifica el orden
        if self.game.VerificaSecuencia(boton_info):
            print("Win")
            self.game.IniciaSecuencia()
        else:
            print("GameOver")


    def actualizar_puntuacion(self):
        """Actualiza el marcador de puntuación"""
        Jugador = self.game.obtenerJugador()
        self.puntuacion = Jugador.getSecuencias()
        self.label_puntuacion.config(text=str(self.puntuacion))

    def actualizar_tiempo(self):
        """Actualiza el marcador de tiempo"""
        if self.label_tiempo:
            self.label_tiempo.config(text=str(self.tiempo_restante))

    def reiniciar_juego(self):
        """Reinicia el juego ocultando todos los botones y reorganizando colores"""
        # Reorganizar colores
        colores_patron = self.colores.copy()
        random.shuffle(colores_patron)
        
        # Reiniciar marcadores
        self.puntuacion = 0
        self.tiempo_restante = 12
        self.actualizar_puntuacion()
        self.actualizar_tiempo()
        
        for i in range(4):
            for j in range(4):
                color_nuevo = colores_patron[i * 4 + j]
                btn = self.botones[i][j]["boton"]
                
                # Ocultar botón nuevamente
                btn.config(
                    bg="#5D00AF",
                    text="",
                    relief="raised"
                )
                
                # Actualizar información
                self.botones[i][j]["color"] = color_nuevo
                self.botones[i][j]["revelado"] = False

    def EnviarFunciones(self):
        self.game.RecibirFunciones(self.actualizar_puntuacion)

        #Reinicar boton de inicio
        self.boton_inicio.config(text="INICIO", bg="#5D00AF")
