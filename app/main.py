from flask import Flask, render_template, jsonify, request
import os

# Set template folder explicitly to handle Render's working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping')
def ping():
    return jsonify({"message": "pong"})

# Housing upgrade endpoint (MVP example)
@app.route('/housing', methods=['GET', 'POST'])
def housing():
    if request.method == 'POST':
        # For now, just echo the received data
        data = request.json
        # Here, you'd insert into DB or process data
        return jsonify({"status": "success", "data": data})
    else:
        # Return mock housing upgrades for MVP
        sample_upgrades = [
            {"id": 1, "type": "Ventilation", "desc": "Install new windows"},
            {"id": 2, "type": "Waste Bin", "desc": "Provide new waste bins"},
        ]
        return jsonify(sample_upgrades)

# Air quality endpoint (MVP example)
@app.route('/air_quality', methods=['GET'])
def air_quality():
    # Mock data; replace with API integration later
    sample_air_quality = {
        "pm25": 62,
        "level": "Unhealthy",
        "advice": "Consider limiting outdoor activities."
    }
    return jsonify(sample_air_quality)

# Civic participation endpoint (MVP example)
@app.route('/civic', methods=['GET', 'POST'])
def civic():
    if request.method == 'POST':
        data = request.json
        # Save feedback, process, etc.
        return jsonify({"status": "success", "data": data})
    else:
        # Return mock civic feedback for MVP
        sample_feedback = [
            {"user": "Amina", "message": "Need more green spaces."},
            {"user": "Raj", "message": "Improve sanitation facilities."}
        ]
        return jsonify(sample_feedback)

if __name__ == "__main__":
    app.run(debug=True)