from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import url_for

from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')


# Route for Click to Call demo page.
@app.route('/')
def index():
    return render_template('index.html',
                           configuration_error=None)


# Voice Request URL
@app.route('/call', methods=['POST'])
def call():
    # Get phone number we need to call
    phone_number = request.form.get('phoneNumber', None)

    try:
        twilio_client = Client(app.config['TWILIO_ACCOUNT_SID'],
                               app.config['TWILIO_AUTH_TOKEN'])
    except Exception as e:
        msg = 'Missing configuration variable: {0}'.format(e)
        return jsonify({'error': msg})

    try:
        twilio_client.calls.create(from_=app.config['TWILIO_CALLER_ID'],
                                   to=phone_number,
                                   url=url_for('.outbound',
                                               _external=True))
    except Exception as e:
        app.logger.error(e)
        return jsonify({'error': str(e)})

    return jsonify({'message': 'Call incoming!'})


@app.route('/outbound', methods=['POST'])
def outbound():
    response = VoiceResponse()

    response.say('Now connecting you to LEGO consumer service. An agent will be there shortly',
                 voice='Polly.Amy',language='en-GB')
    response.dial('+4588915109')
    return str(response)


# Route for Landing Page after Heroku deploy.
@app.route('/landing.html')
def landing():
    return render_template('landing.html',
                           configuration_error=None)
