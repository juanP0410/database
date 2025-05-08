import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import hashlib
import os

class RestaurantReservationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservas para Restaurantes")
        self.root.geometry("1200x800")
        
        # Configuración de la base de datos
        try:
            self.conn = sqlite3.connect('restaurante.db')
            self.cursor = self.conn.cursor()
            
            # Verificar si las tablas existen
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = self.cursor.fetchall()
            if not tables:
                self.initialize_database()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {str(e)}")
            raise
        
        # Configuración del correo electrónico
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': 'restaurante@example.com',
            'password': 'password'
        }
        
        # Autenticación
        self.current_admin = None
        self.show_login_screen()
    
    def initialize_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        try:
            # Crear tablas
            self.cursor.executescript("""
                CREATE TABLE Clientes (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo_electronico TEXT NOT NULL UNIQUE,
                    telefono TEXT,
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE Mesas (
                    id_mesa INTEGER PRIMARY KEY AUTOINCREMENT,
                    capacidad INTEGER NOT NULL,
                    estado TEXT CHECK(estado IN ('disponible', 'ocupada', 'mantenimiento')) DEFAULT 'disponible',
                    ubicacion TEXT
                );
                
                CREATE TABLE Reservas (
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
                
                CREATE TABLE Administradores (
                    id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL UNIQUE,
                    contrasena_hash TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    nivel_acceso INTEGER DEFAULT 1
                );
                
                CREATE INDEX idx_fecha_hora ON Reservas(fecha, hora);
                CREATE INDEX idx_mesa_fecha_hora ON Reservas(id_mesa, fecha, hora);
            """)
            
            # Insertar datos iniciales
            self.insert_initial_data()
            self.conn.commit()
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo inicializar la base de datos: {str(e)}")
            raise
    
    def insert_initial_data(self):
        """Inserta datos iniciales en la base de datos"""
        # Insertar mesas
        self.cursor.executemany(
            "INSERT INTO Mesas (capacidad, estado, ubicacion) VALUES (?, ?, ?)",
            [
                (2, 'disponible', 'Ventana'),
                (2, 'disponible', 'Centro'),
                (4, 'disponible', 'Ventana'),
                (4, 'disponible', 'Centro'),
                # ... (resto de mesas)
            ]
        )
        
        # Insertar administradores (contraseñas: admin123, manager456, supervisor789)
        self.cursor.executemany(
            "INSERT INTO Administradores (usuario, contrasena_hash, nombre, nivel_acceso) VALUES (?, ?, ?, ?)",
            [
                ('admin', hashlib.sha256('admin123'.encode()).hexdigest(), 'Administrador Principal', 3),
                ('manager', hashlib.sha256('manager456'.encode()).hexdigest(), 'Gerente del Restaurante', 2),
                ('supervisor', hashlib.sha256('supervisor789'.encode()).hexdigest(), 'Supervisor de Turno', 1)
            ]
        )
    
    # ... (resto de los métodos de la clase)

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantReservationSystem(root)
    root.mainloop()