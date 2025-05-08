from datetime import datetime, timedelta
import re

def validate_email(email):
    """Valida que un email tenga formato correcto"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Valida que un número de teléfono tenga formato correcto"""
    if not phone:  # El teléfono es opcional
        return True
    pattern = r'^[\d\s+-]+$'
    return re.match(pattern, phone) is not None

def generate_time_slots():
    """Genera slots de tiempo cada 30 minutos desde las 11:00 hasta las 22:00"""
    return [f"{hour:02d}:{minute:02d}" for hour in range(11, 22) for minute in [0, 30]]

def format_datetime_for_display(datetime_str):
    """Formatea una fecha/hora para mostrarla al usuario"""
    try:
        dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%d/%m/%Y %H:%M')
    except ValueError:
        return datetime_str