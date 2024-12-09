import tkinter as tk 
from tkinter import messagebox, ttk
from tkcalendar import DateEntry  # Importar DateEntry

class ToolTip:
    """Tooltips para widgets."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, bg="lightyellow",
                         relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=480, height=320)
        self.root = root
        self.pack(fill=tk.BOTH, expand=True)
        self.config(bg='#E6F2FF')
        self.create_form()
        self.create_buttons()  # Asegúrate de llamar después de que 'create_buttons' esté definida
        self.barrita_menu()

    def create_form(self):
        """Formulario compacto con estilos uniformes."""
        self.form_frame = tk.Frame(self, bg='#E6F2FF')
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.form_frame.grid_columnconfigure(1, weight=1)

        label_style = {'font': ("Arial", 10), 'bg': '#E6F2FF',
                       'fg': 'black', 'anchor': 'w', 'padx': 10, 'pady': 3}
        entry_style = {'width': 30, 'font': ("Arial", 10),
                       'relief': 'solid', 'borderwidth': 1}

        fields = [
            ("ID Perro:", tk.Entry, 'entry_id_perro'),
            ("Fecha de Ingreso:", DateEntry, 'entry_fecha_ingreso'),
            ("Color:", tk.Entry, 'entry_color'),
            ("Estado:", ttk.Combobox, 'entry_estado'),
            ("Nombre:", tk.Entry, 'entry_nombre')
        ]

        for row, (text, widget_type, attr_name) in enumerate(fields):
            tk.Label(self.form_frame, text=text, **label_style).grid(
                row=row, column=0, sticky='w')
            if widget_type == ttk.Combobox:
                widget = ttk.Combobox(self.form_frame, state="readonly",
                                      values=["Disponible", "En Adopción", "Adoptado", "No Adoptable"],
                                      width=27)
            elif widget_type == DateEntry:
                widget = DateEntry(self.form_frame, width=27, font=("Arial", 10),
                                   date_pattern='yyyy-mm-dd',  # Formato de fecha
                                   background='lightblue', foreground='black', borderwidth=1)
            else:
                widget = widget_type(self.form_frame, **entry_style)
            widget.grid(row=row, column=1, padx=10, pady=3, sticky='ew')
            setattr(self, attr_name, widget)

    def create_buttons(self):
        button_frame = tk.Frame(self, bg='#E6F2FF')
        button_frame.grid(row=1, column=0, pady=10, sticky="ew")
        buttons = [
            ("Guardar", self.save_data, "Guardar los datos ingresados."),
            ("Actualizar", self.update_data, "Actualizar datos existentes."),
            ("Eliminar", self.delete_data, "Eliminar los datos seleccionados."),
            ("Limpiar", self.clear_fields, "Limpiar todos los campos del formulario.")
        ]

        for col, (text, command, tooltip) in enumerate(buttons):
            self.create_button(button_frame, text, command, col, tooltip)

    def create_button(self, parent, text, command, column, tooltip=None):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=12,
            height=2,
            relief="solid",
            borderwidth=2,
            bg="#1E88E5",
            fg="white",
            font=("Arial", 10, "bold"),
            activebackground="#1565C0",
            activeforeground="white"
        )
        button.grid(row=0, column=column, padx=10, pady=5, sticky="ew")
        if tooltip:
            ToolTip(button, tooltip)

    def habilitar_campos(self):
        """Habilita los campos para que puedan ser editados."""
        self.entry_id_perro.config(state='normal')
        self.entry_fecha_ingreso.config(state='normal')
        self.entry_color.config(state='normal')
        self.entry_estado.config(state='normal')
        self.entry_nombre.config(state='normal')

    def bloquear_campos(self):
        """Bloquea los campos para que no puedan ser editados."""
        self.entry_id_perro.config(state='disabled')
        self.entry_fecha_ingreso.config(state='disabled')
        self.entry_color.config(state='disabled')
        self.entry_estado.config(state='disabled')
        self.entry_nombre.config(state='disabled')

    def barrita_menu(self):
        barra = tk.Menu(self.root)
        self.root.config(menu=barra)
        inicio = tk.Menu(barra, tearoff=0)
        opciones = tk.Menu(barra, tearoff=0)
        barra.add_cascade(label='Inicio', menu=inicio)
        barra.add_cascade(label='Opciones', menu=opciones)
        inicio.add_command(label='Conectar DB')
        inicio.add_command(label='Desconectar DB')
        inicio.add_command(label='Salir', command=self.root.destroy)
        opciones.add_command(label='Contacto', command=self.mostrar_contacto)

    def mostrar_contacto(self):
        messagebox.showinfo("Contacto", "Correo: taraguipora2005@gmail.com")

    def save_data(self):
        print(f"Fecha ingresada: {self.entry_fecha_ingreso.get()}")

    def update_data(self):
        """Se habilitan los campos para poder editarlos."""
        print("Modo de actualización. Campos habilitados.")
        self.habilitar_campos()

    def delete_data(self):
        print("Datos eliminados.")

    def clear_fields(self):
        """Se bloquean los campos y limpiamos los valores."""
        print("Campos limpiados. Campos bloqueados.")
        # Limpiar los campos de entrada
        self.entry_id_perro.delete(0, tk.END)  # Limpiar Entry
        self.entry_fecha_ingreso.delete(0, tk.END)  # Limpiar Entry
        self.entry_color.delete(0, tk.END)  # Limpiar Entry
        self.entry_estado.set('')  # Limpiar Combobox
        self.entry_nombre.delete(0, tk.END)  # Limpiar Entry
        
        # Bloquear los campos después de limpiarlos
        self.bloquear_campos()

# Aplicación principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Formulario de Perros")
    app = Frame(root)
    root.mainloop()
