import time
import threading

import RPi.GPIO as GPIO
from flask import Flask
from flask_restful import Resource, Api, reqparse

from constants import DISPLAING_TYPE


# =============================================================================
# Flask variables
DISPLAY = DISPLAING_TYPE.CONNECTION
COMMUTATION_PER_MINUTE = 60
CONNECTED_DEVICE = None

# =============================================================================
# Raspberry variables
LED_1 = 4
LED_2 = 17
LED_3 = 18


# =============================================================================
# Flask code block

app = Flask(__name__)
api = Api(app)


# -----------------------------------------------------------------------------
# API Controllers

class Connect(Resource):
    def get(self):
        global CONNECTED_DEVICE, DISPLAY
        parser = reqparse.RequestParser()
        parser.add_argument('device', required=True)
        args = parser.parse_args()
        if CONNECTED_DEVICE is None:
            CONNECTED_DEVICE = args['device']
            DISPLAY = DISPLAING_TYPE.NORMAL
            return {'status': 'CONNECTED'}
        else:
            return {'status': 'FAIL'}


class Disconnect(Resource):
    def post(self):
        global CONNECTED_DEVICE, COMMUTATION_PER_MINUTE, DISPLAY
        parser = reqparse.RequestParser()
        parser.add_argument('device', required=True)
        args = parser.parse_args()
        if args.get('device'):
            CONNECTED_DEVICE = None
            DISPLAY = DISPLAING_TYPE.CONNECTION
            COMMUTATION_PER_MINUTE = 60


# -----------------------------------------------------------------------------
# Routing

api.add_resource(Connect, '/connect')
api.add_resource(Disconnect, '/disconnect')


# =============================================================================
# Raspberry Pi Code block

def connection_mode():
    for _ in range(3):
        time.sleep(0.5)
        GPIO.output(LED_1, True)
        GPIO.output(LED_2, True)
        GPIO.output(LED_3, True)
        time.sleep(0.5)
        GPIO.output(LED_1, False)
        GPIO.output(LED_2, False)
        GPIO.output(LED_3, False)
    time.sleep(2)


def first_mode(timing):
    time.sleep(timing)
    GPIO.output(LED_1, True)
    time.sleep(timing)
    GPIO.output(LED_1, False)


def second_mode(timing):
    time.sleep(timing)
    GPIO.output(LED_2, True)
    time.sleep(timing)
    GPIO.output(LED_2, False)


def third_mode(timing):
    time.sleep(timing)
    GPIO.output(LED_3, True)
    time.sleep(timing)
    GPIO.output(LED_3, False)


def normal_mode(timing):
    time.sleep(timing)
    GPIO.output(LED_3, False)
    GPIO.output(LED_1, True)
    time.sleep(timing)
    GPIO.output(LED_1, False)
    GPIO.output(LED_2, True)
    time.sleep(timing)
    GPIO.output(LED_2, False)
    GPIO.output(LED_3, True)


def reverse_mode(timing):
    time.sleep(timing)
    GPIO.output(LED_1, False)
    GPIO.output(LED_3, True)
    time.sleep(timing)
    GPIO.output(LED_3, False)
    GPIO.output(LED_2, True)
    time.sleep(timing)
    GPIO.output(LED_2, False)
    GPIO.output(LED_1, True)


def rasp_main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup((LED_1, LED_2, LED_3), GPIO.OUT)
    while True:
        global COMMUTATION_PER_MINUTE, DISPLAY
        timing = 60.0 / COMMUTATION_PER_MINUTE
        if DISPLAY == DISPLAING_TYPE.CONNECTION:
            connection_mode()
        elif DISPLAY == DISPLAING_TYPE.LED_1:
            first_mode(timing)
        elif DISPLAY == DISPLAING_TYPE.LED_2:
            second_mode(timing)
        elif DISPLAY == DISPLAING_TYPE.LED_3:
            third_mode(timing)
        elif DISPLAY == DISPLAING_TYPE.NORMAL:
            normal_mode(timing)
        elif DISPLAY == DISPLAING_TYPE.REVERSE:
            reverse_mode(timing)


# =============================================================================
# Main code block

if __name__ == '__main__':
    threads = [
        threading.Thread(target=rasp_main()),
        threading.Thread(target=app.run,
                         kwargs={'host': '0.0.0.0', 'port': 5000}),
    ]
    for thread in threads:
        thread.start()
