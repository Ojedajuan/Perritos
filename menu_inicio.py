import tkinter as tk
import os
from tkinter import messagebox
from modelo.conecciodb import ConeccioDB
from modelo.consultas import crear_tablas
from Perros.dueños import FrameDuenos 
from Perros.vista import Frame 

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

        frame_botones = tk.Frame(self.root, bg='#E6F2FF')
        frame_botones.pack(expand=True)

        botones = [
            ("Gestionar Perros", self.abrir_gestion_perros),
            ("Gestionar duenos", self.abrir_gestion_duenos),
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
        Frame(ventana_perros)  # Usar Frame en lugar de FrameDuenos
        ventana_perros.title("Gestión de Perros")
        ventana_perros.geometry("600x700")
        
        def volver_menu():
            ventana_perros.destroy()
            self.root.deiconify()
        
        boton_volver = tk.Button(
            ventana_perros, 
            text="Volver al Menú", 
            command=volver_menu, 
            bg="#1E88E5", 
            fg="white"
        )
        boton_volver.pack(side=tk.BOTTOM, pady=10)

    def abrir_gestion_duenos(self):
        self.root.withdraw()
        ventana_duenos = tk.Toplevel(self.root)
        FrameDuenos(ventana_duenos)
        ventana_duenos.title("Gestión de Dueños")
        ventana_duenos.geometry("600x700")
        ventana_duenos.configure(bg='#E6F2FF')
        
        try:
            img_dir = r'C:\Users\WINDOWS_10\Desktop\Perritos\img'
            icon_path = os.path.join(img_dir, 'favicon.ico')
            ventana_duenos.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al establecer el icono: {e}")
    
        def volver_menu():
            ventana_duenos.destroy()
            self.root.deiconify()
        
        boton_volver = tk.Button(
            ventana_duenos, 
            text="Volver al Menú", 
            command=volver_menu, 
            bg="#1E88E5", 
            fg="white"
        )
        boton_volver.pack(side=tk.BOTTOM, pady=10)

    def abrir_adopcion(self):
        messagebox.showinfo("En Desarrollo", "Funcionalidad de adopción próximamente.")

    def salir(self):
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro que desea salir?")
        if respuesta:
            self.root.quit()
def verificar_estructura(tabla):
    conn = ConeccioDB()
    connection = conn.connect()
    cursor = connection.cursor()

    cursor.execute(f"PRAGMA table_info({tabla})")
    columnas = cursor.fetchall()
    
    print(f"📌 Estructura de la tabla '{tabla}':")
    for columna in columnas:
        print(columna)

    conn.close()

# Llamar a la función con la tabla que está dando error
verificar_estructura("Perros")  # O "DUEÑOS", según el error

def main():
    db = ConeccioDB()
    connection = db.connect()
    if connection:
        print("✅ Base de datos inicializada correctamente")
    else:
        print("❌ Error al inicializar la base de datos")
    root = tk.Tk()
    root.title("Menú de Inicio")
    root.geometry("500x400")
    root.configure(bg='#E6F2FF')
    crear_tablas()
    app = MenuInicio(root)
    root.mainloop()

if __name__ == "__main__":
    main()