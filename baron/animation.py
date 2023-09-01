"""
Rules for creating animations.
"""

from time import sleep

import cv2


class Frames:
    """
    Iterator class to return frames of an animation.
    """
    def __init__(self):
        # read in all the frames from files in the images/fade directory
        self.frames = [cv2.imread(f"images/fade/{i}.png") for i in range(1, 21)]
        self.index = 0

    def __next__(self):
        """
        Iterate through the frames.
        """
        self.index += 1 # increment the index
        self.index %= len(self.frames) # wrap around if necessary
        return self.frames[self.index]

    def __iter__(self):
        return self

def gen_frames():
    """
    Generator function to return frames of an animation.
    """
    frames = Frames()
    while True:
        sleep(0.25)
        yield next(frames)
