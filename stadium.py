from pico2d import *

class Stadium:

    def __init__(self):
        self.image = load_image('stadium.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)