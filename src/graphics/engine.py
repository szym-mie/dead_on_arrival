import time

from pygame import display, init


class Engine:
    def __init__(self):
        init()

        self.screen = None
        self.clock = time.clock()

    def init_screen(self, width, height):
        self.screen = display.set_mode((width, height))
