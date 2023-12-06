from pico2d import *

class Ground:

    def __init__(self):
        self.image = load_image('ground.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(600, 30)

    def get_bb(self):
        return 0, 0, 1200, 60

    def handle_collision(self, group, other):
        match group:
            case 'cock:ground':
                pass