from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('index.html', section='about')

@app.route('/skills')
def skills():
    return render_template('index.html', section='skills')

@app.route('/projects')
def projects():
    return render_template('index.html', section='projects')

@app.route('/experience')
def experience():
    return render_template('index.html', section='experience')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        return render_template('index.html', section='contact', success=True)
    return render_template('index.html', section='contact')

@app.route('/resume')
def resume():
    resume_path = os.path.join(app.root_path, 'static', 'files', 'resume.pdf')
    if os.path.exists(resume_path):
        return send_from_directory(os.path.join(app.root_path, 'static', 'files'), 'resume.pdf')
    return "Resume not found", 404

if __name__ == '__main__':
    app.run(debug=True)