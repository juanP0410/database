import sqlite3
import hashlib

def initialize_database():
    """Inicializa la base de datos con estructura y datos iniciales"""
    try:
        conn = sqlite3.connect('restaurante.db')
        cursor = conn.cursor()
        
        # Crear tablas
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS Clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo_electronico TEXT NOT NULL UNIQUE,
                telefono TEXT,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS Mesas (
                id_mesa INTEGER PRIMARY KEY AUTOINCREMENT,
                capacidad INTEGER NOT NULL,
                estado TEXT CHECK(estado IN ('disponible', 'ocupada', 'mantenimiento')) DEFAULT 'disponible',
                ubicacion TEXT
            );
            
            CREATE TABLE IF NOT EXISTS Reservas (
                id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                id_mesa INTEGER NOT NULL,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                num_personas INTEGER NOT NULL,
                estado TEXT CHECK(estado IN ('confirmada', 'cancelada', 'completada')) DEFAULT 'confirmada',
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
                FOREIGN KEY (id_mesa) REFERENCES Mesas(id_mesa)
            );
            
            CREATE TABLE IF NOT EXISTS Administradores (
                id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                contrasena_hash TEXT NOT NULL,
                nombre TEXT NOT NULL,
                nivel_acceso INTEGER DEFAULT 1
            );
            
            CREATE INDEX IF NOT EXISTS idx_fecha_hora ON Reservas(fecha, hora);
            CREATE INDEX IF NOT EXISTS idx_mesa_fecha_hora ON Reservas(id_mesa, fecha, hora);
        """)
        
        # Insertar datos iniciales
        insert_initial_data(cursor)
        
        conn.commit()
        print("Base de datos inicializada correctamente.")
        
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {str(e)}")
    finally:
        if conn:
            conn.close()

def insert_initial_data(cursor):
    """Inserta datos iniciales en la base de datos"""
    # Insertar mesas
    mesas = [
        (2, 'disponible', 'Ventana'),
        (2, 'disponible', 'Centro'),
        (4, 'disponible', 'Ventana'),
        # ... (resto de mesas)
    ]
    cursor.executemany("INSERT INTO Mesas (capacidad, estado, ubicacion) VALUES (?, ?, ?)", mesas)
    
    # Insertar administradores
    administradores = [
        ('admin', hashlib.sha256('admin123'.encode()).hexdigest(), 'Administrador Principal', 3),
        ('manager', hashlib.sha256('manager456'.encode()).hexdigest(), 'Gerente del Restaurante', 2),
        ('supervisor', hashlib.sha256('supervisor789'.encode()).hexdigest(), 'Supervisor de Turno', 1)
    ]
    cursor.executemany(
        "INSERT INTO Administradores (usuario, contrasena_hash, nombre, nivel_acceso) VALUES (?, ?, ?, ?)",
        administradores
    )

if __name__ == "__main__":
    initialize_database()