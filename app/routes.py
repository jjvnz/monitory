from flask import Blueprint, jsonify, request, render_template
from .metrics import get_system_metrics, check_thresholds, save_metrics_to_db
from .utils import get_historical_data

main = Blueprint('main', __name__)

@main.route("/metrics")
def metrics():
    data = get_system_metrics()
    if "error" not in data:
        save_metrics_to_db(data)
    return jsonify(data)

@main.route("/suggestions")
def suggestions():
    thresholds = {
        "cpu": request.args.get("cpu", default=80, type=int),
        "memory": request.args.get("memory", default=85, type=int),
        "disk": request.args.get("disk", default=90, type=int)
    }
    metrics = get_system_metrics()
    suggestions = check_thresholds(metrics, thresholds)
    return jsonify({"suggestions": suggestions})

@main.route("/historical_data")
def historical_data():
    try:
        rows = get_historical_data()
    except Exception as e:
        print(f"Error al obtener datos históricos: {e}")
        rows = []
    return jsonify(rows)

@main.route("/")
def dashboard():
    return render_template('dashboard.html')
