import tkinter as tk
from tkinter import messagebox
import os
import time
from MainMenu import MainMenu
from face_gui import Face_Recognition

class LoginMemory:
    def __init__(self, root):
        self.root = root
        self.face_window = None
        self.root.title("Log in")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#FFEBD7")
        self.center_window()
        self.primary_color = "#FFB347"     # Colores 
        self.secondary_color = "#FFD89C"   
        self.accent_color = "#FF8C00"     
        self.text_color = "#000000"       
        self.users = {}
        self.load_users()
        self.create_login_widgets()
        self.create_register_widgets()
        self.show_login_window()

    def load_users(self):
        """Carga los usuarios desde el archivo users.txt"""
        if os.path.exists("users.txt"):
            try:
                with open("users.txt", "r") as f:
                    for line in f:
                        if ":" in line:
                            username, password = line.strip().split(":")
                            self.users[username] = password
            except:
                self.users = {}
    
    def save_users(self):
        """Guarda los usuarios en el archivo users.txt"""
        with open("users.txt", "w") as f:
            for username, password in self.users.items():
                f.write(f"{username}:{password}\n")

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (500 // 2)
        self.root.geometry(f'400x500+{x}+{y}')
    
    def create_login_widgets(self):
        """Crea los widgets para el login"""
        self.login_frame = tk.Frame(self.root, bg="#FFEBD7")
        logo_label = tk.Label(self.login_frame, text="Memory Game", font=("Arial", 28, "bold"), fg="#000000",bg="#FFEBD7"
        )
        logo_label.pack(pady=(10, 30))
        form_frame = tk.Frame(self.login_frame, bg=self.secondary_color, padx=20, pady=20)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label(form_frame, text="Usuario", font=("Arial", 10), bg=self.secondary_color,fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        self.username_entry = tk.Entry(form_frame, font=("Arial", 12), bg="white",relief=tk.FLAT
        )
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        tk.Label(form_frame, text="Contraseña", font=("Arial", 10),  bg=self.secondary_color,fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        self.password_entry = tk.Entry( form_frame,  font=("Arial", 12),  show="*",  bg="white",relief=tk.FLAT
        )
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        tk.Button(form_frame, text="Iniciar sesión", font=("Arial", 12, "bold"),  bg=self.primary_color,fg="white", activebackground=self.accent_color, activeforeground="white",  relief=tk.FLAT, command=self.login
        ).pack(fill=tk.X, pady=(0, 15))
        tk.Button(                           form_frame,  text="Reconocimiento facial", font=("Arial", 10), bg=self.secondary_color,fg=self.text_color,activebackground=self.secondary_color, activeforeground=self.text_color,relief=tk.RAISED, highlightbackground="black",  highlightthickness=2,command=self.face_recognition
        ).pack(fill=tk.X)
        tk.Frame(self.login_frame, height=1, bg="lightgray").pack(fill=tk.X, pady=10) # Separador
        tk.Button( self.login_frame, text="Crear cuenta nueva", font=("Arial", 12),  bg="#000000", fg="white", activebackground="#000000", activeforeground="white", relief=tk.FLAT,command=self.show_register_window
        ).pack(fill=tk.X, pady=(5, 15))

    def create_register_widgets(self):
        """Crea los widgets para el registro"""
        self.register_frame = tk.Frame(self.root, bg="#FFEBD7")
        tk.Label( self.register_frame,   text="Registro",   font=("Arial", 24, "bold"),   fg=self.accent_color,    bg="#FFEBD7"
        ).pack(pady=(10, 30))
        form_frame = tk.Frame(self.register_frame, bg=self.secondary_color, padx=20, pady=20)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label( form_frame,   text="Nuevo usuario",  font=("Arial", 10),   bg=self.secondary_color,   fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        self.new_user_entry = tk.Entry( form_frame,   font=("Arial", 12),   bg="white",  relief=tk.FLAT
        )
        self.new_user_entry.pack(fill=tk.X, pady=(0, 15))
        tk.Label( form_frame, text="Nueva contraseña",  font=("Arial", 10),  bg=self.secondary_color, fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        self.new_pass_entry = tk.Entry( form_frame,   font=("Arial", 12),    show="*",   bg="white",  relief=tk.FLAT
        )
        self.new_pass_entry.pack(fill=tk.X, pady=(0, 20))
        tk.Label( form_frame,  text="Confirmar contraseña",   font=("Arial", 10),  bg=self.secondary_color, fg=self.text_color
        ).pack(anchor="w", pady=(0, 5))
        self.confirm_pass_entry = tk.Entry(form_frame,  font=("Arial", 12),   show="*",  bg="white", relief=tk.FLAT
        )
        self.confirm_pass_entry.pack(fill=tk.X, pady=(0, 20))
        tk.Button(form_frame,  text="Registrarse",  font=("Arial", 12, "bold"),  bg=self.primary_color, fg="white",activebackground=self.accent_color,  activeforeground="white",  relief=tk.FLAT, command=self.register_user
        ).pack(fill=tk.X, pady=(0, 15))
        tk.Button( self.register_frame,  text="Volver al login",   font=("Arial", 10),   bg="#FFEBD7", fg=self.text_color, activebackground="#FFEBD7",   activeforeground=self.text_color,  relief=tk.RAISED,  highlightbackground="black", highlightthickness=2,  command=self.show_login_window
        ).pack(pady=(20, 0))
    
    def show_login_window(self):
        """Muestra la ventana de login y oculta la de registro"""
        self.register_frame.pack_forget()
        self.login_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def show_register_window(self):
        """Muestra la ventana de registro y oculta la de login"""
        self.login_frame.pack_forget()
        self.register_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def login(self):
        """Valida credenciales de usuario y abre el menú principal."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Por favor ingresa usuario y contraseña")
            return
        if username in self.users and self.users[username] == password:
            self.open_main_menu(username)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def open_main_menu(self, username):
        """Cierra el login y abre el MainMenu"""
        self.root.destroy()  # DESTRUIR en lugar de withdraw
        root = tk.Tk()
        app = MainMenu(root, username)  # SIN callback
        root.mainloop()
    
    def register_user(self):
        """Obtiene y guarda el usuario y la contraeña de alguien al registrarse"""
        username = self.new_user_entry.get()
        password = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return
        if password != confirm_pass:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        if username in self.users:
            messagebox.showerror("Error", "El usuario ya existe")
            return
        self.users[username] = password # Guardar nuevo usuario
        self.save_users()  # Guardar en archivo
        messagebox.showinfo("Éxito", "¡Registro exitoso!")
        self.show_login_window()
 
    def face_recognition(self):
        """Abre el sistema de reconocimiento facial"""
        try:
            self.root.destroy()
            root = tk.Tk()
            app = Face_Recognition(root)
            root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir reconocimiento facial: {e}")

    def create_new_login(self):
        """Crea una nueva ventana de login después del logout"""
        root = tk.Tk()
        app = LoginMemory(root)
        root.mainloop()