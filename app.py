from flask import Flask, render_template, request, redirect, url_for, flash
import os, json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# folders for saving files
UPLOAD_FOLDER = 'uploads'
DATA_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

DATA_FILE = os.path.join(DATA_FOLDER, 'issues.json')

# helper: load & save data
def load_issues():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_issue(issue):
    issues = load_issues()
    issues.append(issue)
    with open(DATA_FILE, 'w') as f:
        json.dump(issues, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_issue():
    issue_type = request.form.get('issue_type')
    description = request.form.get('description')
    file = request.files.get('screenshot')

    if not description.strip():
        flash("Please provide a description of the issue.", "error")
        return redirect(url_for('index'))

    filename = None
    if file and file.filename != '':
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))

    issue_data = {
        "issue_type": issue_type,
        "description": description,
        "screenshot": filename,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    save_issue(issue_data)
    flash("✅ Your issue has been saved locally!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
