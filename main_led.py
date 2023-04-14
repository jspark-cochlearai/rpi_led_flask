import os
import wave
import time
from datetime import datetime
from pixels import *
from flask import Flask, jsonify, request, Response
import numpy as np

pixels = Pixels()

app = Flask(__name__)

LED_IN_PROGRESS_FLAG = 0

@app.route('/redlight', methods=['POST'])
def redlight():
    global LED_IN_PROGRESS_FLAG
    if LED_IN_PROGRESS_FLAG == 1:
        return jsonify({"status":"200"})
    else:
        LED_IN_PROGRESS_FLAG = 1
        pixels.blink(rgb="r")
        time.sleep(3)
        pixels.wakeup()
        LED_IN_PROGRESS_FLAG = 0
        return jsonify({"status":"200"})


@app.route('/energy_filter', methods=['POST'])
def energy_filter():
    json_data = request.get_json()
    x = np.array(list(json_data))/32768.0

    energy_threshold = 2500
    validity = int(np.sum(np.abs(np.fft.fft(x))[25:100])>energy_threshold)
    return Response(str(validity), content_type='text/plain')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
