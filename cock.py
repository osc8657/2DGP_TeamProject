import time

from pico2d import *
import game_framework
import game_world
import play_mode
import next_mode

import player

PIXEL_PER_METER = (10.0 / 0.25)  # 10 pixel 33 cm

# 롱--------------------------------------------------
LX_RUN_SPEED_KMPH = 60  # Km / Hour
LX_RUN_SPEED_MPM = (LX_RUN_SPEED_KMPH * 1000.0 / 60.0)
LX_RUN_SPEED_MPS = (LX_RUN_SPEED_MPM / 60.0)
LX_RUN_SPEED_PPS = (LX_RUN_SPEED_MPS * PIXEL_PER_METER)

LY_RUN_SPEED_KMPH = 90.0  # Km / Hour
LY_RUN_SPEED_MPM = (LY_RUN_SPEED_KMPH * 1000.0 / 60.0)
LY_RUN_SPEED_MPS = (LY_RUN_SPEED_MPM / 60.0)
LY_RUN_SPEED_PPS = (LY_RUN_SPEED_MPS * PIXEL_PER_METER)
# 숏--------------------------------------------
SX_RUN_SPEED_KMPH = 55.0  # Km / Hour
SX_RUN_SPEED_MPM = (SX_RUN_SPEED_KMPH * 1000.0 / 60.0)
SX_RUN_SPEED_MPS = (SX_RUN_SPEED_MPM / 60.0)
SX_RUN_SPEED_PPS = (SX_RUN_SPEED_MPS * PIXEL_PER_METER)

SY_RUN_SPEED_KMPH = 40.0  # Km / Hour
SY_RUN_SPEED_MPM = (SY_RUN_SPEED_KMPH * 1000.0 / 60.0)
SY_RUN_SPEED_MPS = (SY_RUN_SPEED_MPM / 60.0)
SY_RUN_SPEED_PPS = (SY_RUN_SPEED_MPS * PIXEL_PER_METER)
# 스매시--------------------------------------------------
SMX_RUN_SPEED_KMPH = 180.0  # Km / Hour
SMX_RUN_SPEED_MPM = (SMX_RUN_SPEED_KMPH * 1000.0 / 60.0)
SMX_RUN_SPEED_MPS = (SMX_RUN_SPEED_MPM / 60.0)
SMX_RUN_SPEED_PPS = (SMX_RUN_SPEED_MPS * PIXEL_PER_METER)

SMY_RUN_SPEED_KMPH = -30.0  # Km / Hour
SMY_RUN_SPEED_MPM = (SMY_RUN_SPEED_KMPH * 1000.0 / 60.0)
SMY_RUN_SPEED_MPS = (SMY_RUN_SPEED_MPM / 60.0)
SMY_RUN_SPEED_PPS = (SMY_RUN_SPEED_MPS * PIXEL_PER_METER)
# 점프 스매시----------------------------------------------
JSMX_RUN_SPEED_KMPH = 200.0  # Km / Hour
JSMX_RUN_SPEED_MPM = (JSMX_RUN_SPEED_KMPH * 1000.0 / 60.0)
JSMX_RUN_SPEED_MPS = (JSMX_RUN_SPEED_MPM / 60.0)
JSMX_RUN_SPEED_PPS = (JSMX_RUN_SPEED_MPS * PIXEL_PER_METER)

JSMY_RUN_SPEED_KMPH = -55.0  # Km / Hour
JSMY_RUN_SPEED_MPM = (JSMY_RUN_SPEED_KMPH * 1000.0 / 60.0)
JSMY_RUN_SPEED_MPS = (JSMY_RUN_SPEED_MPM / 60.0)
JSMY_RUN_SPEED_PPS = (JSMY_RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0


def wait(cock):
    cock.dir = 0
    cock.sx, cock.sy = None, None
    if play_mode.who_sub == 'player':
        cock.x, cock.y = play_mode.player.x+25, play_mode.player.y-25
        # cock.x, cock.y = play_mode.player.x+30, play_mode.player.y +80
    else:
        cock.x, cock.y = play_mode.opponent.x-25, play_mode.opponent.y-25

def long_shot(cock):
    cock.play_time = time.time() - cock.current_time

    if cock.dir == 1:
        cock.x += (LX_RUN_SPEED_PPS - cock.sx / (1200 / cock.sx) - cock.sy / (450 / cock.sy)) * game_framework.frame_time
        cock.y += (LY_RUN_SPEED_PPS - cock.sx / (700 / cock.sx) - cock.sy / (150 / cock.sy)) * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2
    else:
        cock.x -= (LX_RUN_SPEED_PPS - cock.sx / (1200 / cock.sx) - cock.sy / (450 / cock.sy)) * game_framework.frame_time
        cock.y += (LY_RUN_SPEED_PPS - cock.sx / (700 / cock.sx) - cock.sy / (150 / cock.sy)) * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2



def short_shot(cock):
    cock.play_time = time.time() - cock.current_time

    if cock.dir == 1:
        cock.x += (SX_RUN_SPEED_PPS - cock.sx / (1200/cock.sx) - cock.sy / (200/cock.sy)) * game_framework.frame_time
        cock.y += (SY_RUN_SPEED_PPS - cock.sx / (1200/cock.sx) - cock.sy / (900/cock.sy)) * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2
    else:
        cock.x -= (SX_RUN_SPEED_PPS - cock.sx / (1200/cock.sx) - cock.sy / (200/cock.sy)) * game_framework.frame_time
        cock.y += (SY_RUN_SPEED_PPS - cock.sx / (1200/cock.sx) - cock.sy / (900/cock.sy)) * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2
        pass
def smash(cock):
    cock.play_time = time.time() - cock.current_time

    if cock.dir == 1:
        cock.x += (SMX_RUN_SPEED_PPS - cock.sx / (500 / cock.sx)) * game_framework.frame_time
        cock.y += (SMY_RUN_SPEED_PPS - cock.sx / (600 / cock.sx)) * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2
    else:
        cock.x -= (SMX_RUN_SPEED_PPS - cock.sx / (500 / cock.sx)) * game_framework.frame_time
        cock.y += (SMY_RUN_SPEED_PPS - cock.sx / (600 / cock.sx)) * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2

    pass

def jump_smash(cock):
    cock.play_time = time.time() - cock.current_time

    if cock.dir == 1:
        cock.x += (JSMX_RUN_SPEED_PPS - cock.sx / (450 / cock.sx)) * game_framework.frame_time
        cock.y += (JSMY_RUN_SPEED_PPS - cock.sx / (300 / cock.sx)) * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2
    else:
        cock.x -= (JSMX_RUN_SPEED_PPS - cock.sx / (450 / cock.sx)) * game_framework.frame_time
        cock.y += (JSMY_RUN_SPEED_PPS - cock.sx / (300 / cock.sx)) * game_framework.frame_time + 1 / 2 * cock.gravity * (cock.play_time) ** 2
    pass

def game_over(cock, case):
    if case == 'COURT_OUT!':
        if cock.x > 610 and cock.x < 1110: #상대 코트 내부일때
            play_mode.player_score += 1
            play_mode.who_sub = 'player'
        elif cock.x < 100: # 내 코트 뒤편으로 나갔을 떄
            play_mode.player_score += 1
            play_mode.who_sub = 'player'
        else:
            play_mode.opponent_score += 1
            play_mode.who_sub = 'opponent'

    if case == 'NET_OUT!':
        if cock.dir == 1:
            play_mode.opponent_score += 1
            play_mode.who_sub = 'opponent'
        else:
            play_mode.player_score += 1
            play_mode.who_sub = 'player'

    print('[',case,']',play_mode.player_score,':',play_mode.opponent_score)

    if play_mode.player_score == play_mode.opponent_score and play_mode.player_score > 19:
        cock.game_state = 'DEUCE'


    if cock.game_state == 'DEUCE':
        if play_mode.player_score == 29 or play_mode.opponent_score == 29:
            if play_mode.player_score == 30:
                play_mode.who_win = 'PLAYER WIN!'
            elif play_mode.opponent_score == 30:
                play_mode.who_win = 'OPPONENT WIN!'

        if play_mode.player_score > play_mode.opponent_score + 1:
            play_mode.who_win = 'PLAYER WIN!'
        elif play_mode.opponent_score > play_mode.player_score + 1:
            play_mode.who_win = 'OPPPONENT WIN!'
    else:
        if play_mode.player_score == 21:
            play_mode.who_win = 'PLAYER WIN!'
        elif play_mode.opponent_score == 21:
            play_mode.who_win = 'OPPONENT WIN!'

    game_framework.push_mode(next_mode)


class Cock:
    image = None

    def __init__(self):
        if Cock.image == None:
            Cock.image = load_image('cock.png')
        self.x, self.y = play_mode.player.x, play_mode.player.y
        self.state = 'NONE'
        self.dir = 0

        self.gravity = -9.8
        self.current_time = 0
        self.play_time = 0
        self.sx, self.sy = None, None

        self.game_state = 'NONE'

    def draw(self):
        self.image.draw(self.x, self.y)


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

        self.x = clamp(10, self.x, 1190)
        self.y = clamp(60, self.y, 650)

    def get_bb(self):
        return self.x-10, self.y-10, self.x+10, self.y+10
        pass

    def handle_collision(self, group, other):
        match group:
            case 'cock:ground':
                game_over(self, 'COURT_OUT!')
                pass
            case 'cock:net':
                game_over(self, 'NET_OUT!')
                pass