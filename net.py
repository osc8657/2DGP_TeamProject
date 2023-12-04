from pico2d import *

class Net:

    def __init__(self):
        self.image = load_image('net.png')
        pass

    def update(self):
        pass

    def draw(self):
        self.image.draw(600,40)
        draw_rectangle(*self.get_bb())


    def get_bb(self):
        return 590, 60, 610, 150

    def handle_collision(self, group, other):
        match group:
            case 'cock:net':
                pass