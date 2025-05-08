import tkinter as tk
from tkinter import ttk

def configure_styles():
    """Configura los estilos para la aplicación"""
    style = ttk.Style()
    
    # Estilo general
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
    style.configure('TButton', font=('Arial', 10), padding=5)
    
    # Estilo para los Treeviews
    style.configure('Treeview', font=('Arial', 10), rowheight=25)
    style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    # Estilo para los combobox
    style.configure('TCombobox', font=('Arial', 10))
    
    # Colores
    colors = {
        'primary': '#4a6fa5',
        'secondary': '#6c757d',
        'success': '#28a745',
        'danger': '#dc3545',
        'warning': '#ffc107',
        'info': '#17a2b8'
    }
    
    return colors