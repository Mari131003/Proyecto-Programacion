import tkinter as tk
from tkinter import PhotoImage, font
from PIL import Image, ImageTk 
import pygame
import os
import random
from MemoryGame import MemoryGame


class MemoryGameGUI:
    def __init__(self, root,music_callback=None,return_callback=None):
        self.root = root
        self.music_callback = music_callback
        self.return_callback = return_callback
        self.root.protocol("WM_DELETE_WINDOW", self.return_to_main)
        self.root.title("Juego de Memoria")
        self.seleccion_activa = True 
        self.music_callback = music_callback
        if self.music_callback:
            self.music_callback("musica/audiomemoria.mp3")
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
        self.game.Recibir_VentanasGane(self.mostrar_ventana_victoria)
        pygame.mixer.init()
        self.sonido_victoria = None
    
        # Cargar sonido de victoria
        try:
            ruta_sonido = os.path.join("musica", "victoria.mp3")
            if os.path.exists(ruta_sonido):
                self.sonido_victoria = pygame.mixer.Sound(ruta_sonido)
        except Exception as e:
            print(f"No se pudo cargar sonido de victoria: {e}")

        tk.Button(
            self.root,
            text="Volver al Menú",
            command=self.return_to_main,
            bg="#B22F70",
            fg='white',
            font=self.custom_font
        ).grid(row=8, column=0, columnspan=13, pady=10)

    def return_to_main(self):
        if self.music_callback:
            self.music_callback("musica/pantallaprincipal.mp3")
        if self.return_callback:
            self.return_callback()

    #Enviar Root a game
    def enviarRoot(self):
        self.game.setRoot(self.root)

    def crear_marcadores(self):

        #Crear frame para contener los marcadores
        marcadores_frame = tk.Frame(self.root, bg="#F5C5DB")
        marcadores_frame.grid(row=0, column=0, columnspan=13, sticky="nsew")
        for i in range(13):
            marcadores_frame.grid_columnconfigure(i, weight=1 if i in [2,9] else 0)

        #Crear frame para jugador 1
        frame_jugador1 = tk.Frame(marcadores_frame, bg='#F5C5DB', bd=2, relief="ridge", padx=10, pady=5)
        frame_jugador1.grid(row=0, column=0, columnspan=6, sticky="nsew", padx=(0,10))
        frame_jugador1.grid_propagate(False)
        frame_jugador1.config(width=self.BOTON_ANCHO*6 + 2*5)  
        tk.Label(frame_jugador1, text="Jugador 1", bg='#B22F70', fg='white',
                font=self.custom_font).pack(pady=(0,5))
        
        #Marcador del juego
        self.marcador_parejas1 = tk.Label(frame_jugador1, text="Parejas: 0", bg='#F5C5DB')
        self.marcador_parejas1.pack()
        self.marcador_fallos1 = tk.Label(frame_jugador1, text="Fallos: 0", bg='#F5C5DB')
        self.marcador_fallos1.pack()

        #Marcador de tiempo
        self.marcador_tiempo1 = tk.Label(frame_jugador1, text="Tiempo: 10s", bg='#F5C5DB')
        self.marcador_tiempo1.pack()

        #Crear frame para jugador 2
        frame_jugador2 = tk.Frame(marcadores_frame, bg='#F5C5DB', bd=2, relief="ridge", padx=10, pady=5)
        frame_jugador2.grid(row=0, column=7, columnspan=6, sticky="nsew", padx=(10,0))
        frame_jugador2.grid_propagate(False)
        frame_jugador2.config(width=self.BOTON_ANCHO*6 + 2*5)  
        tk.Label(frame_jugador2, text="Jugador 2", bg='#B22F70', fg='white',
                font=self.custom_font).pack(pady=(0,5))
        
        #Marcador del juego
        self.marcador_parejas2 = tk.Label(frame_jugador2, text="Parejas: 0", bg='#F5C5DB')
        self.marcador_parejas2.pack()
        self.marcador_fallos2 = tk.Label(frame_jugador2, text="Fallos: 0", bg='#F5C5DB')
        self.marcador_fallos2.pack()

        #Macrcador de tiempo
        self.marcador_tiempo2 = tk.Label(frame_jugador2, text="Tiempo: 10s", bg='#F5C5DB')
        self.marcador_tiempo2.pack()

        #Marcador de turno
        self.marcador_turno = tk.Label(marcadores_frame, text="Turno: Jugador 1", bg="#F5C5DB", 
                                     font=("Helvetica", 12, "bold"), fg="#B22F70")
        self.marcador_turno.grid(row=0, column=6, sticky="ns")

        marcadores_frame.config(height=100)
        marcadores_frame.grid_propagate(False)

        self.EnviarMarcadores()

    #Enviar marcadores a la clase game
    def EnviarMarcadores(self):
        #Enviamos marcadores de tiempo (para actualizarlos cada segundo)
        self.game.setMarcadores(self.marcador_tiempo1,self.marcador_tiempo2)

        #Enviamos la funcion para actualizarlos
        self.game.Recibir_ActualizarMarcadores(self.actualizar_marcadores)

        #Enviamos funcion que muestra los marcadores al ganar
        self.game.Recibir_VentanasGane(self.mostrar_ventana_ganador)



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
                ruta = f"imagenesmemoria/imagen{i}.jpg"
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

        #Crea la separacion entre ambos
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

        #Enviar imagen oculta a game para actualizar luego los botones
        self.game.setImagenOculta(self.imagen_oculta)

        #Enviar tableros y sus botones
        self.game.setTableros(self.botones_tablero1,self.botones_tablero2)
    

    def revelar_imagen(self, fila, col, tablero):
        """Revela la imagen en la posición especificada del tablero indicado."""
        if not self.seleccion_activa:  # No hacer nada si la selección está bloqueada
            return
        if tablero == 1:
            boton_info = self.botones_tablero1[fila][col]
        else:
            boton_info = self.botones_tablero2[fila][col]
        if not boton_info["revelado"]:
            imagen_id = boton_info["imagen_id"]
            boton_info["boton"].config(image=self.imagenes[imagen_id])
            boton_info["revelado"] = True
            self.Espera_Pareja(imagen_id, boton_info)

    def Espera_Pareja(self, imagen_id, casilla):
        """Verifica que haya 2 cartas antes de verificar las parejas e inicia el cronometro del jugador"""
        self.game.AumentaCartas(1)
        CantCartas = self.game.getCantCartas()
        if CantCartas == 2:
            self.seleccion_activa = False
            jugador_actual = self.game.obtener_jugador_actual()
            self.game.SetCartas(0)
            self.game.SetSegundaCarta(imagen_id, casilla)
            self.game.VerificaPareja(jugador_actual)
            self.actualizar_marcadores()  # Actualizar marcadores después de verificar pareja
            self.game.VerificarTerminaJuego()
            self.root.after(1000, lambda: setattr(self, 'seleccion_activa', True))
        else:
            self.game.SetPrimeraCarta(imagen_id, casilla)
            if not self.game.ejecutando:
                self.game.iniciar_cronometro()

    def mostrar_ventana_ganador(self, ganador, intentos1, intentos2):
        """Muestra una ventana con el jugador ganador"""
        ventana_ganador = tk.Toplevel()
        ventana_ganador.title("¡Juego Terminado!")
        ventana_ganador.geometry("300x150")
        ventana_ganador.resizable(False, False)
        ventana_ganador.config(bg="#ffcff1")
        
        # Centrar la ventana
        ventana_ganador.transient(self.root) 
        ventana_ganador.grab_set()
        
        # Título
        titulo = tk.Label(ventana_ganador, text="🎉 ¡Felicidades! 🎉", 
                        font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Mensaje del ganador
        mensaje = tk.Label(ventana_ganador, text=f"Ganador: {ganador}", 
                        font=("Arial", 12, "bold"), fg="#ff00c5")
        mensaje.pack(pady=5)
        
        # Mostrar intentos
        detalles = tk.Label(ventana_ganador, 
                        text=f"Jugador 1: {intentos1} intentos\nJugador 2: {intentos2} intentos")
        detalles.pack(pady=5)
        
        # Botón para cerrar
        boton_ok = tk.Button(ventana_ganador, text="OK", 
                            command=ventana_ganador.destroy,
                            width=10)
        boton_ok.pack(pady=10)
        
        # Centrar la ventana en la pantalla
        ventana_ganador.update_idletasks()
        x = (ventana_ganador.winfo_screenwidth() // 2) - (ventana_ganador.winfo_width() // 2)
        y = (ventana_ganador.winfo_screenheight() // 2) - (ventana_ganador.winfo_height() // 2)
        ventana_ganador.geometry(f"+{x}+{y}")

    def reiniciar_juego(self):
        """Reinicia ambos tableros del juego."""
        self.seleccion_activa = True 
        # Detener cronómetro completamente
        self.game.ejecutando = False
        if self.game.hilo_cronometro and self.game.hilo_cronometro.is_alive():
            self.game.hilo_cronometro.join()
        self.game.hilo_cronometro = None
        
        # Reiniciar tablero 1
        for fila in self.botones_tablero1:
            for casilla in fila:
                casilla["boton"].config(image=self.imagen_oculta, state="normal")
                casilla["revelado"] = False
        
        # Reiniciar tablero 2
        for fila in self.botones_tablero2:
            for casilla in fila:
                casilla["boton"].config(image=self.imagen_oculta, state="disabled")
                casilla["revelado"] = False
        
        # Reiniciar el juego
        self.game.reiniciar()
        self.actualizar_marcadores()


    def mostrar_ventana_victoria(self, ganador):
        """Muestra ventana de victoria con imagen que ocupa todo el marco"""
        if self.sonido_victoria:
            self.sonido_victoria.play()
        self.root.withdraw()
        ventana_victoria = tk.Toplevel()
        ventana_victoria.title("¡Victoria!")
        ventana_victoria.geometry("600x500") 
        ventana_victoria.resizable(False, False)
        ventana_victoria.configure(bg='#F5C5DB')
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
                                        text=f"¡{ganador} ha ganado!",
                                        font=("Helvetica", 16, "bold"), 
                                        bg='white', fg='#B22F70')
                label_ganador.place(relx=0.5, rely=0.9, anchor='center')
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
            tk.Label(marco_imagen, 
                    text=f"¡{ganador} ha ganado!\n\nVICTORIA",
                    font=("Helvetica", 24, "bold"), 
                    bg='white', fg='#B22F70').pack(expand=True)
        frame_botones = tk.Frame(ventana_victoria, bg='#F5C5DB')
        frame_botones.pack(pady=(10, 20), fill='x')
        tk.Button(
            frame_botones,
            text="Ver Premios",
            command=lambda: [self.detener_sonido(), ventana_victoria.destroy(), self.abrir_premios()],
            bg="#B22F70",
            fg='white',
            font=self.custom_font,
            width=15
        ).pack(side='left', padx=20, expand=True)
        tk.Button(
            frame_botones,
            text="Menú Principal",
            command=lambda: [self.detener_sonido(), ventana_victoria.destroy(), self.return_to_main()],
            bg="#B22F70",
            fg='white',
            font=self.custom_font,
            width=15
        ).pack(side='right', padx=20, expand=True)


    def detener_sonido(self):
        """Detiene el sonido de victoria"""
        if self.sonido_victoria:
            self.sonido_victoria.stop()

    def abrir_premios(self):
        """Método para abrir ventana de premios"""
        self.root.destroy()  # Cierra la ventana actual del juego
        root = tk.Tk()
        from MainMenu import MainMenu
        app = MainMenu(root)
        app.open_premios_window()  # Abre directamente la ventana de premios
        root.mainloop()