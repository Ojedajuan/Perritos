import sqlite3
from sqlite3 import Error
from typing import List,Tuple, Optional
from modelo.conecciodb import ConeccioDB



class Perros:
    def __init__(self, nombre: str, color: str,estado: str, fecha_ingreso: str =None , id_perro: Optional[int] = None):
        self.id_perro = id_perro
        self.nombre = nombre
        self.color = color
        self.estado = estado 
        self.fecha_ingreso = fecha_ingreso

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
        conn.execute("PRAGMA foreign_keys= 1")  # Habilitar claves foráneas
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def db_connection(func):
    """Decorador que maneja la conexión a la base de datos."""
    def wrapper(*args, **kwargs):
        conn = ConeccioDB().connect()
        if not conn:
            print("❌ No se pudo conectar a la base de datos.")
            return []
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except sqlite3.Error as e:
            print(f"❌ Error en la base de datos: {e}")
            return []	
        finally:
            conn.close()
    return wrapper

def validar_perro(perro: Perros) -> bool:
    """Valida los datos de un objeto Perros."""
    if not perro.nombre.strip():
        print("El nombre no puede estar vacío.")
        return False
    if not perro.estado.strip():
        print("El estado no puede estar vacío.")
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
def listar_perros(conn) -> List[Tuple]:
    """Lista todos los perros de la base de datos."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_perro,color, nombre, estado, fecha_ingreso
        FROM perros
        ORDER BY nombre
    """)
    return cursor.fetchall()

@db_connection
def guardar_perros(conn, perro: Perros = None, nombre: str = None, color: str = "Desconocido", estado: str = "Disponible", fecha_ingreso: str = "2024-01-01")-> bool:
    """Guarda un perro en la base de datos, permitiendo recibir un objeto Perros o valores individuales."""
    
    # Si se pasa un objeto Perros, extraer los valores
    if perro:
        nombre = perro.nombre
        color = perro.color
        estado = perro.estado
        fecha_ingreso = perro.fecha_ingreso if perro.fecha_ingreso else "2024-01-01"

    # Definir estados válidos
    estados_validos = {"Disponible", "Adoptado", "No adoptado"}

    # Normalización de entradas
    # No aplicar strip() a id_perro ya que es un entero
    nombre = nombre.strip() if nombre else ""
    color = color.strip().capitalize() if color else "Desconocido"
    estado = estado.strip().capitalize() if estado else "Disponible"
    fecha_ingreso = fecha_ingreso.strip() if fecha_ingreso else "2024-01-01"

    # Corrección de estados
    if estado == "No Adoptado":
        estado = "No adoptado"

    # Validar estado
    if estado not in estados_validos:
        print(f"❌ Error: '{estado}' no es un estado válido. Estados permitidos: {estados_validos}")
        return False  
    if not nombre:
        print("❌ Error: El nombre no puede estar vacío")
        return False
    # Ejecutar la inserción
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Perros (NOMBRE, COLOR, ESTADO, FECHA_INGRESO) 
        VALUES (?, ?, ?, ?)
    """, (nombre, color, estado, fecha_ingreso))

    print("✅ Perro guardado correctamente.")
    return True


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
def crear_tablas():
    """Crea las tablas en la base de datos."""
    try:
        conn = ConeccioDB()
        connection = conn.connect()

        if connection:
            cursor = connection.cursor()

            cursor.executescript("""
                DROP TABLE IF EXISTS Dueños;
                DROP TABLE IF EXISTS Perros;
            """)

            sql_script = """
            CREATE TABLE IF NOT EXISTS DUEÑOS (
                ID_DUEÑO INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE_APELLIDO TEXT NOT NULL,
                TELEFONO TEXT NOT NULL,
                FECHA_ADOPCION TEXT NOT NULL,
                EMAIL TEXT NOT NULL,
                ID_PERRO INTEGER,
                FOREIGN KEY (ID_PERRO) REFERENCES PERROS (ID_PERRO)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS PERROS (
                ID_PERRO INTEGER PRIMARY KEY AUTOINCREMENT,
                FECHA_INGRESO TEXT NOT NULL,
                COLOR TEXT NOT NULL,
                ESTADO TEXT NOT NULL DEFAULT 'Disponible' 
                    CHECK (ESTADO IN ('Adoptado', 'No adoptado', 'Disponible')),
                NOMBRE TEXT NOT NULL
            );
            """

            cursor.executescript(sql_script)  # Permite ejecutar varias sentencias SQL
            connection.commit()
            print("✅ Tablas creadas correctamente")
            conn.close()
            return True

    except Exception as e:
        print(f"❌ Error creando las tablas: {e}")
        return False
