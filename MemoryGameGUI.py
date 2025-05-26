import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk 
import os
import random
from MemoryGame import MemoryGame

class MemoryGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Memoria")
        self.BOTON_ANCHO = 100
        self.BOTON_ALTO = 100
        self.imagenes = self.cargar_imagenes()
        self.imagen_oculta = self.crear_imagen_oculta() 
        
        self.game = MemoryGame()
        self.botones = [[None for _ in range(6)] for _ in range(6)]
        self.crear_interfaz()

    def crear_imagen_oculta(self):
        """Crea una imagen oculta (cuadro gris)."""
        img = Image.new("RGB", (self.BOTON_ANCHO, self.BOTON_ALTO), color="gray")
        return ImageTk.PhotoImage(img)

    def cargar_imagenes(self):
        """Carga y redimensiona las imágenes al tamaño del botón."""
        imagenes = []
        for i in range(1, 5):  # Solo 4 imágenes de prueba por el momento, cuando las elijamos, añadimos el resto
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
                img_respaldo = Image.new("RGB", (self.BOTON_ANCHO, self.BOTON_ALTO), color="red")
                imagenes.append(ImageTk.PhotoImage(img_respaldo))
        return imagenes

    def crear_interfaz(self):
        """Crea la matriz 6x6 con botones de tamaño fijo."""
        parejas = [i % 4 for i in range(36)]
        random.shuffle(parejas)
        for i in range(6):
            for j in range(6):
                id_imagen = parejas[i * 6 + j]
                btn = tk.Button(
                    self.root,
                    image=self.imagen_oculta,
                    command=lambda row=i, col=j: self.revelar_imagen(row, col),
                    width=self.BOTON_ANCHO,
                    height=self.BOTON_ALTO
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.botones[i][j] = {
                    "boton": btn,
                    "imagen_id": id_imagen,
                    "revelado": False
                }

        tk.Button(
            self.root,
            text="Reiniciar Juego",
            command=self.reiniciar_juego
        ).grid(row=6, column=0, columnspan=6, pady=10)

    def revelar_imagen(self, fila, col):
        casilla = self.botones[fila][col]
        if not casilla["revelado"]:
            casilla["boton"].config(image=self.imagenes[casilla["imagen_id"]])
            casilla["revelado"] = True

    def reiniciar_juego(self):
        for fila in self.botones:
            for casilla in fila:
                casilla["boton"].config(image=self.imagen_oculta)
                casilla["revelado"] = False