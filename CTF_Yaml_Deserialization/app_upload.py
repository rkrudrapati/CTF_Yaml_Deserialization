import os
import yaml
import json
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['CONVERTED_FOLDER'] = 'converted/'
app.secret_key = 'supersecretkey'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)

# Allowed file extension for upload
ALLOWED_EXTENSIONS = {'yaml', 'yml'}

# Check if the uploaded file is a YAML file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to render upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and conversion
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Convert the YAML to JSON
        try:
            with open(file_path, 'r') as yaml_file:
                yaml_data = yaml.safe_load(yaml_file)
                json_data = json.dumps(yaml_data, indent=4)

                json_filename = filename.rsplit('.', 1)[0] + '.json'
                json_path = os.path.join(app.config['CONVERTED_FOLDER'], json_filename)

                # Save the converted JSON to a file
                with open(json_path, 'w') as json_file:
                    json_file.write(json_data)

                # Pass the JSON data to the template for display
                flash('File successfully uploaded and converted')
                return render_template('result.html', json_data=json_data, filename=json_filename)

        except yaml.YAMLError as e:
            flash(f'Error parsing YAML: {e}')
            return redirect(request.url)

    flash('Allowed file type is YAML')
    return redirect(request.url)

# Route to handle JSON file download
@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['CONVERTED_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    flash('File not found')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8070)