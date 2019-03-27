import time

import RPi.GPIO as GPIO
from flask import Flask, request

from constants import DISPLAING_TYPE


# =============================================================================
# Flask variables
DISPLAY = DISPLAING_TYPE.CONNECTION
COMMUTATION_PER_MINUTE = 60
INITIALIZED = False

# =============================================================================
# Raspberry variables
LED_1 = 4
LED_2 = 17
LED_3 = 18


# =============================================================================
# Flask code block

app = Flask(__name__)


# -----------------------------------------------------------------------------
# HTTP controllers
@app.route('/')
def index():
    global INITIALIZED
    if not INITIALIZED:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup((LED_1, LED_2, LED_3), GPIO.OUT)
        INITIALIZED = True
        response = 'Successful initialized'
    else:
        response = 'Server is already running'
    connection_mode()
    return response


@app.route('/1')
def _1():
    timing = 60 / request.form.get('cpm', 60)
    count = request.form.get('count', 5)
    for _ in range(count):
        first_mode(timing)
    return 'OK'


@app.route('/2')
def _2():
    timing = 60 / request.form.get('cpm', 60)
    count = request.form.get('count', 5)
    for _ in range(count):
        second_mode(timing)
    return 'OK'


@app.route('/3')
def _3():
    timing = 60 / request.form.get('cpm', 60)
    count = request.form.get('count', 5)
    for _ in range(count):
        third_mode(timing)
    return 'OK'


@app.route('/normal')
def normal():
    timing = 60 / request.form.get('cpm', 60)
    count = request.form.get('count', 5)
    for _ in range(count):
        normal_mode(timing)
    return 'OK'


@app.route('/reverse')
def reverse():
    timing = 60 / request.form.get('cpm', 60)
    count = request.form.get('count', 5)
    for _ in range(count):
        reverse_mode(timing)
    return 'OK'


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


# =============================================================================
# Main code block

if __name__ == '__main__':
    app.run()
