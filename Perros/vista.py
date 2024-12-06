import tkinter as tk
import os
import tkinter as tk
from tkinter import messagebox



class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=480, height=320)
        self.root = root
        self.pack(fill=tk.BOTH, expand=True)
        self.config(bg='#E6F2FF')
        self.label_form()

    def label_form(self):
        self.label_id_perro = tk.Label(self, text="ID_PERRO:", font=('Arial', 12, 'bold'))
        self.label_id_perro.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        self.label_fecha_ingreso = tk.Label(self, text="FECHA_INGRESO:", font=('Arial', 12, 'bold'))
        self.label_fecha_ingreso.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.label_color = tk.Label(self, text="COLOR:", font=('Arial', 12, 'bold'))
        self.label_color.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.label_fecha_adopcion = tk.Label(self, text="FECHA_ADOPCION:", font=('Arial', 12, 'bold'))
        self.label_fecha_adopcion.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        self.label_estado = tk.Label(self, text="ESTADO:", font=('Arial', 12, 'bold'))
        self.label_estado.grid(row=4, column=0, padx=10, pady=10, sticky='e')

        self.label_nombre = tk.Label(self, text="NOMBRE:", font=('Arial', 12, 'bold'))
        self.label_nombre.grid(row=5, column=0, padx=10, pady=10, sticky='e')

def mostrar_contacto():
    messagebox.showinfo("Contacto", "Correo: taraguipora2005@gmail.com")
    
def barrita_menu(root):
    barra = tk.Menu(root)
    root.config(menu=barra, width=300, height=300)
    menu_inicio = tk.Menu(barra, tearoff=0)
    menu_inicio2=tk.Menu(barra,tearoff=0)
    barra.add_cascade(label='Inicio', menu=menu_inicio)
    barra.add_cascade(label='Opciones', menu=menu_inicio2)
    menu_inicio.add_command(label='Conectar DB')
    menu_inicio.add_command(label='Desconectar DB')
    menu_inicio.add_command(label='Salir', command=root.destroy)
    menu_inicio2.add_command(label='Contacto', command=mostrar_contacto)
