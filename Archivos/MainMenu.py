import tkinter as tk
from tkinter import font
from MemoryGameGUI import MemoryGameGUI
from PatternGameGUI import PatternGameGUI
from Premios import Premios
import pygame
import os

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal")
        self.root.geometry("1200x750")
        self.custom_font = font.Font(family="Helvetica", size=12, weight="bold")
        pygame.mixer.init()
        self.current_music=None
        self.play_musica("musica/pantallaprincipal.mp3")
        self.create_widgets()
        self.child_window = None

    def play_musica(self,file_path,loop=True):
        if not os.path.exists(file_path):
            print("Audio no encontrado:,{file_path}")
            return
        if self.current_music== file_path and pygame.mixer.music.get_busy():
            return
        
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(0.4)
            if loop:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.play()
            self.current_music= file_path
        except Exception as e:
            print(f"Error al reproducir música: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music=None
        
    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, padx=50, pady=50)
        tk.Label(main_frame, 
                text="Bienvenidos a los Juegos", 
                font=("Helvetica", 16, "bold"),
                fg="#000000").pack(pady=(0, 30))
        memory_btn = tk.Button(
            main_frame,
            text="Juego de Memoria",
            command=self.open_memory_game,
            bg="#B22F70",
            fg='white',
            activebackground='#FF1493',
            activeforeground='white',
            font=self.custom_font,
            width=20,
            height=2
        )
        memory_btn.pack(pady=10)
        game2_btn = tk.Button(
            main_frame,
            text="Juego de Patrones",
            command=self.open_pattern_game, 
            bg="#B22F70",
            fg='white',
            activebackground='#FF1493',
            activeforeground='white',
            font=self.custom_font,
            width=20,
            height=2
        )
        game2_btn.pack(pady=10)
        api_btn = tk.Button(
            main_frame,
            text="Premios",
            command=self.open_premios_window,  # Nueva función
            bg="#B22F70",  # Color diferente
            fg='white',
            activebackground='#FF1493',
            activeforeground='white',
            font=self.custom_font,
            width=20,
            height=2
        )
        api_btn.pack(pady=10)
    
    def open_memory_game(self):
        self.stop_music()
        self.root.withdraw()  # Ocultar en lugar de destruir
    
        self.child_window = tk.Toplevel()
        self.child_window.protocol("WM_DELETE_WINDOW", self.return_to_main)
        app = MemoryGameGUI(self.child_window, self.play_musica, self.return_to_main)
    
    def open_pattern_game(self):
        self.stop_music()
        self.root.withdraw()  # Ocultar en lugar de destruir
    
        self.child_window = tk.Toplevel()
        self.child_window.protocol("WM_DELETE_WINDOW", self.return_to_main)
        app = PatternGameGUI(self.child_window, self.play_musica, self.return_to_main)

    def open_premios_window(self):
        """Abre la nueva ventana manteniendo la música del menú principal"""
        self.root.withdraw()  # Oculta la ventana principal
    
        # Crea la nueva ventana
        premios_window = tk.Toplevel()
        premios_window.title("Ventana Premios")
        premios_window.geometry("800x600")
    
        # Configura el cierre para volver al menú
        premios_window.protocol("WM_DELETE_WINDOW", lambda: self.return_from_premios_window(premios_window))
        self.premios = Premios(test_mode=True)
    
        # Botón para volver
        back_btn = tk.Button(
            premios_window,
            text="Volver al Menú",
            command=lambda: self.return_from_premios_window(premios_window),
            bg="#4B0082",
            fg='white',
            font=self.custom_font
        )
        back_btn.pack(pady=20,side='bottom')

    def return_from_premios_window(self, window):
        """Regresa al menú principal desde la nueva ventana"""
        window.destroy()
        self.root.deiconify()

    def return_to_main(self):
        if self.child_window:
            self.child_window.destroy()
        self.play_musica("musica/pantallaprincipal.mp3")
        self.root.deiconify()  # Mostrar nuevamente la ventana principal
    