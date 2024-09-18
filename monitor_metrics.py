from flask import Flask, jsonify, render_template, request
import psutil
import sqlite3
from datetime import datetime

app = Flask(__name__)

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
    try:
        with sqlite3.connect('metrics.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO metrics (timestamp, cpu_percent, memory_percent, disk_percent)
            VALUES (?, ?, ?, ?)
            ''', (datetime.now().isoformat(), metrics["cpu_percent"], metrics["memory_percent"], metrics["disk_percent"]))
            conn.commit()
    except Exception as e:
        print(f"Error al guardar métricas en la base de datos: {e}")

@app.route("/metrics")
def metrics():
    data = get_system_metrics()
    if "error" not in data:
        save_metrics_to_db(data)
    return jsonify(data)

@app.route("/suggestions")
def suggestions():
    thresholds = {
        "cpu": request.args.get("cpu", default=80, type=int),
        "memory": request.args.get("memory", default=85, type=int),
        "disk": request.args.get("disk", default=90, type=int)
    }

    # Validar umbrales
    if not (0 <= thresholds["cpu"] <= 100):
        thresholds["cpu"] = 80
    if not (0 <= thresholds["memory"] <= 100):
        thresholds["memory"] = 85
    if not (0 <= thresholds["disk"] <= 100):
        thresholds["disk"] = 90

    metrics = get_system_metrics()
    suggestions = check_thresholds(metrics, thresholds)
    return jsonify({"suggestions": suggestions})

@app.route("/historical_data")
def historical_data():
    try:
        with sqlite3.connect('metrics.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT timestamp, cpu_percent, memory_percent, disk_percent FROM metrics
            ORDER BY timestamp DESC
            ''')
            rows = cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener datos históricos: {e}")
        rows = []
    return jsonify(rows)

@app.route("/")
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
