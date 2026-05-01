from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
MY_WHATSAPP_NUMBER = os.environ.get('MY_WHATSAPP_NUMBER')

def send_whatsapp_message(name, email, message):
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, MY_WHATSAPP_NUMBER]):
        print("WhatsApp not configured - missing credentials")
        return False
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        body = f"New Contact from Portfolio:\n\nName: {name}\nEmail: {email}\nMessage: {message}"
        message = client.messages.create(
            from_=f'whatsapp:{TWILIO_PHONE_NUMBER}',
            body=body,
            to=f'whatsapp:{MY_WHATSAPP_NUMBER}'
        )
        return True
    except Exception as e:
        print(f"Error sending WhatsApp: {e}")
        return False

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
        
        send_whatsapp_message(name, email, message)
        
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