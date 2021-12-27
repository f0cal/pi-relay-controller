# Raspberry Pi Relay Controller

from __future__ import print_function

import sys
import time
import json
import os

from flask import Flask
from flask import make_response
from flask import render_template
from flask_bootstrap import Bootstrap

from relay_lib import *
from digital_in_lib import *

error_msg = '{msg:"error"}'
success_msg = '{msg:"success"}'

# Initialize these from channels.json
RELAY_PORTS = {}

root_dir = os.environ['CONTROLLER_ROOT_DIR']

with open('{}/channels.json'.format(root_dir)) as json_file:
    channel_config = json.load(json_file)
    RELAY_PORTS = {ch['channel']: ch['pin'] for ch in channel_config['channels'] if ch['type'] == "relay"}
    DIGITAL_IN_PORTS = [ch['pin'] for ch in channel_config['channels'] if ch['type'] == "digital-in"]

RELAY_NAME = 'Generic Relay Controller'

# initialize the relay library with the system's port configuration
relay_control = RelayControl(RELAY_PORTS)
digital_in_control = DigitalInControl(DIGITAL_IN_PORTS)

app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.route('/')
def index():
    print("Loading app Main page")
    return render_template('index.html', relay_name=RELAY_NAME, channel_info=channel_config['channels'])


@app.route('/state/<int:digital_in>')
def api_get_state(digital_in):
    res = digital_in_control.input_get_state(digital_in)
    if res:
        print("State is HIGH")
        return make_response("1", 200)
    else:
        print("State is LOW")
        return make_response("0", 200)


@app.route('/status/<int:relay>')
def api_get_status(relay):
    res = relay_control.relay_get_port_status(relay)
    if res:
        print("Relay is ON")
        return make_response("1", 200)
    else:
        print("Relay is OFF")
        return make_response("0", 200)


@app.route('/toggle/<int:relay>')
def api_toggle_relay(relay):
    print("Executing api_relay_toggle:", relay)
    relay_control.relay_toggle_port(relay)
    return make_response(success_msg, 200)


@app.route('/on/<int:relay>')
def api_relay_on(relay):
    print("Executing api_relay_on:", relay)
    relay_control.relay_on(relay)
    return make_response(success_msg, 200)


@app.route('/off/<int:relay>')
def api_relay_off(relay):
    print("Executing api_relay_off:", relay)
    relay_control.relay_off(relay)
    return make_response(success_msg, 200)


@app.route('/all_toggle/')
def api_relay_all_toggle():
    print("Executing api_relay_all_toggle")
    relay_control.relay_toggle_all_port()
    return make_response(success_msg, 200)


@app.route('/all_on/')
def api_relay_all_on():
    print("Executing api_relay_all_on")
    relay_control.relay_all_on()
    return make_response(success_msg, 200)


@app.route('/all_off/')
def api_all_relay_off():
    print("Executing api_relay_all_off")
    relay_control.relay_all_off()
    return make_response(success_msg, 200)

@app.route('/reboot/<int:relay>')
def api_relay_reboot(relay, sleep_time=3):
    print("Executing api_relay_reboot:", relay)
    relay_control.relay_off(relay)
    time.sleep(sleep_time)
    relay_control.relay_on(relay)
    return make_response(success_msg, 200)


@app.errorhandler(404)
def page_not_found(e):
    print("ERROR: 404")
    return render_template('404.html', the_error=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    print("ERROR: 500")
    return render_template('500.html', the_error=e), 500


if __name__ == "__main__":
    # On the Pi, you need to run the app using this command to make sure it
    # listens for requests outside of the device.
    app.run(host='0.0.0.0', port=8080)
