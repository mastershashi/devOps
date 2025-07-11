from flask import Flask, request, jsonify
import logging
import json
import os

app = Flask(__name__)
# Setup logger to write JSON logs
log_file = "/app/logs/flask.log"
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logger = logging.getLogger('flask_app')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_file)
handler.setFormatter(logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'))
logger.addHandler(handler)

# In-memory storage for patient records
patients = {}
patient_id_counter = 1

@app.route('/patients', methods=['POST'])
def create_patient():
    global patient_id_counter
    data = request.get_json()

    if not data or 'name' not in data or 'age' not in data:
        logger.warning("Missing name or age in request.")
        return jsonify({'error': 'Name and age are required'}), 400

    patient_id = patient_id_counter
    patients[patient_id] = {
        'id': patient_id,
        'name': data['name'],
        'age': data['age'],
        'conditions': data.get('conditions', [])
    }
    patient_id_counter += 1

    logger.info(f"Created patient {patient_id}")
    return jsonify(patients[patient_id]), 201

@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = patients.get(patient_id)
    if not patient:
        logger.error(f"Patient {patient_id} not found")
        return jsonify({'error': 'Patient not found'}), 404
    
    logger.info(f"Retrieved patient {patient_id}")
    return jsonify(patient), 200

@app.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.get_json()
    patient = patients.get(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    # Update patient fields if present
    patient['name'] = data.get('name', patient['name'])
    patient['age'] = data.get('age', patient['age'])
    patient['conditions'] = data.get('conditions', patient['conditions'])

    return jsonify(patient), 200

@app.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    if patient_id not in patients:
        return jsonify({'error': 'Patient not found'}), 404

    del patients[patient_id]
    return jsonify({'message': f'Patient {patient_id} deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
