import os
import wave
#import RPi.GPIO as GPIO
import time
from datetime import datetime
from pixels import *
from flask import Flask, jsonify, request

#BUTTON = 17
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(BUTTON, GPIO.IN)

pixels = Pixels()

app = Flask(__name__)


@app.route('/redlight', methods=['POST'])
def redlight():
    pixels.blink(rgb="r")
    time.sleep(3)
    pixels.wakeup()
    return jsonify({"status":"200"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)

