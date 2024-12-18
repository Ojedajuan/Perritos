import tkinter as tk
import os
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import date

class FrameDuenos(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=480, height=320)
        self.root = root
        self.Id_Dueno = None
        self.pack(fill=tk.BOTH, expand=True)
        self.config(bg='#E6F2FF')
        self.create_form()
        self.create_buttons()
        self.mostrar_tabla()
        try:
            img_dir = r'C:\Users\WINDOWS_10\Desktop\Perritos\img'
            icon_path = os.path.join(img_dir, 'favicon.ico')
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al establecer el icono: {e}")
    def create_form(self):
        """Crea el formulario para ingresar datos de dueños."""
        self.form_frame = tk.Frame(self, bg='#E6F2FF')
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.form_frame.grid_columnconfigure(1, weight=1)

        labels_entries = [
            ("ID Dueño:", tk.Entry, 'entry_id_dueno', 'disabled'),
            ("nombre_apellido:", tk.Entry, 'normal'),
            ("Teléfono:", tk.Entry, 'entry_telefono', 'normal'),
            ("Fecha de Adopción:", DateEntry, 'entry_fecha_adopcion', 'normal'),
            ("Dirección:", tk.Entry, 'entry_direccion', 'normal'),
            ("Email:", tk.Entry, 'Email', 'normal')

        ]

        for i, (label, widget_type, attr_name, state) in enumerate(labels_entries):
            tk.Label(self.form_frame, text=label, bg='#E6F2FF', font=("Arial", 10)).grid(row=i, column=0, sticky='w')
            
            if widget_type == DateEntry:
                widget = DateEntry(self.form_frame, width=27, font=("Arial", 10), date_pattern='yyyy-mm-dd')
            else:
                widget = widget_type(self.form_frame, state=state, width=30)
            
            widget.grid(row=i, column=1, padx=10, pady=3, sticky='ew')
            setattr(self, attr_name, widget)

    def create_buttons(self):
        """Crea los botones para manejar el formulario de dueños."""
        button_frame = tk.Frame(self, bg='#E6F2FF')
        button_frame.grid(row=1, column=0, pady=10, sticky="ew")

        buttons = [
            ("Nuevo", self.nuevo_registro),
            ("Guardar", self.save_data),
            ("Actualizar", self.update_dueno),
            ("Eliminar", self.delete_data),
            ("Limpiar", self.clear_fields)
        ]

        for col, (text, command) in enumerate(buttons):
            tk.Button(
                button_frame, text=text, command=command, width=10, height=2, 
                bg="#1E88E5", fg="white", font=("Arial", 10, "bold"), 
                relief="solid", borderwidth=2
            ).grid(row=0, column=col, padx=5, pady=5, sticky="ew")

    def nuevo_registro(self):
        """Prepara un nuevo registro de dueño."""
        self.clear_fields()
        self.enable_fields()

    def enable_fields(self):
        """Habilita los campos para edición."""
        campos = [
            self.entry_nombre, 
            self.entry_apellido, 
            self.entry_telefono, 
            self.entry_fecha_adopcion, 
            self.entry_direccion,
            self.entry_Email
        ]
        for campo in campos:
            campo.config(state='normal')

    def seleccionar_registro(self, event):
        """Maneja el evento cuando un registro de dueño es seleccionado."""
        try:
            item_seleccionado = self.tabla.selection()[0]
            self.Id_Dueno = self.tabla.item(item_seleccionado)['text']
            
            valores = self.tabla.item(item_seleccionado)['values']
            if len(valores) < 5: 
                raise ValueError("Error: El registro seleccionado no tiene todos los valores necesarios.")
            
            # Rellenar los campos del formulario
            self.entry_nombre_apellido.delete(0, tk.END)
            self.entry_nombre_apellido.insert(0, valores[0])
            
            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, valores[2])
            
            self.entry_fecha_adopcion.set_date(valores[3])
            
            self.entry_direccion.delete(0, tk.END)
            self.entry_direccion.insert(0, valores[4])

            self.entry_Email.delete(0,tk.END)
            self.entry_Email.insert(0, valores[5])
            
            # Habilitar campos para edición
            self.enable_fields()

        except IndexError:
            messagebox.showerror("Error", "No se ha seleccionado ningún registro.")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def clear_fields(self):
        """Limpia los campos del formulario de dueños."""
        self.entry_id_dueno.config(state='normal')
        self.entry_id_dueno.delete(0, tk.END)
        self.entry_id_dueno.config(state='disabled')
        
        self.entry_nombre_apellido.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_fecha_adopcion.set_date(date.today())
        self.entry_direccion.delete(0, tk.END)
        self.entry_Email.delete(0,tk.END)

    def validar_campos(self):
        """Valida que los campos obligatorios estén llenos."""
        if (not self.entry_nombre_apellido.get() or 
            not self.entry_telefono.get() or 
            not self.entry_fecha_adopcion.get() or 
            not self.entry_direccion.get()or
            not self.entry_Email.get()) :
            
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return False
        return True

    def save_data(self):
        """Guarda o actualiza un registro de dueño."""
        try:
            if not self.validar_campos():
                return
            
            # Aquí deberías importar y usar tu modelo de Dueños
            # Por ejemplo: 
            # dueno = Duenos(
            #     nombre_apellido_apellido=self.entry_nombre_apellido.get(),
            #     apellido=self.entry_apellido.get(),
            #     telefono=self.entry_telefono.get(),
            #     fecha_adopcion=self.entry_fecha_adopcion.get(),
            #     direccion=self.entry_direccion.get()
            # )
            
            if self.Id_Dueno:
                # Código para actualizar
                # update_dueno(dueno)
                messagebox.showinfo("Éxito", "Registro actualizado correctamente")
            else:
                # Código para guardar nuevo
                # guardar_duenos(dueno)
                messagebox.showinfo("Éxito", "Registro guardado correctamente")
            
            self.mostrar_tabla()
            self.clear_fields()
            self.Id_Dueno = None
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def update_dueno(self):
        """Prepara un registro de dueño para actualización."""
        try:
            if not self.tabla.selection():
                messagebox.showwarning("Advertencia", "Seleccione un registro para actualizar")
                return

            item_seleccionado = self.tabla.selection()[0]
            self.Id_Dueno = self.tabla.item(item_seleccionado)['text']
            
            # Similar a seleccionar_registro(), pero preparando para edición
            valores = self.tabla.item(item_seleccionado)['values']
            
            self.entry_nombre_apellido_apellido.delete(0, tk.END)
            self.entry_nombre_apellido_apellido.insert(0, valores[0])
            
            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, valores[2])
            
            self.entry_fecha_adopcion.set_date(valores[3])
            
            self.entry_direccion.delete(0, tk.END)
            self.entry_direccion.insert(0, valores[4])
            
            self.enable_fields()

        except Exception as error:
            messagebox.showerror("Error", f"Error al preparar actualización: {error}")

    def delete_data(self):
        """Elimina un registro de dueño."""
        try:
            selected_item = self.tabla.selection()
            if not selected_item:
                messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar")
                return
            
            self.Id_Dueno = self.tabla.item(selected_item[0])['text']

            confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?")
            if confirmar:
                # Aquí deberías usar tu función de eliminación
                # eliminar_duenos(self.Id_Dueno)
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self.mostrar_tabla()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar: {e}")

    def mostrar_tabla(self):
        """Muestra la tabla de dueños."""
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()
        
        # Aquí deberías usar tu función de listar dueños
        # self.lista_d = listar_duenos()
        
        self.tabla = ttk.Treeview(self, columns=('nombre_apellido_apellido', 'apellido', 'telefono', 'fecha_adopcion', 'direccion'), height=8)
        self.tabla.grid(row=4, column=0, columnspan=4, padx=10, pady=10)
        
        self.tabla.heading('#0', text='ID Dueño', anchor='center')
        self.tabla.heading('#1', text='nombre_apellido', anchor='center')
        self.tabla.heading('#2', text='APELLIDO', anchor='center')
        self.tabla.heading('#3', text='TELÉFONO', anchor='center')
        self.tabla.heading('#4', text='FECHA ADOPCIÓN', anchor='center')
        self.tabla.heading('#5', text='DIRECCIÓN', anchor='center')

        # Ejemplo de inserción de datos (comentado porque necesitarás tu propia función de listado)
        # for d in listar_duenos():
        #     self.tabla.insert('', 'end', text=d[0], values=(d[1], d[2], d[3], d[4], d[5]))
        
        self.tabla.bind('<ButtonRelease-1>', self.seleccionar_registro)
        self.tabla.update()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Formulario de Dueños")
    root.geometry("600x700")
    app = FrameDuenos(root)
    root.mainloop()

