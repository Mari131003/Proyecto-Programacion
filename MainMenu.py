import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from MemoryGameGUI import MemoryGameGUI
from PatternGameGUI import PatternGameGUI
from Premios import Premios
import pygame
import os
from datetime import datetime
from PIL import Image, ImageTk

class MainMenu:
    def __init__(self, root, username=None, logout_callback=None):
        self.root = root
        self.username = username
        self.logout_callback = logout_callback
        self.root.title("Memory Game - Menú Principal")
        self.root.geometry("1000x600")
        self.root.configure(bg="#DD039F") 
        self.title_font = ("Helvetica", 24, "bold") # Fuentes personalizadas
        self.subtitle_font = ("Helvetica", 14, "bold")
        self.custom_font = ("Helvetica", 12, "bold")
        self.intro_font = ("Helvetica", 11)

        pygame.mixer.init()
        self.current_music = None
        self.play_musica("musica/pantallaprincipal.mp3")
        self.child_window = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window_width = 1000
        self.window_height = 600
        self.center_window()
        self.imagenes = {} # Inicializar diccionario para referencias de imágenes
        self.animation_active = True # Control simple de animación
        self.animation_job = None
        self.create_widgets()
        self.start_princess_animation() # Iniciar animación de la princesa

    def play_musica(self, file_path, loop=True):
        """Reproduce un archivo de música con opciones de repetición y control de volumen."""
        if not os.path.exists(file_path):
            print(f"Audio no encontrado: {file_path}")
            return
        if self.current_music == file_path and pygame.mixer.music.get_busy():
            return
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(0.4)
            if loop:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play()
            self.current_music = file_path
        except Exception as e:
            print(f"Error al reproducir música: {e}")

    def stop_music(self):
        """Para la música."""
        pygame.mixer.music.stop()
        self.current_music = None

    def center_window(self):
        """Centra la ventana en la pantalla."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - self.window_width/2)
        center_y = int(screen_height/2 - self.window_height/2)
        self.root.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.root.resizable(False, False)    
        
    def create_widgets(self):
        """Crea los widgets y botones necesarios con diseño mejorado."""
        main_container = tk.Frame(self.root, bg="#DD039F")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        left_frame = tk.Frame(main_container, bg="#FFDCF5", relief="raised", bd=3)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        content_frame = tk.Frame(left_frame, bg="#FFDCF5")
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        title_label = tk.Label(content_frame,text="❀ MEMORY GAME ❀", font=self.title_font,fg="#D00087", bg= "#FFDCF5"
        )
        title_label.pack(pady=(0, 20))
        welcome_label = tk.Label(content_frame,text=f"¡Hola {self.username}! ☻", font=self.subtitle_font, fg="#FFDCF5", bg="#D00087",
        )
        welcome_label.pack(pady=(0, 15))
        intro_text = "Pon a prueba tu mente con nuestros emocionantes desafíos.\n¡Memoria y patrones te esperan para una diversión sin límites!"
        intro_label = tk.Label(content_frame,text=intro_text, font=self.intro_font, fg="#000000",bg="#FFDCF5", justify="center", wraplength=400
        )
        intro_label.pack(pady=(0, 30))
        buttons_frame = tk.Frame(content_frame, bg="#FFDCF5")
        buttons_frame.pack(pady=20)
        button_style = {
            "font": self.custom_font,
            "width": 18,
            "height": 3,
            "relief": "raised",
            "bd": 3,
            "cursor": "hand2"
        }
        memory_btn = tk.Button(buttons_frame,text="Modo\n Clásico",command=self.open_memory_game,bg="#D00087", fg='white',activebackground="#FE28B3", activeforeground='white',
            **button_style
        )
        memory_btn.pack(pady=8)
        pattern_btn = tk.Button(buttons_frame, text="Modo\n Patrones", command=self.open_pattern_game, bg="#D00087",   fg='white', activebackground="#FE28B3", activeforeground='white',
            **button_style
        )
        pattern_btn.pack(pady=8)
        prizes_btn = tk.Button( buttons_frame, text="Premios\n🏆",  command=self.open_premios_window, bg="#D00087",   fg='white', activebackground="#FE28B3",  activeforeground='white',
            **button_style
        )
        prizes_btn.pack(pady=8)
        right_frame = tk.Frame(main_container, bg="#FFDCF5", relief="raised", bd=3)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        animation_title = tk.Label( right_frame,text="⚝¡Buena Suerte!⚝", font=("Helvetica", 20, "bold"), fg="#D00087", bg="#FFDCF5"
        )
        animation_title.pack(pady=(20, 10))
        
        # Canvas para la animación de la princesa
        self.canvas_princesa = tk.Canvas(
            right_frame,
            width=450,
            height=380,
            bg="#FFDCF5",
            highlightthickness=0
        )
        self.canvas_princesa.pack(pady=20)

        logout_btn = tk.Button(  right_frame,  text="Cerrar Sesión", command=self.cerrar_sesion, bg="#D00087",  fg='white',activebackground="#FE28B3",activeforeground='white',font=self.custom_font,width=15, height=2,relief="raised",  bd=3,  cursor="hand2"
        )
        logout_btn.pack(pady=(10, 20))

    def start_princess_animation(self):
        """Inicia la animación de la princesa si no está ya activa."""
        if not hasattr(self, '_animation_running') or not self._animation_running:
            self._animation_running = True  # Bandera para evitar duplicados
            self.princesa_recursiva(0)  # Inicia la animación desde el frame 0
    
    def princesa_recursiva(self, contador):
        """Animación recursiva de la princesa."""
        # Salida rápida si no está activa
        if not self.animation_active:
            return
        if contador > 11:
            contador = 0
        try:
            name = f"./Animacion/frame_{contador}_delay-0.1s.png"
            
            if os.path.exists(name):
                princesa = Image.open(name)
                princesa = princesa.resize((310, 360), Image.LANCZOS)
                princesa_photo = ImageTk.PhotoImage(princesa)
                self.imagenes["princesa_actual"] = princesa_photo
                self.canvas_princesa.delete("all")
                self.canvas_princesa.create_image(225, 210, image=princesa_photo, anchor="center")
            else:
                self.canvas_princesa.delete("all")
                self.canvas_princesa.create_text(
                    225, 200, 
                    text="🎮 Animación\nAquí! 🎮", 
                    font=("Helvetica", 18, "bold"),
                    fill="#8B008B",
                    justify="center"
                )
            contador += 1
            if self.animation_active:
                self.animation_job = self.root.after(150, lambda: self.princesa_recursiva(contador))
        except:
            pass  # Ignorar cualquier error
    
    def open_memory_game(self):
        """Oculta el menú y abre el modo clásico de memory game."""
        self.stop_music()
        self.root.withdraw()
        self.child_window = tk.Toplevel()
        self.child_window.protocol("WM_DELETE_WINDOW", self.return_to_main)
        app = MemoryGameGUI(self.child_window, self.play_musica, self.return_to_main,username=self.username)
    
    def open_pattern_game(self):
        """Oculta el menú y abre el modo patrones de memory game."""
        self.stop_music()
        self.root.withdraw()
        self.child_window = tk.Toplevel()
        self.child_window.protocol("WM_DELETE_WINDOW", self.return_to_main)
        app = PatternGameGUI(self.child_window, self.play_musica, self.return_to_main)

    def open_premios_window(self):
        """Abre la ventana de premios manteniendo la música del menú principal"""
        self.root.withdraw() 
        self.animation_active = False  # Pausa la animación actual
        if self.animation_job:
            self.root.after_cancel(self.animation_job) 
        premios_window = tk.Toplevel()
        premios_window.title("Ventana Premios")
        premios_window.configure(background='#D6EADF')
        window_width = 800 # CENTRAR LA VENTANA
        window_height = 600
        screen_width = premios_window.winfo_screenwidth()
        screen_height = premios_window.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        premios_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        premios_window.resizable(False, False)
        premios_window.protocol("WM_DELETE_WINDOW", lambda: self.return_from_premios_window(premios_window)) # Configura el cierre para volver al menú
        self.premios = Premios(test_mode=True)
        tk.Label(premios_window, text="MEJORES JUGADORES - JUEGO DE MEMORIA", font=("Helvetica", 16, "bold"), bg='#D6EADF', fg="#060505"
        ).pack(pady=(20, 10))
        tk.Label( premios_window, text="Premio = (1/Intentos) × 100 × Tipo de Cambio", font=("Helvetica", 10),bg='#D6EADF', fg="#060505"
        ).pack(pady=(0, 20))
        # Crear tabla
        columns = ("#", "Jugador", "Intentos", "Fecha", "Premio (₡)")
        tree = ttk.Treeview(premios_window, columns=columns, show="headings", height=7)
        tree.heading("#", text="#") # Configurar columnas
        tree.heading("Jugador", text="Jugador")
        tree.heading("Intentos", text="Intentos")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Premio (₡)", text="Premio (₡)")
        tree.column("#", width=50, anchor='center')
        tree.column("Jugador", width=150, anchor='center')
        tree.column("Intentos", width=100, anchor='center')
        tree.column("Fecha", width=150, anchor='center')
        tree.column("Premio (₡)", width=150, anchor='center')
        style = ttk.Style() # Estilo de la tabla
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        # Obtener datos
        premios = Premios(test_mode=True)  # Cambiar a test_mode=False en producción
        top5 = premios.obtener_top5()
        for i, jugador in enumerate(top5):
            tree.insert("", "end", values=(
                i + 1,
                jugador['nombre'],
                jugador['intentos'],
                jugador.get('fecha', 'N/A'),
                f"₡{jugador['premio']:.2f}"
            ))
        tree.pack(padx=20, pady=10, fill='both', expand=True)
        if not top5:
            tk.Label(premios_window,  text="¡Aún no hay jugadores registrados! Gana una partida para aparecer aquí",font=("Helvetica", 12),fg="#060505", bg='#D6EADF'
            ).pack(pady=50)
        button_frame = tk.Frame(premios_window, bg='#D6EADF')
        button_frame.pack(pady=10)
        def borrar_seleccionado():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Advertencia", "Selecciona un jugador de la tabla.")
                return 
            item = tree.item(selected[0])
            values = item['values']
            nombre = values[1]  # Columna 1 es el nombre
            intentos = int(values[2])  # Columna 2 es intentos
            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Eliminar a {nombre} con {intentos} intentos?"
            )
            if confirm:
                if self.premios.eliminar_jugador(nombre, intentos):
                    messagebox.showinfo("Éxito", "Datos eliminados correctamente.")
                    premios_window.destroy()
                    self.open_premios_window()  # Recargar ventana
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el registro.")
        tk.Button( button_frame, text="Limpiar dato", command=borrar_seleccionado,  bg="#D00087", fg='white', activebackground="#FE28B3", activeforeground='white', font=self.custom_font, width=15
        ).pack(side="left", padx=10)
        tk.Button(button_frame,text="Volver al Menú",command=lambda: self.return_from_premios_window(premios_window),  bg="#75B592",   fg="#FFFFFF", font=self.custom_font, width=15
        ).pack(side="right", padx=10)

    def return_from_premios_window(self, window):
        """Regresa al menú principal desde la ventana de premios."""
        window.destroy()
        self.root.deiconify()
        self.animation_active = True 
        self.start_princess_animation() 

    def return_to_main(self):
        """Regresa al menú principal desde los juegos."""
        self.stop_music()
        # Guardar puntaje del jugador actual 
        if hasattr(self, 'child_window') and self.child_window:
            self.child_window.destroy()
            self.play_musica("musica/pantallaprincipal.mp3")
            self.root.deiconify()

    def on_closing(self):
        """Método para manejar el cierre de la ventana principal."""
        self.stop_music()
        pygame.mixer.quit()
        self.root.destroy()

    def cerrar_sesion(self):
        """Cierra la sesión actual y regresa a la ventana de login."""
        self.animation_active = False 
        if self.animation_job:
            self.root.after_cancel(self.animation_job) 
        self.stop_music()
        pygame.mixer.quit()
        self.root.destroy()

        if self.logout_callback:
            self.logout_callback()
        else:
            from Login import LoginMemory
            root = tk.Tk()
            app = LoginMemory(root)
            root.mainloop()