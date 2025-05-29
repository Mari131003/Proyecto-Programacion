import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk 
import os
import random
from MemoryGame import MemoryGame

class PatternGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Patrones")
        self.root.configure(bg="white")
        self.BOTON_ANCHO = 80
        self.BOTON_ALTO = 80
        self.imagenes = self.cargar_imagenes()
        self.game = MemoryGame()
        self.botones = [[None for _ in range(6)] for _ in range(6)]
        self.crear_interfaz()

    def cargar_imagenes(self):
        imagenes = []
        for i in range(1, 6):  
            try:
                ruta = f"imagenespatrones/imagen{i}.jpg"
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
        marco_superior = tk.Frame(self.root, bg="white")
        marco_superior.grid(row=0, column=0, columnspan=6, pady=20)
        for i in range(8):
            btn = tk.Button(
                marco_superior,
                text=f"Btn {i+1}",
                width=self.BOTON_ANCHO//10,
                height=self.BOTON_ALTO//20
            )
            btn.grid(row=0, column=i, padx=5)
        parejas = [i % 5 for i in range(36)] #Tablero 6x6
        random.shuffle(parejas)
        for i in range(6):
            for j in range(6):
                id_imagen = parejas[i * 6 + j]
                btn = tk.Button(
                    self.root,
                    image=self.imagenes[id_imagen],
                    width=self.BOTON_ANCHO,
                    height=self.BOTON_ALTO
                )
                btn.grid(row=i+1, column=j, padx=2, pady=2)
                self.botones[i][j] = {
                    "boton": btn,
                    "imagen_id": id_imagen
                }
        tk.Button(
            self.root,
            text="Reiniciar Juego",
            command=self.reiniciar_juego
        ).grid(row=7, column=0, columnspan=6, pady=10)

    def reiniciar_juego(self):
        parejas = [i % 5 for i in range(36)] #Reorganiza las imágenes en el tablero.
        random.shuffle(parejas)
        for i in range(6):
            for j in range(6):
                id_imagen = parejas[i * 6 + j]
                self.botones[i][j]["boton"].config(image=self.imagenes[id_imagen])
                self.botones[i][j]["imagen_id"] = id_imagen