import tkinter as tk
from tkinter import PhotoImage, font
from PIL import Image, ImageTk 
import os
import random
from MemoryGame import MemoryGame

class MemoryGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Memoria")
        self.root.configure(bg='#F5C5DB')
        self.custom_font = font.Font(family="Helvetica", size=10, weight="bold")
        self.BOTON_ANCHO = 85
        self.BOTON_ALTO = 85
        self.imagenes = self.cargar_imagenes()
        self.imagen_oculta = self.crear_imagen_oculta() 
        self.HayPareja = 0
        self.game = MemoryGame()
        self.botones_tablero1 = [[None for _ in range(6)] for _ in range(6)]
        self.botones_tablero2 = [[None for _ in range(6)] for _ in range(6)]
        self.crear_marcadores()
        self.crear_interfaz()
        self.enviarRoot()
        self.actualizar_marcadores()
    def enviarRoot(self):
        self.game.setRoot(self.root)
    def crear_marcadores(self):
        marcadores_frame = tk.Frame(self.root, bg="#F5C5DB")
        marcadores_frame.grid(row=0, column=0, columnspan=13, sticky="nsew")
        for i in range(13):
            marcadores_frame.grid_columnconfigure(i, weight=1 if i in [2,9] else 0)
        frame_jugador1 = tk.Frame(marcadores_frame, bg='#F5C5DB', bd=2, relief="ridge", padx=10, pady=5)
        frame_jugador1.grid(row=0, column=0, columnspan=6, sticky="nsew", padx=(0,10))
        frame_jugador1.grid_propagate(False)
        frame_jugador1.config(width=self.BOTON_ANCHO*6 + 2*5)  
        tk.Label(frame_jugador1, text="Jugador 1", bg='#B22F70', fg='white',
                font=self.custom_font).pack(pady=(0,5))
        self.marcador_parejas1 = tk.Label(frame_jugador1, text="Parejas: 0", bg='#F5C5DB')
        self.marcador_parejas1.pack()
        self.marcador_fallos1 = tk.Label(frame_jugador1, text="Fallos: 0", bg='#F5C5DB')
        self.marcador_fallos1.pack()
        self.marcador_tiempo1 = tk.Label(frame_jugador1, text="Tiempo: 0s", bg='#F5C5DB')
        self.marcador_tiempo1.pack()
        frame_jugador2 = tk.Frame(marcadores_frame, bg='#F5C5DB', bd=2, relief="ridge", padx=10, pady=5)
        frame_jugador2.grid(row=0, column=7, columnspan=6, sticky="nsew", padx=(10,0))
        frame_jugador2.grid_propagate(False)
        frame_jugador2.config(width=self.BOTON_ANCHO*6 + 2*5)  
        tk.Label(frame_jugador2, text="Jugador 2", bg='#B22F70', fg='white',
                font=self.custom_font).pack(pady=(0,5))
        self.marcador_parejas2 = tk.Label(frame_jugador2, text="Parejas: 0", bg='#F5C5DB')
        self.marcador_parejas2.pack()
        self.marcador_fallos2 = tk.Label(frame_jugador2, text="Fallos: 0", bg='#F5C5DB')
        self.marcador_fallos2.pack()
        self.marcador_tiempo2 = tk.Label(frame_jugador2, text="Tiempo: 0s", bg='#F5C5DB')
        self.marcador_tiempo2.pack()
        self.marcador_turno = tk.Label(marcadores_frame, text="Turno: Jugador 1", bg="#F5C5DB", 
                                     font=("Helvetica", 12, "bold"), fg="#B22F70")
        self.marcador_turno.grid(row=0, column=6, sticky="ns")
        marcadores_frame.config(height=100)
        marcadores_frame.grid_propagate(False)

    def actualizar_marcadores(self):
        self.marcador_parejas1.config(text=f"Parejas: {self.game.jugador1.getParejasEncontradas()}")
        self.marcador_parejas2.config(text=f"Parejas: {self.game.jugador2.getParejasEncontradas()}")
        self.marcador_fallos1.config(text=f"Fallos: {self.game.jugador1.getFallos()}")
        self.marcador_fallos2.config(text=f"Fallos: {self.game.jugador2.getFallos()}")
        jugador_actual = "Jugador 1" if self.game.turno_actual == 0 else "Jugador 2"
        self.marcador_turno.config(text=f"Turno: {jugador_actual}")

    def crear_imagen_oculta(self):
        img = Image.new("RGB", (self.BOTON_ANCHO, self.BOTON_ALTO), color="#F3B3D1")
        return ImageTk.PhotoImage(img)

    def cargar_imagenes(self):
        imagenes = []
        for i in range(1,19):
            try:
                ruta = f"imagenes/imagen{i}.jpg"
                if os.path.exists(ruta):
                    img = Image.open(ruta)
                    img = img.resize((self.BOTON_ANCHO, self.BOTON_ALTO))
                    imagenes.append(ImageTk.PhotoImage(img))
                else:
                    raise FileNotFoundError(f"Archivo {ruta} no encontrado")
            except Exception as e:
                print(f"Error al cargar imagen {i}: {e}")
                img_respaldo = Image.new("RGB", (self.BOTON_ANCHO, self.BOTON_ALTO), color="#FF69B4")
                imagenes.append(ImageTk.PhotoImage(img_respaldo))
        return imagenes

    def crear_interfaz(self):
        """Crea la matriz 6x6 con botones de tamaño fijo."""
        parejas_tablero1 = [i % 18 for i in range(36)]
        parejas_tablero2 = [i % 18 for i in range(36)]
        random.shuffle(parejas_tablero1)
        random.shuffle(parejas_tablero2)

        # Crear tablero 1 (columnas 0-5)
        for i in range(6):
            for j in range(6):
                id_imagen = parejas_tablero1[i * 6 + j]
                btn = tk.Button(
                    self.root,
                    image=self.imagen_oculta,
                    command=lambda row=i, col=j, tablero=1: self.revelar_imagen(row, col, tablero),
                    width=self.BOTON_ANCHO,
                    height=self.BOTON_ALTO,
                    bg="#F3B3D1",  
                    activebackground="#F3B3D1"  
                )
                btn.grid(row=i+1, column=j, padx=2, pady=2)  # +1 por los marcadores
                self.botones_tablero1[i][j] = {
                    "boton": btn,
                    "imagen_id": id_imagen,
                    "revelado": False
                }
        separador = tk.Frame(self.root, width=20, bg='#F5C5DB')
        separador.grid(row=1, column=6, rowspan=6, sticky="ns", padx=10)
        
        # Crear tablero 2 (columnas 7-12)
        for i in range(6):
            for j in range(6):
                id_imagen = parejas_tablero2[i * 6 + j]
                btn = tk.Button(
                    self.root,
                    image=self.imagen_oculta,
                    command=lambda row=i, col=j, tablero=2: self.revelar_imagen(row, col, tablero),
                    width=self.BOTON_ANCHO,
                    height=self.BOTON_ALTO,
                    bg='#F3B3D1', 
                    activebackground="#F3B3D1" 
                )
                btn.grid(row=i+1, column=j+7, padx=2, pady=2)  # +1 por los marcadores
                self.botones_tablero2[i][j] = {
                    "boton": btn,
                    "imagen_id": id_imagen,
                    "revelado": False
                }
        tk.Button(
            self.root,
            text="Reiniciar Juego",
            command=self.reiniciar_juego,
            bg="#B22F70", 
            fg='white',    
            activebackground='#FF1493',
            activeforeground='white',
            font=self.custom_font
        ).grid(row=7, column=0, columnspan=13, pady=10)
        # Iniciar con los botones del tablero 2 deshabilitados
        for fila in self.botones_tablero2:
                for casilla in fila:
                    casilla["boton"].config(state="disabled")

    def revelar_imagen(self, fila, col, tablero):
        """Revela la imagen en la posición especificada del tablero indicado."""
        if tablero == 1:
            boton_info = self.botones_tablero1[fila][col]
        else:
            boton_info = self.botones_tablero2[fila][col]
        if not boton_info["revelado"]:
            imagen_id = boton_info["imagen_id"]
            boton_info["boton"].config(image=self.imagenes[imagen_id])
            boton_info["revelado"] = True
            self.Espera_Pareja(1, imagen_id, boton_info)

    def Espera_Pareja(self, CantPareja, imagen_id, casilla):
        self.HayPareja += CantPareja
        if self.HayPareja == 2:
            jugador_actual = self.game.obtener_jugador_actual()
            self.HayPareja = 0
            self.game.SetSegundaCarta(imagen_id, casilla)
            self.game.VerificaPareja(jugador_actual, self.imagen_oculta, self.botones_tablero1, self.botones_tablero2)
            self.actualizar_marcadores()  # Actualizar marcadores después de verificar pareja
        else:
            self.game.SetPrimeraCarta(imagen_id, casilla)

    def reiniciar_juego(self):
        """Reinicia ambos tableros del juego."""
        # Reiniciar tablero 1
        for fila in self.botones_tablero1:
            for casilla in fila:
                casilla["boton"].config(image=self.imagen_oculta)
                casilla["revelado"] = False
        # Reiniciar tablero 2
        for fila in self.botones_tablero2:
            for casilla in fila:
                casilla["boton"].config(image=self.imagen_oculta)
                casilla["revelado"] = False
        # Reiniciar el juego
        self.game.reiniciar()
        self.actualizar_marcadores()
        # Volver a deshabilitar tablero 2
        for fila in self.botones_tablero2:
            for casilla in fila:
                casilla["boton"].config(state="disabled")