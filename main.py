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
    phone = data['phone']
    looking = data['looking_for']
    service_selector = data['service_selector']
    custom_service = data['custom_service']
    industry = data['industry']
    custom_industry = data['custom_industry']
    number_of_employees = data['number_of_employees']
    message = data['message']
    pageSource = data['pageSource']

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
        "subject": "Email from EchoMinds",
        "htmlContent": """
        <html>
        <head></head>
        <body>
            <p>Name : {name},</p>
            <p>Email : {email},</p>
            <p>Phone : {phone},</p>
            <p>Looking For : {looking},</p>
            <p>Selected Service : {service_selector},</p>
            <p>Custom Service  : {custom_service},</p>
            <p>Industry : {industry},</p>
            <p>Custom Industry : {custom_industry},</p>
            <p>Number of employees : {number_of_employees},</p>
            <p>Message : {message},</p>
            <p>Source Page : {pageSource},</p>
        </body>
        </html>
        """.format(name=name, email=email,phone=phone,looking=looking,service_selector=service_selector,custom_service=custom_service,industry=industry,custom_industry=custom_industry
                   ,number_of_employees=number_of_employees,message=message)
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
