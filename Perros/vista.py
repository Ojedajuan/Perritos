import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import date
from modelo.consultas import (
    crear_tabla, Perros, listar_perros, listar_dueños, 
    guardar_perros, update_perro, eliminar_perros,
)

class Frame(tk.Frame):
    def __init__(self, root=None):  
        super().__init__(root, width=480, height=320)
        self.root = root
        self.Id_Perro = None
        self.pack(fill=tk.BOTH, expand=True)
        self.config(bg='#E6F2FF')
        self.create_form()
        self.create_buttons()
        self.create_menu()
        self.mostrar_tabla()

    # (Otros métodos...)

    def seleccionar_registro(self, event):
        """Maneja el evento cuando un registro es seleccionado en la tabla."""
        try:
            # Obtener el ítem seleccionado
            item_seleccionado = self.tabla.selection()[0]
            self.Id_Perro = self.tabla.item(item_seleccionado)['text']
            
            # Obtener los valores del registro
            valores = self.tabla.item(item_seleccionado)['values']
            if len(valores) < 4: raise ValueError("Error: El registro seleccionado no tiene todos los valores necesarios.")
            
            # Rellenar los campos del formulario con los valores del registro seleccionado
            self.entry_fecha_ingreso.set_date(valores[0])
            self.entry_color.delete(0, tk.END)
            self.entry_color.insert(0, valores[1])
            
            # Establecer el estado en el combobox
            estado_index = self.estados.index(valores[2]) if valores[2] in self.estados else 0
            self.entry_estado.current(estado_index)
            
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, valores[3])
            
            # Habilitar los campos para edición
            self.entry_fecha_ingreso.config(state='normal')
            self.entry_color.config(state='normal')
            self.entry_estado.config(state='readonly')
            self.entry_nombre.config(state='normal')

        except IndexError:
            messagebox.showerror("Error", "No se ha seleccionado ningún registro.")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def create_form(self):
        """Crea el formulario para ingresar datos."""
        dueño_db = listar_dueños()
        self.estados = ["Seleccione uno", "disponible", "adoptado", "no adoptado",]

        self.form_frame = tk.Frame(self, bg='#E6F2FF')
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.form_frame.grid_columnconfigure(1, weight=1)

        labels_entries = [
            ("ID Perro:", tk.Entry, 'entry_id_perro', 'disabled'),
            ("Fecha de Ingreso:", DateEntry, 'entry_fecha_ingreso', 'normal'),
            ("Color:", tk.Entry, 'entry_color', 'normal'),
            ("Estado:", ttk.Combobox, 'entry_estado', 'readonly'),
            ("Nombre:", tk.Entry, 'entry_nombre', 'normal')
        ]

        for i, (label, widget_type, attr_name, state) in enumerate(labels_entries):
            tk.Label(self.form_frame, text=label, bg='#E6F2FF', font=("Arial", 10)).grid(row=i, column=0, sticky='w')
            if widget_type == ttk.Combobox:
                widget = ttk.Combobox(self.form_frame, state=state, values=self.estados)
                widget.current(0)
            elif widget_type == DateEntry:
                widget = DateEntry(self.form_frame, width=27, font=("Arial", 10), date_pattern='yyyy-mm-dd')
            else:
                widget = widget_type(self.form_frame, state=state, width=30)
            widget.grid(row=i, column=1, padx=10, pady=3, sticky='ew')
            setattr(self, attr_name, widget)

    def create_buttons(self):
        """Crea los botones para manejar el formulario."""
        button_frame = tk.Frame(self, bg='#E6F2FF')
        button_frame.grid(row=1, column=0, pady=10, sticky="ew")

        buttons = [
            ("Nuevo", self.nuevo_registro),
            ("Guardar", self.save_data),
            ("Actualizar", self.update_perro),
            ("Eliminar", self.delete_data),
            ("Limpiar", self.clear_fields)
        ]

        for col, (text, command) in enumerate(buttons):
            tk.Button(
                button_frame, text=text, command=command, width=10, height=2, bg="#1E88E5", 
                fg="white", font=("Arial", 10, "bold"), relief="solid", borderwidth=2
            ).grid(row=0, column=col, padx=5, pady=5, sticky="ew")

    def create_menu(self):
        """Crea la barra de menú."""
        barra = tk.Menu(self.root)
        self.root.config(menu=barra)

        inicio = tk.Menu(barra, tearoff=0)
        barra.add_cascade(label='Inicio', menu=inicio)
        inicio.add_command(label='Conectar DB', command=crear_tabla)
        inicio.add_command(label='Salir', command=self.root.destroy)

    def nuevo_registro(self):
        self.clear_fields()
        self.enable_fields()

    def update_perro(self):
        try:
            # Verificar que hay un elemento seleccionado
            if not self.tabla.selection():
                messagebox.showwarning("Advertencia", "Seleccione un registro para actualizar")
                return

            # Obtener el registro seleccionado
            item_seleccionado = self.tabla.selection()[0]
            self.Id_Perro = self.tabla.item(item_seleccionado)['text']

            # Obtener los valores del registro
            valores = self.tabla.item(item_seleccionado)['values']
            if len(valores) < 4:
                raise ValueError("El registro seleccionado no tiene todos los valores necesarios.")
            
            # Rellenar los campos para edición
            self.entry_fecha_ingreso.set_date(valores[0])
            self.entry_color.delete(0, tk.END)
            self.entry_color.insert(0, valores[1])
            
            # Establecer el estado en el combobox
            estado_index = self.estados.index(valores[2]) if valores[2] in self.estados else 0
            self.entry_estado.current(estado_index)
            
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, valores[3])
            
            # Habilitar campos para edición
            self.entry_fecha_ingreso.config(state='normal')
            self.entry_color.config(state='normal')
            self.entry_estado.config(state='readonly')
            self.entry_nombre.config(state='normal')

        except Exception as error:
            messagebox.showerror("Error", f"Error al preparar actualización: {error}")

    def clear_fields(self):
        """Limpia los campos del formulario."""
        self.entry_id_perro.config(state='normal')
        self.entry_id_perro.delete(0, tk.END)
        self.entry_id_perro.config(state='disabled')
        self.entry_fecha_ingreso.set_date(date.today())  # Usar fecha actual por defecto
        self.entry_color.delete(0, tk.END)
        self.entry_estado.current(0)
        self.entry_nombre.delete(0, tk.END)

    def save_data(self):
        try:
            if not self.validar_campos():
                return
            estado = self.estados[self.entry_estado.current()]
            perro = Perros(
                fecha_ingreso=self.entry_fecha_ingreso.get(),
                color=self.entry_color.get(),
                estado=estado,
                nombre=self.entry_nombre.get())
            
            if self.Id_Perro:
                perro.id_perros = self.Id_Perro
                if update_perro(perro):  # Usar la función importada
                    messagebox.showinfo("Éxito", "Registro actualizado correctamente")
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el registro")
            else:
                # Si es un nuevo registro
                guardar_perros(perro)
                messagebox.showinfo("Éxito", "Registro guardado correctamente")
            
            self.mostrar_tabla()
            self.clear_fields()
            self.Id_Perro = None  # Reiniciar el ID de perro
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def delete_data(self):
        try:
            selected_item = self.tabla.selection()
            if not selected_item:
                messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar")
                return
            self.Id_Perro = self.tabla.item(selected_item[0])['text']

            confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?")
            if confirmar:
                eliminar_perros(self.Id_Perro)  # Función externa importada
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self.mostrar_tabla()
                self.tabla.update()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar: {e}")

    def validar_campos(self):
        if not self.entry_fecha_ingreso.get() or not self.entry_color.get() or not self.entry_nombre.get() or self.entry_estado.current() == 0:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return False
        return True

    def mostrar_tabla(self):
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()

        self.tabla = ttk.Treeview(self, columns=('ID_Perro','fecha_ingreso', 'color', 'estado', 'nombre'), height=8)
        self.tabla.grid(row=4, column=0, columnspan=4, padx=10, pady=10)
        self.tabla.heading('#0', text='ID_Perro', anchor='center')
        self.tabla.heading('#1', text='FECHA INGRESO', anchor='center')
        self.tabla.heading('#2', text='COLOR', anchor='center')
        self.tabla.heading('#3', text='ESTADO', anchor='center')
        self.tabla.heading('#4', text='NOMBRE', anchor='center')

        for p in listar_perros():  # Función externa
            self.tabla.insert('', 'end', text=p[0], values=(p[1], p[2], p[3], p[4]))
        self.tabla.bind('<ButtonRelease-1>', self.seleccionar_registro)
        self.tabla.update()  

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Formulario de Perros")
    root.geometry("600x700")
    app = Frame(root)
    root.mainloop()
