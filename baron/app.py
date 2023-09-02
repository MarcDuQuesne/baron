"""
Baron Fortesque App
"""

import logging

from flask import Flask, Response, request

from baron.animation import stream_frames, handle_text
from baron.matching import get_phonemes

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    """
    Returns the index page
    """
    return "Hello, World!"

@app.route('/talk', methods=['POST'])
def talk():
    """
    Puts the text in a queue and returns a 200 response
    """
    text = request.body.decode('utf-8')
    logging.info('Received text %s', text)
    phonemes = get_phonemes(text)

    return 'OK'

@app.route('/video')
def video_feed():
    """
    Returns a video feed
    """
    return Response(stream_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":

    app.run(debug=True, threaded = True, port=5000)
