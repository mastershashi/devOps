from flask import Flask, render_template, request, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os, datetime

app = Flask(__name__)
BASE_DIR = os.path.dirname(__file__)

app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['REPORT_FOLDER'] = os.path.join(BASE_DIR, 'reports')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Patient fields
    patient = {
        'id': request.form.get('id', ''),  # NEW: Patient ID field
        'name': request.form.get('name', ''),
        'age': request.form.get('age', ''),
        'sex': request.form.get('sex', ''),
        'weight': request.form.get('weight', ''),
        'address': request.form.get('address', ''),
        'mobile': request.form.get('mobile', ''),
        'diagnosis': request.form.get('diagnosis', ''),      # NEW: Diagnosis
        'findings': request.form.get('findings', ''),        # NEW: Findings
        'prescription': request.form.get('prescription', ''),# NEW: Prescription Given
        'notes': request.form.get('notes', ''),              # Keep old notes for compatibility
        'date': request.form.get('date') or datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    }

    # Save uploaded images
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    img_paths = []
    for key in request.files:
        f = request.files[key]
        if f and allowed(f.filename):
            fname = datetime.datetime.now().strftime('%Y%m%d%H%M%S_') + secure_filename(f.filename)
            out_path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            f.save(out_path)
            img_paths.append(('uploads', fname))

    # Include optional sample images
    for key in request.form:
        if key.startswith('sample_') and request.form.get(key) == 'on':
            img_paths.append(('static', key.replace('sample_', '')))

    # Render HTML report
    os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)
    slug = (patient['name'] or 'patient').replace(' ', '_')
    report_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{slug}.html"
    report_path = os.path.join(app.config['REPORT_FOLDER'], report_name)

    html = render_template('report.html', patient=patient, images=img_paths)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return jsonify({"report_url": url_for('report', filename=report_name)})

@app.route('/reports/<path:filename>')
def report(filename):
    return send_from_directory(app.config['REPORT_FOLDER'], filename, as_attachment=False)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=7860, debug=True)
