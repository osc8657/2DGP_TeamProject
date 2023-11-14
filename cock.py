from pico2d import *
import game_framework
import game_world

class Cock:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Cock.image == None:
            Cock.image = load_image('cock.png')
        self.x, self.y, self.velocity = x, y, velocity
        # 공격권에 따라 시작 위치 조정

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        # 콕을 쳣을 때 움직임 (숏, 롱, 스매시, 점프 스매시)
        #
        pass