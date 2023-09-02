"""
Rules for creating animations.
"""

from random import choice, random
from time import sleep
from typing import Generator

import cv2
import numpy as np
from glitch_this import ImageGlitcher
from PIL import Image

from baron import IMAGES


def cv2_to_image(img: np.ndarray) -> Image:
    """
    Convert a cv2 image to a PIL image.
    """
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def image_to_cv2(img: Image) -> np.ndarray:
    """
    Convert a PIL image to a cv2 image.
    """
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

class Animation:
    """
    Stores the animation algorithms.
    """
    fade_images = [cv2.imread((IMAGES / "fade" / f"{i:03d}.png").as_posix()) for i in range(23)]
    fade_index = -1

    features = {
            'top': [cv2.imread((IMAGES / "features" / 'top' / f"{i}.png").as_posix()) for i in range(5)],
            'bottom' : [cv2.imread((IMAGES / "features" / 'bottom' / f"{i}.png").as_posix()) for i in range(8)]
        }
    bottom_index = 0
    top_index = 0
    idle_count = 0
    frame_delay = 0.1

    def fade_in(self):
        """
        Fade in animation.
        """
        self.fade_index += 1
        if self.fade_index == len(self.fade_images)-1:
            self.current_animation_algorithm = self.idle
        return self.fade_images[self.fade_index]

    def fade_out(self):
        """
        Fade out animation.
        """
        self.fade_index -= 1
        if self.fade_index == 0:
            self.current_animation_algorithm = self.fade_in
        return self.fade_images[self.fade_index]

    def idle(self):
        """
        Idle animation.
        """

        self.idle_count += 1
        if self.idle_count > 100:
            self.idle_count = 0
            self.current_animation_algorithm = self.sleep

        # if closed eyes, open them
        if (self.top_index == 0 or self.top_index == 4) and random() > 0.02:
            self.top_index = choice([1, 2, 3])
        else:
            # Unchanged
            if random() > 0.99:
                self.top_index = choice([0,4])
            elif 0.99 > random() > 0.9:
                self.top_index = choice([1,2,3])
        if random() > 0.99:
            self.bottom_index = choice([0,1,6])

        return cv2.vconcat([self.features['top'][self.top_index],
                            self.features['bottom'][self.bottom_index]])

    def sleep(self):
        """
        Sleep animation.
        """
        if self.fade_index > 6:
            self.fade_index -= 1
        return self.fade_images[self.fade_index]

    def speak(self, word: str):
        """
        Speak animation.
        """

class Stream(Generator, Animation):
    """
    Iterator class to return frames of an animation.
    """
    glitcher = ImageGlitcher()

    def __init__(self):
        super().__init__()
        self.current_animation_algorithm = self.fade_in

    @classmethod
    def glitch(cls, img: np.ndarray) -> np.ndarray:
        """
        Glitch animation.
        """
        glitched_pil_image = cls.glitcher.glitch_image(src_img=cv2_to_image(img), glitch_amount=1, glitch_change=0.1, cycle=True, color_offset=False, scan_lines=True, gif=False, frames=23, step=1)
        glitched_img = image_to_cv2(glitched_pil_image)
        return glitched_img

    def send(self, value):
        """
        Send the next frame.
        """
        sleep(self.frame_delay)
        base = self.current_animation_algorithm()
        img = self.glitch(base)
        return img

    def throw(self, typ=None, val=None, tb=None):
        print("Exception Thrown in Generator.")
        raise StopIteration

def generate_frames(queue):
    """
    Generator function to return frames of an animation.
    """
    stream = Stream()
    while True:
        queue.put(next(stream))

def stream_frames():
    """
    Read frames from the queue.
    """

    import multiprocessing as mp
    queue = mp.Queue()

    generator = mp.Process(target=generate_frames, args=(queue, ))
    generator.start()

    while True:
        img = queue.get()
        (_flag, encoded_image) = cv2.imencode(".jpg", img)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(encoded_image) + b'\r\n')

def handle_text(text: str):

    for word in nltk.word_tokenize(text):
        phonemes = get_phonemes(word)
        words_queue.put(phonemes)
