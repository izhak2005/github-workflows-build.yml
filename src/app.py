from flask import Flask, render_template, jsonify, request, session
import json
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # שנה למפתח אקראי אמיתי

# הגדרות אימייל
GMAIL_USER = "your-email@gmail.com"  # שנה לאימייל שלך
GMAIL_PASSWORD = "your-app-password"  # סיסמת אפליקציה מגוגל

def load_users():
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    users = load_users()
    user = next((u for u in users if u['username'] == data['username'] and 
                 u['password'] == data['password']), None)
    
    if user:
        if not user['is_approved']:
            return jsonify({'success': False, 'message': 'המשתמש עדיין לא אושר'})
        
        if not user['paid'] and user['login_count'] >= 7:
            return jsonify({'success': False, 'message': 'נגמרו הכניסות החינמיות'})
        
        user['login_count'] = user.get('login_count', 0) + 1
        save_users(users)
        session['username'] = user['username']
        
        return jsonify({
            'success': True,
            'is_admin': user.get('is_admin', False),
            'logins_left': 7 - user['login_count'] if not user['paid'] else None
        })
    
    return jsonify({'success': False, 'message': 'שם משתמש או סיסמה שגויים'})

if __name__ == '__main__':
    app.run(debug=True)
