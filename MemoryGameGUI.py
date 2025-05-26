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
        self.BOTON_ANCHO = 85
        self.BOTON_ALTO = 85
        self.imagenes = self.cargar_imagenes()
        self.imagen_oculta = self.crear_imagen_oculta() 
        self.HayPareja = 0
        self.game = MemoryGame()
        self.botones_tablero1 = [[None for _ in range(6)] for _ in range(6)]
        self.botones_tablero2 = [[None for _ in range(6)] for _ in range(6)]
        self.crear_interfaz()
        self.EnviarRoot()

    #Enviar root a la clase game
    def EnviarRoot(self):
        self.game.setRoot(self.root)

    def crear_imagen_oculta(self):
        """Crea una imagen oculta (cuadro gris)."""
        img = Image.new("RGB", (self.BOTON_ANCHO, self.BOTON_ALTO), color="gray")
        return ImageTk.PhotoImage(img)

    def cargar_imagenes(self):
        """Carga y redimensiona las imágenes al tamaño del botón."""
        imagenes = []
        for i in range(1,19):  # 18 imagenes (Falta seleccionarlas mejor)
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
        parejas_tablero1 = [i % 18 for i in range(36)] #18 imagenes
        parejas_tablero2 = [i % 18 for i in range(36)] #18 imagenes
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
                    height=self.BOTON_ALTO
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.botones_tablero1[i][j] = {
                    "boton": btn,
                    "imagen_id": id_imagen,
                    "revelado": False
                }
        
        # Separador visual entre tableros
        separador = tk.Frame(self.root, width=20, bg="lightgray")
        separador.grid(row=0, column=6, rowspan=6, sticky="ns", padx=10)
        
        # Crear tablero 2 (columnas 7-12)
        for i in range(6):
            for j in range(6):
                id_imagen = parejas_tablero2[i * 6 + j]
                
                btn = tk.Button(
                    self.root,
                    image=self.imagen_oculta,
                    command=lambda row=i, col=j, tablero=2: self.revelar_imagen(row, col, tablero),
                    width=self.BOTON_ANCHO,
                    height=self.BOTON_ALTO
                )
                btn.grid(row=i, column=j+7, padx=2, pady=2)  # +7 para posicionar en la segunda matriz
                self.botones_tablero2[i][j] = {
                    "boton": btn,
                    "imagen_id": id_imagen,
                    "revelado": False
                }

        # Botón de reinicio centrado debajo de ambos tableros
        tk.Button(
            self.root,
            text="Reiniciar Juego",
            command=self.reiniciar_juego
        ).grid(row=6, column=0, columnspan=13, pady=10)

        #Iniciar con los botones del tablero 2 deshabilitados
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


     #Espera a que haya una pareja para luego verificar si son iguales       
    def Espera_Pareja(self,CantPareja, imagen_id, casilla):
        self.HayPareja += CantPareja
        if self.HayPareja == 2:
            jugador_actual = self.game.obtener_jugador_actual()
            self.HayPareja = 0
            self.game.SetSegundaCarta(imagen_id, casilla)
            self.game.VerificaPareja(jugador_actual, self.imagen_oculta, self.botones_tablero1, self.botones_tablero2)
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

    
