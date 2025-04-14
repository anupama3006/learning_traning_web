from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from training_data import add_training_record, get_all_records, delete_training_record

app = Flask(__name__)
CORS(app)
# Set a secret API key (you could store this in environment variables or a database)
API_KEY = "3f9e2b7a1e8841bdb0a6a9c6a3d7e59e"

def check_api_key():
    api_key = request.headers.get("X-API-KEY")
    if api_key != API_KEY:
        return jsonify({"message": "Unauthorized"}), 401
    return None  # If API key is correct, continue processing the request

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api/trainings', methods=['POST'])
def add_training():
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    data = request.get_json()
    employer = data.get("employer")
    employee = data.get("employee")
    calendar_year = data.get("calendarYear")
    trainings = data.get("trainings", [])

    if not employer or not employee or not calendar_year or not trainings:
        return jsonify({"message": "Invalid payload"}), 400

    record = {
        "companyId": employer["companyId"],
        "inss": employee["inss"],
        "calendarYear": calendar_year,
        "trainings": trainings
    }

    add_training_record(record)
    return jsonify({"message": "Training data submitted successfully"}), 201

@app.route('/api/trainings', methods=['GET'])
def list_trainings():
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    return jsonify(get_all_records()), 200

@app.route('/api/trainings', methods=['DELETE'])
def delete_training():
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    data = request.get_json()
    company_id = data.get("companyId")
    inss = data.get("inss")
    calendar_year = data.get("calendarYear")
    training = data.get("training")

    if not company_id or not inss or not calendar_year:
        return jsonify({"message": "Missing required identifiers"}), 400

    result = delete_training_record(company_id, inss, calendar_year, training)
    status = 200 if "deleted" in result or "Removed" in result else 404
    return jsonify({"message": result}), status

if __name__ == '__main__':
    app.run(debug=True)

