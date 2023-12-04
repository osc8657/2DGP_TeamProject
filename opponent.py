from pico2d import *

import game_framework
import game_world
from behavior_tree import *
import play_mode

import random
import time


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


class Opponent:
    def __init__(self):
        self.x, self.y = 800, 150
        self.frame = 0
        self.dir = 0
        self.state = 'WAIT'
        self.image = load_image('opponent_animation_sheet.png')
        self.action = 5

        self.tx, self.ty = 800, 100
        self.what_to_do = 'WAIT'
        self.serve_count = 0

        self.build_behavior_tree()
        pass

    def get_bb(self):
        return self.x - 20, self.y - 90, self.x + 20, self.y + 50

    def update(self):
        if self.state =='wait':
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 1
        elif self.state == 'serve':
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5 + 2
        elif self.state == 'move':
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.bt.run()

    def draw(self):
        self.image.clip_draw(int(self.frame)*200, self.action*200, 200, 200, self.x, self.y, 250, 250)
        draw_rectangle(*self.get_bb())
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
        self.state = 'wait'

    def move_to(self, r = 0.5):
        if self.tx > self.x:
            self.action = 3
        else:
            self.action = 2

        self.state = 'move'

        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def wait(self):
        self.action = 5
        return BehaviorTree.SUCCESS

    def can_hit_cock(self):
        if play_mode.cock.x > 600:
            if play_mode.cock.x > self.x - 80:
                if play_mode.cock.x < self.x + 80:
                    if play_mode.cock.y > self.y - 80:
                        if play_mode.cock.y < self.y + 80:
                            miss = random.randint(0,20)
                            if miss == 0:
                                return BehaviorTree.FAIL
                            play_mode.cock.current_time = time.time()
                            play_mode.cock.sx, play_mode.cock.sy = self.x, self.y
                            return BehaviorTree.SUCCESS

        return BehaviorTree.FAIL
    def swing(self):
        what = 0
        play_mode.cock.sx = self.x
        if play_mode.cock.y > self.y + 30:
            self.action = 1  # 하이 스윙 액션
            what = random.randint(1,3)
            if what == 1:
                play_mode.cock.state = 'SMASH'
            else:
                play_mode.cock.state = 'LONG'
        else:
            self.action = 0 # 언더 스윙 액션
            what = random.randint(1,2)
            if what == 1:
                play_mode.cock.state = 'LONG'
            else:
                play_mode.cock.state = 'SHORT'

        print(play_mode.cock.state)
        play_mode.cock.dir = -1
        return BehaviorTree.SUCCESS

    def set_location_to_swing(self):
        if play_mode.cock.dir == 1:
            if play_mode.cock.state == 'LONG':
                # if play_mode.cock.sx > 250:
                #     self.tx = play_mode.cock.sx + 70 - play_mode.cock.sx / 2
                # else:
                #     self.tx = play_mode.cock.sx + 70
                self.tx = 1000
            elif play_mode.cock.state == 'SHORT':
                # if play_mode.cock.sx > 250:
                #     self.tx = play_mode.cock.sx + 55 - play_mode.cock.sx / 2
                # else:
                #     self.tx = play_mode.cock.sx + 55
                self.tx = 650
            elif play_mode.cock.state == 'SMASH':
                # if play_mode.cock.sx > 250:
                #     self.tx = play_mode.cock.sx + 200
                # else:
                #     self.tx = play_mode.cock.sx + 200
                self.tx = 800
            elif play_mode.cock.state == 'JUMP_SMASH':
                # if play_mode.cock.sx > 250:
                #     self.tx = play_mode.cock.sx + 250
                # else:
                #     self.tx = play_mode.cock.sx + 250
                self.tx = 800
            self.ty = 150
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
                            miss = random.randint(0,20)
                            if miss == 0:
                                return BehaviorTree.FAIL
                            play_mode.cock.current_time = time.time()
                            play_mode.cock.sx, play_mode.cock.sy = self.x, self.y
                            return BehaviorTree.SUCCESS

        return BehaviorTree.FAIL

    def serve(self):

        x = random.randint(1,2)
        play_mode.cock.dir = -1
        self.action = 5 # 언더 액션
        if x == 1:
            play_mode.cock.state = 'SHORT'
        else:
            play_mode.cock.state = 'LONG'
        print('serve : ', play_mode.cock.state)
        play_mode.who_sub = None
        return BehaviorTree.SUCCESS


    def build_behavior_tree(self):

        a1 = Action('Set target location to center of court', self.set_target_location, 850, 150)
        a2 = Action('move to', self.move_to)

        SEQ_move_to_center_of_court = Sequence('move to center', a1, a2)

        a3 = Action('wait', self.wait)

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