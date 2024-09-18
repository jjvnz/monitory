import psutil
from datetime import datetime

def get_system_metrics():
    metrics = {}
    try:
        metrics["cpu_percent"] = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        metrics["memory_percent"] = memory.percent
        disk = psutil.disk_usage('/')
        metrics["disk_percent"] = disk.percent
    except Exception as e:
        metrics["error"] = str(e)
    return metrics

def check_thresholds(metrics, thresholds):
    suggestions = []
    if "error" in metrics:
        suggestions.append(f"Error al obtener métricas: {metrics['error']}")
        return suggestions

    if metrics["cpu_percent"] > thresholds["cpu"]:
        suggestions.append("La CPU está al límite. Considera reducir procesos o optimizar la carga de trabajo.")
    if metrics["memory_percent"] > thresholds["memory"]:
        suggestions.append("La memoria está casi llena. Considera liberar memoria o cerrar aplicaciones no necesarias.")
    if metrics["disk_percent"] > thresholds["disk"]:
        suggestions.append("El disco está casi lleno. Considera liberar espacio.")

    return suggestions

def save_metrics_to_db(metrics):
    from .models.db import get_db
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO metrics (timestamp, cpu_percent, memory_percent, disk_percent)
        VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), metrics["cpu_percent"], metrics["memory_percent"], metrics["disk_percent"]))
        conn.commit()
    except Exception as e:
        print(f"Error al guardar métricas en la base de datos: {e}")
