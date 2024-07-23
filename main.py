from flask import Flask, request, jsonify
import requests
import json
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

BREVO_API_KEY = os.getenv('BREVO_API_KEY')

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    if not data or 'email' not in data or 'name' not in data:
        return jsonify({"error": "Email and name are required"}), 400

    email = data['email'] 
    name = data['name']

    payload = {
        "sender": {
            "name": name,
            "email": email
        },
        "to": [
            {
                "email": 'k.ashrf911@gmail.com',
                "name": 'Karim'
            }
        ],
        "subject": "Hello world",
        "htmlContent": """
        <html>
        <head></head>
        <body>
            <p>Hello {name},</p>
            <p>This is my first transactional email sent from Brevo.</p>
            <p>If you wish to unsubscribe, please click <a href="http://example.com/unsubscribe?email={email}">here</a>.</p>
        </body>
        </html>
        """.format(name=name, email=email)
    }

    headers = {
        'accept': 'application/json',
        'api-key': BREVO_API_KEY,
        'content-type': 'application/json'
    }

    response = requests.post('https://api.brevo.com/v3/smtp/email', headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        return jsonify({"message": "Email sent successfully"}), 201
    else:
        return jsonify({"error": "Failed to send email", "details": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
