import tkinter as tk
import os
import sys
from tkinter import messagebox
from Perros.vista import Frame, crear_tabla

class MenuInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú de Inicio")
        self.root.geometry("500x400")
        self.root.configure(bg='#E6F2FF')
    
        self.create_widgets()

    def create_widgets(self):
        titulo = tk.Label(
            self.root, 
            text="Sistema de Gestión de Refugio Canino", 
            font=("Arial", 16, "bold"), 
            bg='#E6F2FF', 
            fg='#1E88E5')
        titulo.pack(pady=20)
        try:
            img_dir = r'C:\Users\WINDOWS_10\Desktop\Perritos\img'
            icon_path = os.path.join(img_dir, 'favicon.ico')
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al establecer el icono: {e}")

        # Frame para botones
        frame_botones = tk.Frame(self.root, bg='#E6F2FF')
        frame_botones.pack(expand=True)

        # Botones del menú
        botones = [
            ("Gestionar Perros", self.abrir_gestion_perros),
            ("Gestionar Dueños", self.abrir_gestion_duenos),
            ("Realizar Adopción", self.abrir_adopcion),
            ("Salir", self.salir)
        ]

        for texto, comando in botones:
            boton = tk.Button(
                frame_botones, 
                text=texto, 
                command=comando, 
                width=20, 
                height=2, 
                bg="#1E88E5", 
                fg="white", 
                font=("Arial", 10, "bold"),
                relief="solid", 
                borderwidth=2
            )
            boton.pack(pady=10)

    def abrir_gestion_perros(self):
        self.root.withdraw()  # Ocultar ventana de inicio
        ventana_perros = tk.Toplevel(self.root)
        ventana_perros.title("Gestión de Perros")
        ventana_perros.geometry("600x700")
        
        frame_perros = Frame(ventana_perros)
        
        def volver_menu():
            ventana_perros.destroy()
            self.root.deiconify()
        
        # Botón de volver al menú principal
        boton_volver = tk.Button(
            ventana_perros, 
            text="Volver al Menú", 
            command=volver_menu, 
            bg="#1E88E5", 
            fg="white"
        )
        boton_volver.pack(side=tk.BOTTOM, pady=10)

    def abrir_gestion_duenos(self):
        messagebox.showinfo("En Desarrollo", "Funcionalidad de gestión de dueños próximamente.")

    def abrir_adopcion(self):
        messagebox.showinfo("En Desarrollo", "Funcionalidad de adopción próximamente.")

    def salir(self):
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro que desea salir?")
        if respuesta:
            self.root.quit()

def main():
    root = tk.Tk()
    
    # Crear tablas al iniciar la aplicación
    crear_tabla()
    
    app = MenuInicio(root)
    root.mainloop()

if __name__ == "__main__":
    main()
       

def main():
    root = tk.Tk()
    app = MenuInicio(root)
    root.mainloop()

if __name__ == "__main__":
    main()