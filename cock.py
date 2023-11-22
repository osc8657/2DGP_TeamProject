import time

from pico2d import *
import game_framework
import game_world
import play_mode
import game_framework

# 롱--------------------------------------------------
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
LX_RUN_SPEED_KMPH = 70.0  # Km / Hour
LX_RUN_SPEED_MPM = (LX_RUN_SPEED_KMPH * 1000.0 / 60.0)
LX_RUN_SPEED_MPS = (LX_RUN_SPEED_MPM / 60.0)
LX_RUN_SPEED_PPS = (LX_RUN_SPEED_MPS * PIXEL_PER_METER)

LY_RUN_SPEED_KMPH = 100.0  # Km / Hour
LY_RUN_SPEED_MPM = (LY_RUN_SPEED_KMPH * 1000.0 / 60.0)
LY_RUN_SPEED_MPS = (LY_RUN_SPEED_MPM / 60.0)
LY_RUN_SPEED_PPS = (LY_RUN_SPEED_MPS * PIXEL_PER_METER)

# 숏--------------------------------------------
SX_RUN_SPEED_KMPH = 55.0  # Km / Hour
SX_RUN_SPEED_MPM = (SX_RUN_SPEED_KMPH * 1000.0 / 60.0)
SX_RUN_SPEED_MPS = (SX_RUN_SPEED_MPM / 60.0)
SX_RUN_SPEED_PPS = (SX_RUN_SPEED_MPS * PIXEL_PER_METER)

SY_RUN_SPEED_KMPH = 65.0  # Km / Hour
SY_RUN_SPEED_MPM = (SY_RUN_SPEED_KMPH * 1000.0 / 60.0)
SY_RUN_SPEED_MPS = (SY_RUN_SPEED_MPM / 60.0)
SY_RUN_SPEED_PPS = (SY_RUN_SPEED_MPS * PIXEL_PER_METER)

# 스매시--------------------------------------------------
SMX_RUN_SPEED_KMPH = 200.0  # Km / Hour
SMX_RUN_SPEED_MPM = (SMX_RUN_SPEED_KMPH * 1000.0 / 60.0)
SMX_RUN_SPEED_MPS = (SMX_RUN_SPEED_MPM / 60.0)
SMX_RUN_SPEED_PPS = (SMX_RUN_SPEED_MPS * PIXEL_PER_METER)

SMY_RUN_SPEED_KMPH = -25.0  # Km / Hour
SMY_RUN_SPEED_MPM = (SMY_RUN_SPEED_KMPH * 1000.0 / 60.0)
SMY_RUN_SPEED_MPS = (SMY_RUN_SPEED_MPM / 60.0)
SMY_RUN_SPEED_PPS = (SMY_RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0


def wait(cock):
    cock.x, cock.y = play_mode.player.x, play_mode.player.y+80


def long_shot(cock):
    cock.play_time = time.time() - cock.current_time
    if cock.sx > 250:
        cock.x += (LX_RUN_SPEED_PPS - cock.sx / 2) * game_framework.frame_time
    else:
        cock.x += (LX_RUN_SPEED_PPS) * game_framework.frame_time
    cock.y += LY_RUN_SPEED_PPS * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2
    cock.y = clamp(60, cock.y, 600)


def short_shot(cock):
    cock.play_time = time.time() - cock.current_time
    if cock.sx > 250:
        cock.x += (SX_RUN_SPEED_PPS - cock.sx/2) * game_framework.frame_time
        cock.y += (SY_RUN_SPEED_PPS - cock.sy/1.5) * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2
    else:
        cock.x += (SX_RUN_SPEED_PPS) * game_framework.frame_time
        cock.y += SY_RUN_SPEED_PPS * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2
    cock.y = clamp(60, cock.y, 1200)


def smash(cock):
    cock.play_time = time.time() - cock.current_time
    if cock.sx > 250:
        cock.x += (SMX_RUN_SPEED_PPS) * game_framework.frame_time
        cock.y += (SMY_RUN_SPEED_PPS * game_framework.frame_time - cock.sx/200) + 1 / 2 * cock.gravity * (cock.play_time) ** 2
    else:
        cock.x += SMX_RUN_SPEED_PPS * game_framework.frame_time
        cock.y += SMY_RUN_SPEED_PPS * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2
    pass

def jump_smash(cock):
    cock.play_time = time.time() - cock.current_time
    if cock.sx > 250:
        cock.x += (SMX_RUN_SPEED_PPS) * game_framework.frame_time
        cock.y += (SMY_RUN_SPEED_PPS * game_framework.frame_time - cock.sx / 200) + 1 / 2 * cock.gravity * (cock.play_time) ** 2
    else:
        cock.x += SMX_RUN_SPEED_PPS * game_framework.frame_time
        cock.y += SMY_RUN_SPEED_PPS * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2
    pass

def game_over(cock, case):
    print(case)

    if case == 'COURT OUT!':
        if cock.x > 610 and cock.x < 1100: #상대 코트 내부일때
            print('1:0')
        elif cock.x < 100: # 내 코트 뒤편으로 나갔을 떄
            print('1:0')
        else:
            print('0:1')

    if case == 'NET OUT!':
        if cock.x < 595:
            print('0:1')
        else:
            print('1:0')

    game_world.remove_object(cock)
    pass


class Cock:
    image = None

    def __init__(self):
        if Cock.image == None:
            Cock.image = load_image('cock.png')
        self.x, self.y = play_mode.player.x, play_mode.player.y
        self.state = 'NONE'

        self.gravity = -9.8
        self.current_time = 0
        self.play_time = 0
        self.sx, self.sy = None, None

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())


    def update(self):
        match self.state:
            case 'NONE':
                wait(self)
            case 'LONG':
                long_shot(self)
            case 'SHORT':
                short_shot(self)
            case 'SMASH':
                smash(self)
            case 'JUMP_SMASH':
                jump_smash(self)

    def get_bb(self):
        return self.x-10, self.y-10, self.x+10, self.y+10
        pass

    def handle_collision(self, group, other):
        match group:
            case 'cock:ground':
                game_over(self, 'COURT OUT!')
                pass
            case 'cock:net':
                game_over(self, 'NET OUT!')
                pass