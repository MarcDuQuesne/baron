"""
Rules for creating animations.
"""

from time import sleep
from typing import Generator
from glitch_this import ImageGlitcher
import numpy as np
from PIL import Image

import cv2

from baron import IMAGES

def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    # return Image.fromarray(img)
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    # return np.asarray(img)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

class Frames(Generator):
    """
    Iterator class to return frames of an animation.
    """
    def __init__(self):
        super().__init__()
        # read in all the frames from files in the images/fade directory
        # pa
        self.frames = [cv2.imread(f"{IMAGES.as_posix()}/fade/{i:03d}.png", 0) for i in range(0, 23)]
        self.index = 0
        cv2.imshow("Frame", self.frames[0])

    def send(self, value):
        """
        Iterate through the frames.
        """
        self.index += 1 # increment the index
        self.index %= len(self.frames) # wrap around if necessary
        return self.frames[self.index]

    def throw(self, value):
        print("Exception Thrown in Generator.")
        raise StopIteration

def gen_frames():
    """
    Generator function to return frames of an animation.
    """
    frames = Frames()
    glitcher = ImageGlitcher()

    while True:
        sleep(0.1)
        try:

            # to PIL image
            pil_image = glitcher.glitch_image(src_img=convert_from_cv2_to_image(next(frames)), glitch_amount=1, glitch_change=0.1, cycle=True, color_offset=False, scan_lines=True, gif=False, frames=23, step=1)
            img = convert_from_image_to_cv2(pil_image)

            (_flag, encodedImage) = cv2.imencode(".jpg", img)
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encodedImage) + b'\r\n')
        except StopIteration:
            break

