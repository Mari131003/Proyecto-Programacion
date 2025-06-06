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
        self.custom_font = font.Font(family="Helvetica", size=12, weight="bold")
        
        # Variables de marcadores
        self.puntuacion = 0
        self.tiempo_restante = 12
        self.tiempo_restante_casillas = 2.0
        
        # Variables de los widgets de marcadores
        self.label_titulo = None
        self.label_puntuacion = None
        self.label_tiempo = None
        self.boton_inicio = None
        
        self.crear_interfaz()
        self.enviarRoot()
        self.CargarSonidoVictoria()
        self.CargarSonidoGameOver()

    def CargarSonidoVictoria(self):
        # Cargar sonido de victoria
        try:
            ruta_sonido = os.path.join("musica", "victoria.mp3")
            if os.path.exists(ruta_sonido):
                self.sonido_victoria = pygame.mixer.Sound(ruta_sonido)
        except Exception as e:
            print(f"No se pudo cargar sonido de victoria: {e}")

    def CargarSonidoGameOver(self):
        # Cargar sonido de victoria
        try:
            ruta_sonido = os.path.join("musica", "GameOver.mp3")
            if os.path.exists(ruta_sonido):
                self.sonido_GameOver = pygame.mixer.Sound(ruta_sonido)
        except Exception as e:
            print(f"No se pudo cargar sonido de victoria: {e}")

        

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
        
        # Configurar 4 columnas con pesos iguales
        frame_marcadores.grid_columnconfigure(0, weight=1)
        frame_marcadores.grid_columnconfigure(1, weight=1)
        frame_marcadores.grid_columnconfigure(2, weight=1)
        frame_marcadores.grid_columnconfigure(3, weight=1)
        
        # Título del juego
        self.label_titulo = tk.Label(
            frame_marcadores,
            text="Pattern Game",
            font=("Arial", 20, "bold"),
            fg="#5D00AF",
            bg="#EBD4FF"
        )
        self.label_titulo.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Marcador de puntuación
        frame_puntuacion = tk.Frame(frame_marcadores, bg="#E5B7FF", relief="sunken", bd=2)
        frame_puntuacion.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_puntuacion, text="Puntuación", 
                font=("Arial", 10, "bold"), bg="#E5B7FF").pack()
        self.label_puntuacion = tk.Label(
            frame_puntuacion,
            text=str(self.puntuacion),
            font=("Arial", 14, "bold"),
            bg="#E5B7FF",
            fg="#5D00AF"
        )
        self.label_puntuacion.pack()
        
        # Marcador de tiempo total
        frame_tiempo = tk.Frame(frame_marcadores, bg="#E5B7FF", relief="sunken", bd=2)
        frame_tiempo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_tiempo, text="Tiempo restante", 
                font=("Arial", 10, "bold"), bg="#E5B7FF").pack()
        self.label_tiempo = tk.Label(
            frame_tiempo,
            text=str(self.tiempo_restante),
            font=("Arial", 14, "bold"),
            bg="#E5B7FF",
            fg="#5D00AF"
        )
        self.label_tiempo.pack()

        # Marcador de tiempo entre casillas
        frame_tiempo_casillas = tk.Frame(frame_marcadores, bg="#E5B7FF", relief="sunken", bd=2)
        frame_tiempo_casillas.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame_tiempo_casillas, text="Entre Casillas", 
                font=("Arial", 10, "bold"), bg="#E5B7FF").pack()
        self.label_tiempo_casillas = tk.Label(
            frame_tiempo_casillas,
            text="2.0",
            font=("Arial", 14, "bold"),
            bg="#E5B7FF",
            fg="#5D00AF"
        )
        self.label_tiempo_casillas.pack()
        
        # Botón de inicio
        self.boton_inicio = tk.Button(
            frame_marcadores,
            text="INICIO",
            command=self.iniciar_juego,
            bg="#5D00AF",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            padx=15,
            pady=5
        )
        self.boton_inicio.grid(row=1, column=3, padx=5, pady=5)

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
            #Verifica si se debe iniciar una nueva secuencia o continuar
            self.game.IniciaSecuencia()
        else:
            jugador = self.game.getJugador()
            secuencias = jugador.getSecuencias()
            self.game.pausar_cronometro_casillas()
            self.game.pausar_cronometro_general()
            self.mostrar_ventana_game_over(secuencias)


    def actualizar_puntuacion(self):
        """Actualiza el marcador de puntuación"""
        Jugador = self.game.getJugador()
        self.puntuacion = Jugador.getSecuencias()
        self.label_puntuacion.config(text=str(self.puntuacion))


    def actualizar_tiempo(self):
        """Actualiza el marcador de tiempo"""
        self.tiempo_restante = self.game.getTiempoRestante()
        self.label_tiempo.config(text=str(self.tiempo_restante))

    def actualizar_tiempo_casillas(self):
        """Actualiza el marcador de tiempo entre casillas"""
        self.tiempo_restante_casillas = self.game.getTiempoRestanteCasillas()
        self.label_tiempo_casillas.config(text=str(self.tiempo_restante_casillas))

    def reiniciar_juego(self):
        """Reinicia el juego ocultando todos los botones y reorganizando colores"""
        #Reiniciar juego
        self.game.reiniciar()
        
        # Reiniciar marcadores visuales
        self.actualizar_puntuacion()
        self.actualizar_tiempo()
        self.actualizar_tiempo_casillas()

        # Reorganizar colores
        colores_patron = self.colores.copy()
        random.shuffle(colores_patron)
        
        for i in range(4):
            for j in range(4):
                color_nuevo = colores_patron[i * 4 + j]
                btn = self.botones[i][j]["boton"]
                
                # Ocultar botón
                btn.config(bg="#5D00AF", text="", relief="raised")
                
                # Actualizar información CON NUEVOS COLORES
                self.botones[i][j]["color"] = color_nuevo
                self.botones[i][j]["revelado"] = False
        
        self.game.SetBotones(self.botones)
        self.game.EstablecerPatron()
        
        # Reiniciar botón de inicio
        self.boton_inicio.config(text="INICIO", bg="#5D00AF")

        #Iniciar con los botones deshabilitados
        self.deshabilitar_botones()


    def mostrar_ventana_victoria(self):
        """Muestra ventana de victoria con imagen que ocupa todo el marco"""
        if self.sonido_victoria:
            self.sonido_victoria.play()
        self.root.withdraw()
        ventana_victoria = tk.Toplevel()
        ventana_victoria.title("¡Victoria!")

        #Centrar en la pantalla
        window_width = 600
        window_height = 500
        screen_width = ventana_victoria.winfo_screenwidth()
        screen_height = ventana_victoria.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        ventana_victoria.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        ventana_victoria.resizable(False, False)
        ventana_victoria.configure(bg="#EBCDFD")
        ventana_victoria.grab_set() 

        ventana_victoria.protocol("WM_DELETE_WINDOW", lambda: None) # Evitar que se cierre con la X
        marco_imagen = tk.Frame(ventana_victoria, bg='white', bd=3, relief='ridge')
        marco_imagen.pack(pady=20, padx=50, fill='y', expand=True)
        try:
            #ruta_imagen = os.path.join("imagenesmemoria", "victoria.jpeg")
            ruta_imagen = os.path.join("imagenesmemoria", "victoria.jpg")
            if os.path.exists(ruta_imagen):
                img_original = Image.open(ruta_imagen)
                marco_ancho = 560  # Calcular relación de aspecto
                marco_alto = 400   
                relacion_original = img_original.width / img_original.height
                relacion_marco = marco_ancho / marco_alto
                if relacion_original > relacion_marco:
                    nuevo_ancho = marco_ancho
                    nuevo_alto = int(marco_ancho / relacion_original)
                else:
                    nuevo_alto = marco_alto
                    nuevo_ancho = int(marco_alto * relacion_original)
                img_redimensionada = img_original.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
                self.img_victoria_tk = ImageTk.PhotoImage(img_redimensionada)
                label_imagen = tk.Label(marco_imagen, image=self.img_victoria_tk, bg='white')
                label_imagen.pack(expand=True)
                label_ganador = tk.Label(marco_imagen, 
                                        text=f"¡has ganado!",
                                        font=("Helvetica", 16, "bold"), 
                                        bg='white', fg="#5D00AF")
                label_ganador.place(relx=0.5, rely=0.9, anchor='center')
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            tk.Label(marco_imagen, 
                    text=f"¡has ganado!\n\nVICTORIA",
                    font=("Helvetica", 24, "bold"), 
                    bg='white', fg="#5D00AF").pack(expand=True)
        frame_botones = tk.Frame(ventana_victoria, bg="#EBCDFD")
        frame_botones.pack(pady=(10, 20), fill='x')
        tk.Button(
            frame_botones,
            text="Menú Principal",
            command=lambda: [self.detener_sonido(), ventana_victoria.destroy(), self.return_to_main()],
            bg="#5D00AF",
            fg='white',
            font=self.custom_font,
            width=15
        ).pack(padx=20, expand=True)

    def mostrar_ventana_game_over(self, secuencias_completadas):
        """Muestra ventana de game over con las secuencias completadas"""
        if self.sonido_GameOver:  # pendiente cambiar sonido para game over 
            self.sonido_GameOver.play()
        self.root.withdraw()
        
        ventana_game_over = tk.Toplevel()
        ventana_game_over.title("¡Game Over!")
        
        # Centrar en la pantalla
        window_width = 600
        window_height = 500
        screen_width = ventana_game_over.winfo_screenwidth()
        screen_height = ventana_game_over.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        ventana_game_over.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        ventana_game_over.resizable(False, False)
        ventana_game_over.configure(bg="#EBCDFD")
        ventana_game_over.grab_set()
        
        ventana_game_over.protocol("WM_DELETE_WINDOW", lambda: None)  # Evitar que se cierre con la X
        
        marco_imagen = tk.Frame(ventana_game_over, bg='white', bd=3, relief='ridge')
        marco_imagen.pack(pady=20, padx=50, fill='y', expand=True)
        
        try:
            ruta_imagen = os.path.join("imagenespatrones", "GameOver.jpeg")  
            if os.path.exists(ruta_imagen):
                img_original = Image.open(ruta_imagen)
                marco_ancho = 560
                marco_alto = 400
                
                relacion_original = img_original.width / img_original.height
                relacion_marco = marco_ancho / marco_alto
                
                if relacion_original > relacion_marco:
                    nuevo_ancho = marco_ancho
                    nuevo_alto = int(marco_ancho / relacion_original)
                else:
                    nuevo_alto = marco_alto
                    nuevo_ancho = int(marco_alto * relacion_original)
                
                img_redimensionada = img_original.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
                self.img_gameover_tk = ImageTk.PhotoImage(img_redimensionada)
                
                label_imagen = tk.Label(marco_imagen, image=self.img_gameover_tk, bg='white')
                label_imagen.pack(expand=True)
                
                # Mostrar secuencias completadas
                label_secuencias = tk.Label(marco_imagen,
                                        text=f"Secuencias completadas: {secuencias_completadas}",
                                        font=("Helvetica", 14, "bold"),
                                        bg="#5D00AF", fg="white")
                label_secuencias.place(relx=0.5, rely=0.95, anchor='center')
                
            else:
                # Si no hay imagen, mostrar solo texto
                tk.Label(marco_imagen,
                        text=f"¡Game Over!\n\nSecuencias completadas: {secuencias_completadas}",
                        font=("Helvetica", 24, "bold"),
                        bg="#5D00AF", fg="white").pack(expand=True)
                        
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            tk.Label(marco_imagen,
                    text=f"¡Game Over!\n\nSecuencias completadas: {secuencias_completadas}",
                    font=("Helvetica", 24, "bold"),
                    bg='white', fg="#5D00AF").pack(expand=True)
        
        frame_botones = tk.Frame(ventana_game_over, bg="#EBCDFD")
        frame_botones.pack(pady=(10, 20), fill='x')
        
        tk.Button(
            frame_botones,
            text="Reiniciar Juego",
            command=lambda: [self.detener_sonido(), ventana_game_over.destroy(), self.root.deiconify(), self.reiniciar_juego()],
            bg="#5D00AF",
            activebackground="#FFB3F9",
            fg='white',
            activeforeground='black',
            font=self.custom_font,
            width=15,
            height=20
        ).pack(padx=20, expand=True)

    def detener_sonido(self):
        """Detiene el sonido de victoria"""
        if self.sonido_victoria:
            self.sonido_victoria.stop()


    def EnviarFunciones(self):
        self.game.RecibirFunciones(self.actualizar_puntuacion, self.actualizar_tiempo, 
                                   self.actualizar_tiempo_casillas,self.mostrar_ventana_victoria, 
                                   self.mostrar_ventana_game_over, self.deshabilitar_botones,self.habilitar_botones)