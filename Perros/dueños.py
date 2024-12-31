import tkinter as tk
import os
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import date
from modelo.consultas import guardar_dueno,listar_duenos,actualizar_dueno,eliminar_dueno

class duenos:
    """Clase que representa un dueno de mascota."""
    def __init__(self, nombre_apellido, dni, email, telefono, fecha_adopcion, id_perro, id_duenos=None):
        self.id_duenos = id_duenos
        self.nombre_apellido = nombre_apellido
        self.dni = dni
        self.email = email
        self.telefono = telefono
        self.fecha_adopcion = fecha_adopcion
        self.id_perro = id_perro

class FrameDuenos(tk.Frame):
    """Frame principal para la gestión de duenos de mascotas."""
    def __init__(self, root=None):
        super().__init__(root, width=480, height=320)
        self.root = root
        self.Id_Dueno = None
        self.pack(fill=tk.BOTH, expand=True)
        self.config(bg='#E6F2FF')
        self.create_form()
        self.create_buttons()
        self.mostrar_tabla()
        self.setup_icon()

    def setup_icon(self):
        """Configura el ícono de la ventana."""
        try:
            img_dir = r'C:\Users\WINDOWS_10\Desktop\Perritos\img'
            icon_path = os.path.join(img_dir, 'favicon.ico')
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error al establecer el icono: {e}")

    def create_form(self):
        """Crea el formulario para ingresar datos de duenos."""
        self.form_frame = tk.Frame(self, bg='#E6F2FF')
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.form_frame.grid_columnconfigure(1, weight=1)

        labels_entries = [
            ("ID dueno:", tk.Entry, 'entry_id_dueno', 'disabled'),
            ("Nombre y Apellido:", tk.Entry, 'entry_nombre_apellido', 'normal'),
            ("Teléfono:", tk.Entry, 'entry_telefono', 'normal'),
            ("Fecha de Adopción:", DateEntry, 'entry_fecha_adopcion', 'normal'),
            ("Email:", tk.Entry, 'entry_email', 'normal'),
            ("ID Perro:", tk.Entry, 'entry_id_perro', 'normal')
        ]

        for i, (label, widget_type, attr_name, state) in enumerate(labels_entries):
            tk.Label(self.form_frame, text=label, bg='#E6F2FF', font=("Arial", 10)).grid(
                row=i, column=0, sticky='w', padx=5
            )
            
            if widget_type == DateEntry:
                widget = DateEntry(
                    self.form_frame, 
                    width=27, 
                    font=("Arial", 10), 
                    date_pattern='yyyy-mm-dd'
                )
            else:
                widget = widget_type(
                    self.form_frame, 
                    state=state, 
                    width=30
                )
            
            widget.grid(row=i, column=1, padx=10, pady=3, sticky='ew')
            setattr(self, attr_name, widget)

    def create_buttons(self):
        """Crea los botones para manejar el formulario de duenos."""
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
        """Prepara un nuevo registro de dueno."""
        self.clear_fields()
        self.enable_fields()

    def enable_fields(self):
        """Habilita los campos para edición."""
        campos = [
            self.entry_nombre_apellido,  
            self.entry_telefono, 
            self.entry_fecha_adopcion, 
            self.entry_email,
            self.entry_id_perro
        ]
        for campo in campos:
            campo.config(state='normal')

    def seleccionar_registro(self, event):
        """Maneja la selección de un registro en la tabla."""
        try:
            item_seleccionado = self.tabla.selection()[0]
            self.Id_Dueno = self.tabla.item(item_seleccionado)['text']
            
            valores = self.tabla.item(item_seleccionado)['values']
            if len(valores) < 5:
                raise ValueError("Error: El registro seleccionado no tiene todos los valores necesarios.")
            
            self.entry_id_dueno.config(state='normal')
            self.entry_id_dueno.delete(0, tk.END)
            self.entry_id_dueno.insert(0, self.Id_Dueno)
            self.entry_id_dueno.config(state='disabled')
            
            self.entry_nombre_apellido.delete(0, tk.END)
            self.entry_nombre_apellido.insert(0, valores[0])
            
            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, valores[1])
            
            self.entry_fecha_adopcion.set_date(valores[2])
            
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, valores[3])

            self.entry_id_perro.delete(0, tk.END)
            self.entry_id_perro.insert(0, valores[4])
            
            self.enable_fields()

        except IndexError:
            messagebox.showerror("Error", "No se ha seleccionado ningún registro.")
        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def clear_fields(self):
        """Limpia los campos del formulario de duenos."""
        self.entry_id_dueno.config(state='normal')
        self.entry_id_dueno.delete(0, tk.END)
        self.entry_id_dueno.config(state='disabled')
        
        self.entry_nombre_apellido.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_fecha_adopcion.set_date(date.today())
        self.entry_email.delete(0, tk.END)
        self.entry_id_perro.delete(0, tk.END)

    def validar_campos(self):
        """Valida que los campos obligatorios estén llenos."""
        if (not self.entry_nombre_apellido.get() or 
            not self.entry_telefono.get() or 
            not self.entry_fecha_adopcion.get() or 
            not self.entry_email.get() or
            not self.entry_id_perro.get()):
            
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
            return False
        return True

    def save_data(self):
        """Guarda o actualiza un registro de dueno."""
        try:
            if not self.validar_campos():
                return
            
            from modelo.consultas import guardar_dueno, actualizar_dueno
            
            dueno = duenos(
                nombre_apellido=self.entry_nombre_apellido.get(),
                dni=None,
                email=self.entry_email.get(),
                telefono=self.entry_telefono.get(),
                fecha_adopcion=self.entry_fecha_adopcion.get(),
                id_perro=self.entry_id_perro.get(),
                id_dueno=self.Id_Dueno if self.Id_Dueno else None
            )
            
            if self.Id_Dueno:
                if actualizar_dueno(dueno):
                    messagebox.showinfo("Éxito", "Registro actualizado correctamente")
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el registro")     
            else:
                if guardar_dueno(dueno):
                    messagebox.showinfo("Éxito", "Registro guardado correctamente")
                else:
                    messagebox.showerror("Error", "No se pudo guardar el registro")
            
            self.mostrar_tabla()
            self.clear_fields()
            self.Id_Dueno = None

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def update_dueno(self):
        """Prepara un registro de dueno para actualización."""
        try:
            if not self.tabla.selection():
                messagebox.showwarning("Advertencia", "Seleccione un registro para actualizar")
                return

            item_seleccionado = self.tabla.selection()[0]
            self.Id_Dueno = self.tabla.item(item_seleccionado)['text']
            
            valores = self.tabla.item(item_seleccionado)['values']
            
            self.entry_nombre_apellido.delete(0, tk.END)
            self.entry_nombre_apellido.insert(0, valores[0])
            
            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, valores[1])
            
            self.entry_fecha_adopcion.set_date(valores[2])
            
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, valores[3])

            self.entry_id_perro.delete(0, tk.END)
            self.entry_id_perro.insert(0, valores[4])
            
            self.enable_fields()

        except Exception as error:
            messagebox.showerror("Error", f"Error al preparar actualización: {error}")

    def delete_data(self):
        """Elimina un registro de dueno."""
        try:
            from modelo.consultas import eliminar_dueno
            selected_item = self.tabla.selection()
            if not selected_item:
                messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar")
                return
            
            self.Id_Dueno = self.tabla.item(selected_item[0])['text']

            confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?")
            if confirmar:
                if eliminar_dueno(self.Id_Dueno):
                    messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                    self.mostrar_tabla()
                    self.clear_fields()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el registro")    
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar: {e}")

    def mostrar_tabla(self):
        """Muestra la tabla de duenos."""
        from modelo.consultas import listar_duenos
        
        # Eliminar tabla existente si hay una
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Treeview):
                widget.destroy()
        
        # Crear nueva tabla
        self.tabla = ttk.Treeview(
            self, 
            columns=('nombre_apellido', 'telefono', 'fecha_adopcion', 'email', 'id_perro'),
            height=8
        )
        self.tabla.grid(row=4, column=0, columnspan=4, padx=10, pady=10)
        
        # Configurar encabezados
        self.tabla.heading('#0', text='ID dueno', anchor='center')
        self.tabla.heading('#1', text='Nombre y Apellido', anchor='center')
        self.tabla.heading('#2', text='Teléfono', anchor='center')
        self.tabla.heading('#3', text='Fecha de Adopción', anchor='center')
        self.tabla.heading('#4', text='Email', anchor='center')
        self.tabla.heading('#5', text='ID Perro', anchor='center')
        
        # Cargar datos
        for d in listar_duenos():
            self.tabla.insert('', 'end', text=d[0], values=(d[1], d[2], d[3], d[4], d[5]))
        
        # Vincular evento de selección
        self.tabla.bind('<ButtonRelease-1>', self.seleccionar_registro)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Formulario de duenos")
    root.geometry("600x700")
    app = FrameDuenos(root)
    root.mainloop()