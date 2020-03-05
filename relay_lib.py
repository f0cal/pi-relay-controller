"""A module for interacting with the ELEGOO 8 Channel board for the Raspberry Pi."""
# =========================================================
# Raspberry Pi Relay Board Library
#
# by John M. Wargo (www.johnwargo.com)
# https://gpiozero.readthedocs.io/en/stable/
#
# by G. Shaughnessy
# =========================================================

from __future__ import print_function

import RPi.GPIO as GPIO
import time

# Some relay boards have a default on state with a low pin
# TODO: Configure this polarity with relay configuration
ON_STATE = False
OFF_STATE = True
# Delay time between turning on next channels for `all_on` and `all_off` - for stability
DELAY_TIME = 0.2


class Relay:
    def __init__(self, port):
        GPIO.setup(port, GPIO.OUT)
        self._port = port
        self.status = OFF_STATE

    def __bool__(self):
        return self.status == ON_STATE

    def relay_on(self):
        GPIO.output(self._port, ON_STATE)
        self.status = ON_STATE
        time.sleep(DELAY_TIME)

    def relay_off(self):
        GPIO.output(self._port, OFF_STATE)
        self.status = OFF_STATE
        time.sleep(DELAY_TIME)

    def relay_toggle(self):
        new_state = not self.status
        GPIO.output(self._port, new_state)
        self.status = new_state
        time.sleep(DELAY_TIME)


class RelayControl:

    def __init__(self, relay_list):
        # Turn off GPIO warnings
        GPIO.setwarnings(False)

        # Set the GPIO numbering convention to be header pin numbers
        GPIO.setmode(GPIO.BOARD)

        self._relays = {}

        # setup the relay ports for output
        for relay in relay_list:
            # TODO: Support named keys rather than addressing by port
            self._relays[relay] = Relay(relay_list[relay])

    def relay_on(self, relay_id):
        self._relays[relay_id].relay_on()

    def relay_off(self, relay_id):
        self._relays[relay_id].relay_off()

    def relay_all_on(self):
        for relay_id in self._relays:
            self._relays[relay_id].relay_on()

    def relay_all_off(self):
        for relay_id in self._relays:
            self._relays[relay_id].relay_off()

    def relay_toggle_port(self, relay_id):
        self._relays[relay_id].relay_toggle()

    def relay_toggle_all_port(self):
        for relay_id in self._relays:
            self._relays[relay_id].relay_toggle()

    def relay_get_port_status(self, relay_id):
        return self._relays[relay_id]
