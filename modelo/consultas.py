import sqlite3
from sqlite3 import Error
from typing import List, Optional, Tuple

class Perros:
    def __init__(self, nombre: str, raza: str, edad: int, estado_salud: str, id_perro: Optional[int] = None):
        self.id_perro = id_perro
        self.nombre = nombre
        self.raza = raza
        self.edad = edad
        self.estado_salud = estado_salud

class Dueno:
    def __init__(self, nombre_apellido: str, telefono: str, fecha_adopcion: str, email: str, id_perro: int, id_dueno: Optional[int] = None):
        self.id_dueno = id_dueno
        self.nombre_apellido = nombre_apellido
        self.telefono = telefono
        self.fecha_adopcion = fecha_adopcion
        self.email = email
        self.id_perro = id_perro

def crear_conexion():
    """Crea una conexión a la base de datos SQLite."""
    try:
        conn = sqlite3.connect('perritos.db')
        conn.execute("PRAGMA foreing_keys= 1")  # Habilitar claves foráneas
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def db_connection(func):
    """Decorador para manejar conexiones a la base de datos."""
    def wrapper(*args, **kwargs):
        conn = crear_conexion()
        if not conn:
            print("No se pudo establecer la conexión con la base de datos.")
            return None
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Error as e:
            print(f"Error en la operación de la base de datos: {e}")
            return None
        finally:
            conn.close()
    return wrapper

def validar_perro(perro: Perros) -> bool:
    """Valida los datos de un objeto Perros."""
    if perro.edad < 0:
        print("La edad no puede ser negativa.")
        return False
    if not perro.nombre.strip():
        print("El nombre no puede estar vacío.")
        return False
    if not perro.raza.strip():
        print("La raza no puede estar vacía.")
        return False
    if not perro.estado_salud.strip():
        print("El estado de salud no puede estar vacío.")
        return False
    return True

def validar_dueno(dueno: Dueno) -> bool:
    """Valida los datos de un objeto Dueno."""
    if not dueno.nombre_apellido.strip():
        print("El nombre del dueño no puede estar vacío.")
        return False
    if not dueno.telefono.strip():
        print("El teléfono no puede estar vacío.")
        return False
    if not dueno.email.strip() or "@" not in dueno.email:
        print("El email es inválido.")
        return False
    return True

# Funciones para perros
@db_connection
def listar_perros(conn) -> List[Tuple[int, str, str, int, str]]:
    """Lista todos los perros de la base de datos."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_perro, nombre, raza, edad, estado_salud 
        FROM perros
        ORDER BY nombre
    """)
    return cursor.fetchall()

@db_connection
def guardar_perros(conn, perro: Perros) -> bool:
    """Guarda un nuevo perro en la base de datos."""
    if not validar_perro(perro):
        return False
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO perros (nombre, raza, edad, estado_salud)
        VALUES (?, ?, ?, ?)
    """, (perro.nombre, perro.raza, perro.edad, perro.estado_salud))
    return True

@db_connection
def actualizar_perro(conn, perro: Perros) -> bool:
    """Actualiza los datos de un perro existente."""
    if not validar_perro(perro):
        return False
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE perros 
        SET nombre = ?, raza = ?, edad = ?, estado_salud = ?
        WHERE id_perro = ?
    """, (perro.nombre, perro.raza, perro.edad, perro.estado_salud, perro.id_perro))
    return cursor.rowcount > 0

@db_connection
def eliminar_perro(conn, id_perro: int) -> bool:
    """Elimina un perro de la base de datos si no tiene dueños asociados."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM dueños WHERE id_perro = ?", (id_perro,))
    if cursor.fetchone()[0] > 0:
        print("No se puede eliminar el perro porque tiene dueños asociados.")
        return False
    cursor.execute("DELETE FROM perros WHERE id_perro = ?", (id_perro,))
    return cursor.rowcount > 0

# Funciones para dueños
@db_connection
def listar_duenos(conn) -> List[Tuple[int, str, str, str, str, int]]:
    """Lista todos los dueños de la base de datos."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_dueno, nombre_apellido, telefono, fecha_adopcion, email, id_perro
        FROM dueños
        ORDER BY nombre_apellido
    """)
    return cursor.fetchall()

@db_connection
def guardar_dueno(conn, dueno: Dueno) -> bool:
    """Guarda un nuevo dueño en la base de datos."""
    if not validar_dueno(dueno):
        return False
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dueños (nombre_apellido, telefono, fecha_adopcion, email, id_perro)
        VALUES (?, ?, ?, ?, ?)
    """, (dueno.nombre_apellido, dueno.telefono, dueno.fecha_adopcion, dueno.email, dueno.id_perro))
    return True

@db_connection
def actualizar_dueno(conn, dueno: Dueno) -> bool:
    """Actualiza los datos de un dueño existente."""
    if not validar_dueno(dueno):
        return False
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE dueños 
        SET nombre_apellido = ?, telefono = ?, fecha_adopcion = ?, email = ?, id_perro = ?
        WHERE id_dueno = ?
    """, (dueno.nombre_apellido, dueno.telefono, dueno.fecha_adopcion, dueno.email, dueno.id_perro, dueno.id_dueno))
    return cursor.rowcount > 0

@db_connection
def eliminar_dueno(conn, id_dueno: int) -> bool:
    """Elimina un dueño de la base de datos."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dueños WHERE id_dueno = ?", (id_dueno,))
    return cursor.rowcount > 0

# Crear tablas
@db_connection
def crear_tablas(conn):
    """Crea las tablas de la base de datos si no existen."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perros (
            id_perro INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            raza TEXT NOT NULL,
            edad INTEGER NOT NULL,
            estado_salud TEXT NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dueños (
            id_dueno INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            fecha_adopcion DATE NOT NULL,
            email TEXT NOT NULL,
            id_perro INTEGER NOT NULL,
            FOREIGN KEY (id_perro) REFERENCES perros(id_perro)
        );
    """)
    print("Tablas creadas exitosamente.")

# Ejecutar creación de tablas al cargar el módulo
crear_tablas()