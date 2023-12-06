from pico2d import *

import game_framework
import game_world
from behavior_tree import *
import play_mode

import random
import time

HIGH_AREA_X1 = 100
HIGH_AREA_X2 = 50
HIGH_AREA_Y1 = 50
HIGH_AREA_Y2 = 100

UNDER_AREA_X1 = 100
UNDER_AREA_X2 = 70
UNDER_AREA_Y1 = 120
UNDER_AREA_Y2 = 50

HIT_AREA_X1 = 100
HIT_AREA_X2 = 100
HIT_AREA_Y1 = 100
HIT_AREA_Y2 = 100


# Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Jumping speed
JUMP_SPEED_KMPH = 20.0
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

def miss():
    x = random.randint(1,100)
    if play_mode.cock.state == 'LONG':
        if x >= 0 and x < 10:
            return 0
    elif play_mode.cock.state == 'SHORT':
        if x >= 0 and x < 10:
            return 0
    elif play_mode.cock.state == 'SMASH':
        if x >= 0 and x < 30:
            return 0
    elif play_mode.cock.state == 'JUMP_SMASH':
        if x >= 0 and x < 40:
            return 0
    else:
        return 1

animation_names = ['high', 'jump', 'jump_smash', 'landing', 'serve', 'under', 'wait', 'walk_back', 'walk_front']

class Opponent:
    images = None
    clear_sound = None
    miss_sound = None
    serve_sound = None
    smash_sound = None

    def load_images(self):
        if Opponent.images == None:
            Opponent.images = {}
            for name in animation_names:
                if name == 'wait' or 'jump' or 'landing':
                    Opponent.images[name] = [load_image("./opponent/" + name + " (%d)" % i + ".png") for i in range(1, 2)]
                elif name == 'serve' or 'jump_smash':
                    Opponent.images[name] = [load_image("./opponent/" + name + " (%d)" % i + ".png") for i in range(1, 6)]
                else:
                    Opponent.images[name] = [load_image("./opponent/" + name + " (%d)" % i + ".png") for i in range(1, 9)]
    def __init__(self):
        self.x, self.y = 800, 180
        self.frame = 0
        self.dir = 0
        self.load_images()
        self.state = 'wait'
        self.action = 5

        self.tx, self.ty = 800, 100

        if not Opponent.clear_sound:
            self.clear_sound = load_wav('./sound/clear_sound.wav')
            self.clear_sound.set_volume(32)
            self.miss_sound = load_wav('./sound/miss_sound.wav')
            self.miss_sound.set_volume(32)
            self.serve_sound = load_wav('./sound/serve_sound.wav')
            self.serve_sound.set_volume(32)
            self.smash_sound = load_wav('./sound/smash_sound.wav')
            self.smash_sound.set_volume(32)

        self.build_behavior_tree()
        pass

    def get_bb(self):
        pass

    def update(self):
        if self.state == 'wait' or 'jump' or 'landing':
            self.frame = (self.frame + 1 * ACTION_PER_TIME * game_framework.frame_time) % 1
        elif self.state == 'serve' or 'jump_smash':
            self.frame = (self.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.bt.run()

    def draw(self):
        Opponent.images[self.state][int(self.frame)].draw(self.x, self.y, 300, 300)

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 =(x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 <(PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r = 0.5):
        if self.tx > self.x:
            self.state = 'walk_back'
        else:
            self.state = 'walk_front'

        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def wait(self):
        self.state = 'wait'
        return BehaviorTree.SUCCESS

    def can_hit_cock(self):
        if play_mode.cock.x > 600:
            # 하이
            if self.x - HIGH_AREA_X1 < play_mode.cock.x:
                if play_mode.cock.x < self.x + HIGH_AREA_X2:
                    if self.y + HIGH_AREA_Y1 < play_mode.cock.y:
                        if play_mode.cock.y < self.y + HIGH_AREA_Y2:
                            if miss() == 0:
                                return BehaviorTree.FAIL
                            self.state = 'high'
                            play_mode.cock.current_time = time.time()
                            play_mode.cock.sx, play_mode.cock.sy = 1200 - self.x, self.y
                            play_mode.cock.dir = -1
                            return BehaviorTree.SUCCESS
            # 언더
            if self.x - UNDER_AREA_X1 < play_mode.cock.x:
                if play_mode.cock.x < self.x - UNDER_AREA_X2 :
                    if self.y - UNDER_AREA_Y1 < play_mode.cock.y:
                        if play_mode.cock.y < self.y + UNDER_AREA_Y2:
                            if miss() == 0:
                                return BehaviorTree.FAIL
                            self.state = 'under'
                            play_mode.cock.current_time = time.time()
                            play_mode.cock.sx, play_mode.cock.sy = 1200 - self.x, self.y
                            play_mode.cock.dir = -1
                            return BehaviorTree.SUCCESS

        return BehaviorTree.FAIL
    def swing(self):
        what = 0
        if self.state == 'high':  # 하이 스윙 액션
            what = random.randint(1,3)
            if what == 1:
                if play_mode.cock.x < 940:
                    self.smash_sound.play()
                    play_mode.cock.state = 'SMASH'
                else:
                    self.clear_sound.play()
                    play_mode.cock.state = 'LONG'
            elif what == 2:
                self.clear_sound.play()
                play_mode.cock.state = 'LONG'
            else:
                self.serve_sound.play()
                play_mode.cock.state = 'SHORT'
        elif self.state == 'under':  # 언더 스윙 액션
            what = random.randint(1,2)
            if what == 1:
                self.clear_sound.play()
                play_mode.cock.state = 'LONG'
            else:
                self.serve_sound.play()
                play_mode.cock.state = 'SHORT'

        return BehaviorTree.SUCCESS

    def set_location_to_swing(self):
        if play_mode.cock.dir == 1:
            if play_mode.cock.state == 'LONG':
                self.tx = 1000
            elif play_mode.cock.state == 'SHORT':
                self.tx = 750
            elif play_mode.cock.state == 'SMASH':
                self.tx = 800
            elif play_mode.cock.state == 'JUMP_SMASH':
                self.tx = 800
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def if_player_swing(self):
        if play_mode.cock.dir == 1:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def if_serve_turn(self):
        if play_mode.cock.state == 'NONE':
            if play_mode.cock.x > self.x - 100:
                if play_mode.cock.x < self.x + 100:
                    if play_mode.cock.y > self.y - 100:
                        if play_mode.cock.y < self.y + 100:
                            play_mode.cock.current_time = time.time()
                            play_mode.cock.sx, play_mode.cock.sy = 1200 - self.x, self.y
                            return BehaviorTree.SUCCESS

        return BehaviorTree.FAIL

    def serve(self):
        x = random.randint(1,2)
        play_mode.cock.dir = -1
        self.state = 'serve' # 언더 액션
        self.serve_sound.play()
        if x == 1:
            play_mode.cock.state = 'SHORT'
        else:
            play_mode.cock.state = 'LONG'
        play_mode.who_sub = None
        return BehaviorTree.SUCCESS


    def build_behavior_tree(self):

        a1 = Action('Set target location to center of court', self.set_target_location, 850, 180)
        a2 = Action('move to', self.move_to)

        SEQ_move_to_center_of_court = Sequence('move to center', a1, a2)

        root = a3 = Action('wait', self.wait)

        SEQ_wait = Sequence('wait in center', SEQ_move_to_center_of_court, a3)

        c1 = Condition('can hit', self.can_hit_cock)
        a4 = Action('swing', self.swing)

        SEQ_swing = Sequence('swing', c1, a4)

        a5 = Action('set location to swing spot', self.set_location_to_swing)

        SEQ_move_to_location_to_swing = Sequence('move to location to swing', a5, a2)

        SEQ_move_and_swing = Sequence('move and swing if can hit', SEQ_move_to_location_to_swing, SEQ_swing)

        c2 = Condition('if player swing', self.if_player_swing)

        SEQ_do_if_player_swing = Sequence('do if player swing', c2, SEQ_move_and_swing)

        a6 = Action('serve', self.serve)
        c3 = Condition('if serve turn', self.if_serve_turn)

        SEQ_serve_if_serve_turn = Sequence('serve if serve turn', c3, a6)

        SEL_serve_or_wait = Selector('serve or wait', SEQ_serve_if_serve_turn, SEQ_wait)

        root = SEL_do_or_wait = Selector('do or wait', SEQ_do_if_player_swing, SEL_serve_or_wait)

        self.bt = BehaviorTree(root)

    pass