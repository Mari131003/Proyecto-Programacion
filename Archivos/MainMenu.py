import tkinter as tk
from tkinter import font
from MemoryGameGUI import MemoryGameGUI
from PatternGameGUI import PatternGameGUI

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal")
        self.root.geometry("1200x750")
        self.custom_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.create_widgets()
        
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
    
    def open_memory_game(self):  #Método para el juego de memoria
        self.root.destroy()
        root = tk.Tk()
        app = MemoryGameGUI(root)
        root.mainloop()

        root = tk.Tk() # Volver a mostrar el menú principal
        app = MainMenu(root)
        root.mainloop()
        
    def open_pattern_game(self):  #Método para el juego de patrones
        self.root.destroy()
        root = tk.Tk()
        app = PatternGameGUI(root)  # Uso de la clase del juego de patrones
        root.mainloop()

        root = tk.Tk() # Volver a mostrar el menú principal
        app = MainMenu(root)
        root.mainloop()