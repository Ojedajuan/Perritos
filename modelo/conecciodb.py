import sqlite3
import os
from typing import Optional, Generator
from contextlib import contextmanager

class ConeccioDB:
    """A class to manage SQLite database connections with safety features and context management."""
    
    def __init__(self, db_name: str = 'dogs_database.db', data_dir: str = 'data'):
        """
        Initialize database connection manager.
        
        Args:
            db_name (str): Name of the database file
            data_dir (str): Directory where the database file will be stored
        """
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = data_dir
        self.db_path = os.path.join(self.base_dir, self.data_dir, db_name)
        self.connection: Optional[sqlite3.Connection] = None
        
    def connect(self) -> Optional[sqlite3.Connection]:
        """
        Establish a connection to the SQLite database.
        
        Returns:
            Optional[sqlite3.Connection]: Database connection object if successful, None otherwise
        """
        try:
            # Ensure the data directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # Create and configure connection
            self.connection = sqlite3.connect(self.db_path)
            self.connection.execute("PRAGMA foreign_keys = ON;")
            
            # Set row factory to use dictionary cursor
            self.connection.row_factory = sqlite3.Row
            
            return self.connection
            
        except sqlite3.Error as e:
            print(f"SQLite error occurred: {e}")
            return None
        except OSError as e:
            print(f"OS error occurred: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            return None
    
    def close(self) -> None:
        """Safely close the database connection."""
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
        except Exception as e:
            print(f"Error closing database connection: {e}")
    
    @contextmanager
    def get_connection(self) -> Generator[Optional[sqlite3.Connection], None, None]:
        """
        Context manager for database connections.
        
        Yields:
            Optional[sqlite3.Connection]: Database connection object
        
        Usage:
            with db.get_connection() as conn:
                # Use the connection here
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM table")
        """
        try:
            conn = self.connect()
            yield conn
        finally:
            self.close()
    
    @property
    def is_connected(self) -> bool:
        """Check if there is an active database connection."""
        return self.connection is not None
    
    def execute_query(self, query: str, parameters: tuple = ()) -> Optional[sqlite3.Cursor]:
        """
        Execute a SQL query safely.
        
        Args:
            query (str): SQL query to execute
            parameters (tuple): Query parameters to prevent SQL injection
            
        Returns:
            Optional[sqlite3.Cursor]: Cursor object if successful, None otherwise
        """
        try:
            if not self.connection:
                self.connect()
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute(query, parameters)
                return cursor
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

# consultas.py
from modelo.conecciodb import ConeccioDB

def crear_tablas():
    try:
        conn = ConeccioDB()
        connection = conn.connect()
        
        if connection:
            cursor = connection.cursor()
            
            # Create tables
            sql = """
            CREATE TABLE IF NOT EXISTS perros
              (
                id_perro INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                fecha_ingreso DATE NOT NULL,
                color TEXT NOT NULL,
                ESTADO TEXT NOT NULL DEFAULT 'Disponible' 
                CHECK (Estado IN ('Adoptado', 'No adoptado', 'No adoptable')),
            );

            CREATE TABLE IF NOT EXISTS dueños (
                id_dueño INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_apellido TEXT NOT NULL,
                dni TEXT,
                telefono TEXT NOT NULL,
                fecha_adopcion DATE NOT NULL,
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
                dueno_dict['id_dueño']
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