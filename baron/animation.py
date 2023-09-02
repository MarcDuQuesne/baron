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
        self.fade_images = [cv2.imread((IMAGES / "fade" / f"{i:03d}.png").as_posix()) for i in range(23)]
        self.fade_index = -1
        self.current_animation_algorithm = self.fade_in

        self.features = {
            'top': [cv2.imread((IMAGES / "features" / 'top' / f"{i}.png").as_posix()) for i in range(5)],
            'bottom' : [cv2.imread((IMAGES / "features" / 'bottom' / f"{i}.png").as_posix()) for i in range(8)]
        }
        self.bottom_index = 0
        self.top_index = 0

        self.idle_count = 0

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
        if self.fade_index > 6:
            self.fade_index -= 1
        return self.fade_images[self.fade_index]

    def speak(self, word: str):
        """
        Speak animation.
        """
        pass

    def send(self, value):
        """
        Send the next frame.
        """
        return self.current_animation_algorithm()

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

            (_flag, encoded_image) = cv2.imencode(".jpg", img)
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                bytearray(encoded_image) + b'\r\n')
        except StopIteration:
            break
