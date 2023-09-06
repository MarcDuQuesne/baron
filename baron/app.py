"""
Baron Fortesque App
"""

import logging
import multiprocessing as mp
import queue as Queue  # Rename the queue module to avoid naming conflicts
from multiprocessing.queues import Queue as mpQueue

from flask import Flask, Response, render_template, request

from baron import TEMPLATES
from baron.animation import generate_frames, stream_frames
from baron.tts import generate_audio, stream_audio


class SlidingQueue(mpQueue):
    """
    A queue that removes the oldest item when full
    """

    def __init__(self, maxsize, *, ctx=mp.get_context()):
        super().__init__(maxsize, ctx=ctx)
        self.maxsize = maxsize

    def put(self, obj, block=True, timeout=None):
        """
        If the queue is full, remove the oldest item before adding a new one
        """
        if self.full():
            try:
                self.get_nowait()
            except Queue.Empty:
                pass  # The queue is already empty
        super(SlidingQueue, self).put(obj, block, timeout)

frames_queue = SlidingQueue(maxsize=2)
# text2wav = mp.Queue()
text2wav = mp.Queue()
# wav2stream = mp.Queue()
conn1, conn2 = mp.Pipe()

app = Flask(__name__, template_folder=TEMPLATES.as_posix())

logging.basicConfig(level=logging.INFO)


@app.route('/')
def index():
    """
    Returns the index page
    """
    return render_template('index.html')

@app.route('/talk', methods=['POST'])
def talk():
    """
    Puts the text in a queue and returns a 200 response
    """
    text = request.body.decode('utf-8')
    logging.info('Received text %s', text)
    text2wav.put(text)
    return 'OK'

@app.route('/audio')
def audio():
    """
    Audio stream
    """

    # return Response(generate_audio(text2wav, wav2stream), mimetype="audio/x-wav")
    return Response(stream_audio(conn2), mimetype="audio/x-wav")

@app.route('/video')
def video():
    """
    Returns a video feed
    """
    return Response(stream_frames(frames_queue), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":

    video_generator = mp.Process(target=generate_frames, args=(frames_queue, text2wav ))
    audio_generator = mp.Process(target=generate_audio, args=(text2wav, conn1))
    video_generator.start()
    audio_generator.start()
    import time
    time.sleep(1)

    app.run(host='0.0.0.0', debug=True, threaded=True)

    video_generator.join()
    audio_generator.join()
