import tkinter as tk
from MainMenu import MainMenu
from Login import LoginMemory

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginMemory(root)
    def on_login_success(username): # Esta función se llamará cuando el login sea exitoso
        login_app.login_frame.pack_forget() # Limpiamos la ventana del login
        global app
        app = MainMenu(root)
    login_app.on_login_success = on_login_success# Asignamos la función de callback al login
    
    root.mainloop()