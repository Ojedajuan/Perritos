from .conecciodb import ConeccioDB

# Función para crear tablas
def crear_tabla():
    conn = ConeccioDB()
    cursor = conn.cursor

    sql = '''
    CREATE TABLE IF NOT EXISTS Perros ( 
        ID_Perros INTEGER PRIMARY KEY AUTOINCREMENT,
        FECHA_INGRESO TEXT NOT NULL,
        COLOR TEXT NOT NULL,
        NOMBRE TEXT (100) NOT NULL,
        ESTADO TEXT DEFAULT 'disponible' CHECK (ESTADO IN ('disponible', 'adoptado', 'no adoptado', 'no adoptable'))
    );

    CREATE TABLE IF NOT EXISTS DUEÑOS (
        ID_DUEÑOS INTEGER PRIMARY KEY AUTOINCREMENT,
        FECHA_ADOPCION TEXT,
        NOMBRE_APELLIDO TEXT NOT NULL,
        EMAIL TEXT NOT NULL,
        DNI TEXT,
        ID_PERRO INTEGER,
        FOREIGN KEY (ID_PERRO) REFERENCES Perros (ID_Perros)
    );

    CREATE TABLE IF NOT EXISTS USUARIO ( 
        ID_USUARIO INTEGER PRIMARY KEY AUTOINCREMENT,
        DNI VARCHAR (30),
        NOMBRE_APELLIDO VARCHAR (150) NOT NULL,
        EMAIL TEXT NOT NULL,
        ID_DUEÑO INTEGER,
        FOREIGN KEY (ID_DUEÑO) REFERENCES DUEÑOS (ID_DUEÑOS)
    );
    '''
    try:
        cursor.executescript(sql)
        conn.commit()
    except Exception as e:
        print(f"Error al crear las tablas: {e}")
    finally:
        conn.cerrar_con()

# Clase para representar a los perros
class Perros:
    def __init__(self, fecha_ingreso, nombre, estado, color):
        self.color=color
        self.id_perros = None
        self.fecha_ingreso = fecha_ingreso
        self.nombre = nombre
        self.estado = estado;"disponible";"adoptado";"no adoptado";

    def __str__(self):
        return f'Perros[{self.fecha_ingreso}, {self.color}, {self.estado}, {self.nombre}]'

# Clase para representar a los dueños
class Dueños:
    def __init__(self, email, dni, nombre_apellido, fecha_adopcion, id_perro):
        self.id_dueños = None
        self.id_perro = id_perro
        self.fecha_adopcion = fecha_adopcion
        self.dni = dni
        self.email = email
        self.nombre_apellido = nombre_apellido

    def __str__(self):
        return f'Dueños[{self.fecha_adopcion}, {self.dni}, {self.nombre_apellido}]'

# Clase para representar a los usuarios
class Usuario:
    def __init__(self, email, dni, nombre_apellido):
        self.id_usuario = None
        self.dni = dni
        self.email = email
        self.nombre_apellido = nombre_apellido

    def __str__(self):
        return f'Usuario[{self.dni}, {self.email}, {self.nombre_apellido}]'

# Función para guardar un perro
def guardar_perros(perro):
    conn = ConeccioDB()
    sql = """
        INSERT INTO Perros (FECHA_INGRESO, COLOR, ESTADO, NOMBRE) 
        VALUES (?, ?, ?, ?)
    """
    try:
        conn.cursor.execute(sql, (
            perro.FECHA_INGRESO, 
            perro.COLOR, 
            perro.ESTADO, 
            perro.NOMBRE
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al guardar perro: {e}")
        return False
    finally:
        conn.cerrar_con()

# Función para guardar un dueño
def guardar_dueños(dueño):
    conn = ConeccioDB()
    sql = """
        INSERT INTO DUEÑOS (FECHA_ADOPCION, DNI, NOMBRE_APELLIDO, EMAIL, ID_PERRO)
        VALUES ('{DUEÑOS.fecha_Adopcion}' ,'{DUEÑOS.dni}',' {DUEÑOS.nombre_apellido}','{DUEÑOS.email}');
    """
    try:
        conn.cursor.execute(sql, (dueño.fecha_adopcion, dueño.dni, dueño.nombre_apellido, dueño.email, dueño.id_perro))
        conn.commit()
    except Exception as e:
        print(f"Error al guardar dueño: {e}")
    finally:
        conn.cerrar_con()

# Función para listar todos los perros
def listar_perros():
    conn = ConeccioDB()
    sql = """
        SELECT ID_Perros, FECHA_INGRESO, COLOR, ESTADO, NOMBRE 
        FROM Perros;
    """
    try:
        conn.cursor.execute(sql)
        perros = conn.cursor.fetchall()
        for perro in perros:
            print(perro)
        return perros
    except Exception as e:
        print(f"Error al listar perros: {e}")
        return []
    finally:
        conn.cerrar_con()

# Función para listar todos los dueños
def listar_dueños():
    conn = ConeccioDB()
    sql = """
        SELECT * FROM DUEÑOS;
    """
    try:
        conn.cursor.execute(sql)
        return conn.cursor.fetchall()
    except Exception as e:
        print(f"Error al listar dueños: {e}")
        return []
    finally:
        conn.cerrar_con()

# Función para editar un perro
def update_perro(perro):
    conn = ConeccioDB()
    sql = """
        UPDATE Perros
        SET 
            NOMBRE = ?,
            FECHA_INGRESO = ?,
            COLOR = ?,
            ESTADO = ?
        WHERE ID_Perros = ?;
    """
    try:
        conn.cursor.execute(sql, (
            perro.NOMBRE, 
            perro.FECHA_INGRESO, 
            perro.COLOR, 
            perro.ESTADO, 
            perro.ID_perros
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al editar perro: {e}")
        return False
    finally:
        conn.cerrar_con()

# Función para eliminar un perro
def eliminar_perros(id_perro):
    conn = ConeccioDB()
    sql = """
        DELETE FROM Perros
        WHERE ID_Perros = ?;
    """
    try:
        conn.cursor.execute(sql, (id_perro,))
        conn.commit()
    except Exception as e:
        print(f"Error al eliminar perro: {e}")
    finally:
        conn.cerrar_con()

