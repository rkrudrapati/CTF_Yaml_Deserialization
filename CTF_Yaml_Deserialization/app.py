import os
import yaml
import json
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['CONVERTED_FOLDER'] = 'converted/'
app.secret_key = 'supersecretkey'

# Ensure converted directory exists
os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)

# Route to render form with text area for YAML input
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle YAML content input and conversion
@app.route('/convert', methods=['POST'])
def convert_yaml():
    yaml_content = request.form.get('yaml_content')  # Get the YAML content from the text area

    if not yaml_content:
        flash('No YAML content provided')
        return redirect(request.url)

    try:
        # Parse the YAML content
        yaml_data = yaml.load(yaml_content, Loader=yaml.Loader) # load function is unsafe and leads to deserialization
        # yaml_data = yaml.safe_load(yaml_content)  # recommended to use safe_load

        # Convert it to JSON
        json_data = json.dumps(yaml_data, indent=4)

        # Create a unique filename for the JSON file
        json_filename = 'converted_file.json'
        json_path = os.path.join(app.config['CONVERTED_FOLDER'], json_filename)

        # Save the JSON data to a file
        with open(json_path, 'w') as json_file:
            json_file.write(json_data)

        # Pass the JSON data to the template for display
        flash('YAML successfully converted to JSON')
        return render_template('result.html', json_data=json_data, filename=json_filename)

    except yaml.YAMLError as e:
        flash(f'Error parsing YAML: {e}')
        return redirect(url_for('index'))

# Route to handle JSON file download
# Not needed for CTF - can be removed
@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['CONVERTED_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    flash('File not found')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9090)
