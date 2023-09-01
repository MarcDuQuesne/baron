"""
Baron Fortesque App
"""

import logging

from flask import Flask, Response, render_template, request
from baron.animation import gen_frames

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
    return 'OK'

@app.route('/video_feed')
def video_feed():
    """
    Returns a video feed
    """
    Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)