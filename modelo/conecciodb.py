import sqlite3

class ConeccioDB:
    def __init__(self):
        """Inicializa la conexión a la base de datos."""
        try:
            self.base_datos = r'C:\Users\WINDOWS_10\Desktop\Perritos\data\New_dogs_db.sql'
            self.conexion = sqlite3.connect(self.base_datos)
            self.cursor = self.conexion.cursor()
            print("Conexión establecida correctamente.")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.conexion = None
            self.cursor = None

    def commit(self):
        """Confirma los cambios en la base de datos."""
        if self.conexion:
            try:
                self.conexion.commit()
                print("Cambios confirmados.")
            except sqlite3.Error as e:
                print(f"Error al confirmar los cambios: {e}")

    def cerrar_con(self):
        """Cierra la conexión a la base de datos."""
        if self.conexion:
            try:
                self.commit()
                self.conexion.close()
                print("Conexión cerrada correctamente.")
            except sqlite3.Error as e:
                print(f"Error al cerrar la conexión: {e}")
