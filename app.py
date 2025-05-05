from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'avi', 'pdf', 'png', 'jpg', 'jpeg'}

# 폴더 경로 생성
for folder in ['music', 'video', 'score']:
    path = os.path.join(UPLOAD_FOLDER, folder)
    os.makedirs(path, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid Credentials'
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/upload/<category>', methods=['GET', 'POST'])
def upload_file(category):
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(UPLOAD_FOLDER, category, filename)
            file.save(upload_path)
            return redirect(url_for('list_files', category=category))

    return render_template('upload.html', category=category)


@app.route('/list/<category>')
def list_files(category):
    if 'username' not in session:
        return redirect(url_for('login'))

    path = os.path.join(UPLOAD_FOLDER, category)
    files = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        upload_time = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
        files.append({'name': filename, 'time': upload_time})

    return render_template('list.html', category=category, files=files)


if __name__ == '__main__':
    app.run(debug=True)
