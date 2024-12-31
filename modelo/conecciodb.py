# conecciodb.py
import sqlite3
import os

class ConeccioDB:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.db_path = os.path.join(self.base_dir, 'data', 'dogs_database.db.sql')
        self.connection = None

    def connect(self):
        try:
            print(f"Attempting to connect to database at: {self.db_path}")
            self.connection = sqlite3.connect(self.db_path)
            print(f"Database connection established successfully to {self.db_path}")
            return self.connection
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

# consultas.py
from modelo.conecciodb import ConeccioDB

def crear_tabla():
    try:
        conn = ConeccioDB()
        connection = conn.connect()
        if connection:
            cursor = connection.cursor()
            
            # Create tables
            sql = """
            CREATE TABLE IF NOT EXISTS perros (
                id_perro INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                raza TEXT NOT NULL,
                edad INTEGER,
                estado TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS dueños (
                id_dueño INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_apellido TEXT NOT NULL,
                dni TEXT,
                telefono TEXT NOT NULL,
                fecha_adopcion DATE NOT NULL,
                email TEXT NOT NULL,
                id_perro INTEGER,
                FOREIGN KEY (id_perro) REFERENCES perros(id_perro)
            );
            """
            cursor.executescript(sql)
            connection.commit()
            print("Tables created successfully")
            conn.close()
            return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        if connection:
            conn.close()
        return False

def guardar_dueno(dueno_dict):
    try:
        conn = ConeccioDB()
        connection = conn.connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO dueños (nombre_apellido, dni, telefono, fecha_adopcion, email, id_perro)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                dueno_dict['nombre_apellido'],
                dueno_dict['dni'],
                dueno_dict['telefono'],
                dueno_dict['fecha_adopcion'],
                dueno_dict['email'],
                dueno_dict['id_perro']
            ))
            connection.commit()
            conn.close()
            return True
    except Exception as e:
        print(f"Error al guardar dueño: {e}")
        if 'connection' in locals() and connection:
            conn.close()
        return False

def listar_duenos():
    try:
        conn = ConeccioDB()
        connection = conn.connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_dueño, nombre_apellido, telefono, fecha_adopcion, email, id_perro
                FROM dueños
                ORDER BY id_dueño
            """)
            duenos = cursor.fetchall()
            conn.close()
            return duenos
    except Exception as e:
        print(f"Error al listar dueños: {e}")
        if 'connection' in locals() and connection:
            conn.close()
        return []

def actualizar_dueno(dueno_dict):
    try:
        conn = ConeccioDB()
        connection = conn.connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE dueños
                SET nombre_apellido = ?,
                    dni = ?,
                    telefono = ?,
                    fecha_adopcion = ?,
                    email = ?,
                    id_perro = ?
                WHERE id_dueño = ?
            """, (
                dueno_dict['nombre_apellido'],
                dueno_dict['dni'],
                dueno_dict['telefono'],
                dueno_dict['fecha_adopcion'],
                dueno_dict['email'],
                dueno_dict['id_perro'],
                dueno_dict['id_dueños']
            ))
            connection.commit()
            conn.close()
            return True
    except Exception as e:
        print(f"Error al actualizar dueño: {e}")
        if 'connection' in locals() and connection:
            conn.close()
        return False

def eliminar_dueno(id_dueno):
    try:
        conn = ConeccioDB()
        connection = conn.connect()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM dueños WHERE id_dueño = ?", (id_dueno,))
            connection.commit()
            conn.close()
            return True
    except Exception as e:
        print(f"Error al eliminar dueño: {e}")
        if 'connection' in locals() and connection:
            conn.close()
        return False