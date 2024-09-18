from flask import Flask, jsonify, render_template
import psutil
import sqlite3
from datetime import datetime

app = Flask(__name__)


def get_system_metrics():
    """
    Obtiene las métricas del sistema: CPU, memoria y disco.
    """
    metrics = {}
    try:
        # CPU metrics
        metrics["cpu_percent"] = psutil.cpu_percent(interval=1)
        # Memory metrics
        memory = psutil.virtual_memory()
        metrics["memory_total"] = memory.total
        metrics["memory_available"] = memory.available
        metrics["memory_used"] = memory.used
        metrics["memory_percent"] = memory.percent
        # Disk metrics
        disk = psutil.disk_usage('/')
        metrics["disk_total"] = disk.total
        metrics["disk_used"] = disk.used
        metrics["disk_free"] = disk.free
        metrics["disk_percent"] = disk.percent
    except Exception as e:
        metrics["error"] = str(e)
    return metrics


def check_thresholds(metrics):
    """
    Revisa las métricas del sistema contra umbrales predefinidos y genera sugerencias.
    """
    suggestions = []
    if "error" in metrics:
        suggestions.append(f"Error al obtener métricas: {metrics['error']}")
        return suggestions

    if metrics["cpu_percent"] > 80:
        suggestions.append("La CPU está al límite. Considera reducir procesos o optimizar la carga de trabajo.")
    if metrics["memory_percent"] > 85:
        suggestions.append("La memoria está casi llena. Considera liberar memoria o cerrar aplicaciones no necesarias.")
    if metrics["disk_percent"] > 90:
        suggestions.append("El disco está casi lleno. Considera liberar espacio.")

    return suggestions


def save_metrics_to_db(metrics):
    """
    Guarda las métricas en la base de datos.
    """
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO metrics (timestamp, cpu_percent, memory_percent, disk_percent)
        VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), metrics["cpu_percent"], metrics["memory_percent"], metrics["disk_percent"]))
        conn.commit()
    except Exception as e:
        print(f"Error al guardar métricas en la base de datos: {e}")
    finally:
        conn.close()


@app.route("/metrics")
def metrics():
    """
    Ruta de la API que devuelve las métricas del sistema en formato JSON.
    """
    data = get_system_metrics()
    if "error" not in data:
        save_metrics_to_db(data)
    return jsonify(data)


@app.route("/suggestions")
def suggestions():
    """
    Ruta de la API que devuelve sugerencias basadas en las métricas del sistema.
    """
    metrics = get_system_metrics()
    suggestions = check_thresholds(metrics)
    return jsonify({"suggestions": suggestions})


@app.route("/")
def dashboard():
    """
    Ruta para la visualización de la interfaz web (HTML simple).
    """
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(debug=True)
