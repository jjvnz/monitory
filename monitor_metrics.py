from flask import Flask, jsonify, render_template
import psutil

app = Flask(__name__)

# Función para obtener las métricas del sistema
def get_system_metrics():
    metrics = {}
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
    return metrics

# Ruta para la API de métricas
@app.route("/metrics")
def metrics():
    data = get_system_metrics()
    return jsonify(data)

# Función para sugerencias basadas en umbrales
def check_thresholds(metrics):
    suggestions = []
    if metrics["cpu_percent"] > 80:
        suggestions.append("La CPU está al límite. Considera reducir procesos o optimizar la carga de trabajo.")
    if metrics["memory_percent"] > 85:
        suggestions.append("La memoria está casi llena. Considera liberar memoria o cerrar aplicaciones no necesarias.")
    if metrics["disk_percent"] > 90:
        suggestions.append("El disco está casi lleno. Considera liberar espacio.")
    return suggestions

# Nueva ruta para sugerencias
@app.route("/suggestions")
def suggestions():
    metrics = get_system_metrics()
    suggestions = check_thresholds(metrics)
    return jsonify({"suggestions": suggestions})

# Ruta para la visualización (HTML simple)
@app.route("/")
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
