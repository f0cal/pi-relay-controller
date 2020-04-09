from __future__ import print_function

import RPi.GPIO as GPIO


class DigitalIn:
    def __init__(self, port):
        GPIO.setup(port, GPIO.IN)
        self._port = port

    def __bool__(self):
        return GPIO.input(self._port) == 1


class DigitalInControl:

    def __init__(self, digital_in_list):
        # Turn off GPIO warnings
        GPIO.setwarnings(False)

        # Set the GPIO numbering convention to be header pin numbers
        GPIO.setmode(GPIO.BOARD)

        self._digital_ins = {}

        # setup the ditial input ports for input
        for input in digital_in_list:
            self._digital_ins[input] = DigitalIn(input)

    def input_get_state(self, digital_in_id):
        return self._digital_ins[digital_in_id]
