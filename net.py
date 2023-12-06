from pico2d import *

class Net:

    def __init__(self):
        self.image = load_image('net.png')
        pass

    def update(self):
        pass

    def draw(self):
        self.image.draw(600,80)


    def get_bb(self):
        return 591, 60, 606, 187

    def handle_collision(self, group, other):
        match group:
            case 'cock:net':
                pass