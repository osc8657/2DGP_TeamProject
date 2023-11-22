from pico2d import *
import game_framework
import game_world
import play_mode
import time


# 우측 키 이벤트
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

#좌측 키 이벤트
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

# 스윙(숏) 이벤트
def z_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_z

# 스윙(롱) 이벤트
def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x


# 스매시 이벤트
def shift_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT

# 점프 이벤트
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE

# time over
def time_out(e):
    return e[0] == 'TIME_OUT'

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

# 대기 클래스
class Wait:
    @staticmethod
    def enter(player, e):
        if player.face_dir == -1: # 왼쪽
            player.action = 2
        elif player.face_dir == 1: # 오른쪽
            player.action = 3
        player.dir = 0
        player.frame = 0
        pass

    @staticmethod
    def exit(player, e):
        # 스윙 입력시 스윙 점프 입력시 점프
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)
        pass

# 이동 클래스
class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):
            player.dir, player.action, player.face_dir = 1, 1, 1
        elif left_down(e) or right_up(e):
            player.dir, player.action, player.face_dir = -1, 0, -1
            pass

    @staticmethod
    def exit(player, e):
        # 스윙시 스윙, 점프시 점프
        pass

    @staticmethod
    def do(player):
        # 이동에 따른 프레임 추가
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8 #(애니메이션 프레임)
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time #(dir : 플레이어가 향하는 방향 1,-1)
        player.x = clamp(25, player.x, 1600-25) # 캔버스 좌, 우 한계선
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)
        pass

    pass

# 스윙(숏) 클래스
class Swing_short:
    @staticmethod
    def enter(player, e):
        if play_mode.cock.y < 90:
            player.action = 1 # 언더 스윙
        else:
            player.action = 1 # 하이 스윙
        play_mode.cock.current_time = time.time()
        play_mode.cock.sx, play_mode.cock.sy = player.x, player.y
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        play_mode.cock.state = 'SHORT'
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)
        pass

    pass

# 스윙(롱) 이벤트
class Swing_long:
    @staticmethod
    def enter(player, e):
        if play_mode.cock.y < 90:
            player.action = 1 # 언더 스윙
        else:
            player.action = 1 # 하이 스윙
        play_mode.cock.current_time = time.time()
        play_mode.cock.sx= player.x
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        play_mode.cock.state = 'LONG'

        # 충돌 처리
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)
        pass

    pass

# 스매시 이벤트
class Smash:
    @staticmethod
    def enter(player, e):
        player.action = 1 # 하이
        play_mode.cock.current_time = time.time()
        play_mode.cock.sx, play_mode.cock.sy = player.x, player.y
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        play_mode.cock.state = 'SMASH'

        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)
        pass

    pass

# 점프 클래스
class Jump:
    @staticmethod
    def enter(player, e):
        player.motion_time = get_time()
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8  # (애니메이션 프레임)
        player.y += JUMP_SPEED_PPS * game_framework.frame_time  # (dir : 플레이어가 향하는 방향 1,-1)
        if get_time() - player.motion_time > 1:
            player.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)
        pass

    pass

# 착지 클래스
class Landing:
    @staticmethod
    def enter(player, e):
        player.motion_time = get_time()
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8  # (애니메이션 프레임)
        player.y -= JUMP_SPEED_PPS * game_framework.frame_time  # (dir : 플레이어가 향하는 방향 1,-1)
        if get_time() - player.motion_time > 1:
            player.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)
        pass

    pass

# 점프 스매시 클래스
class Jump_smash:
    @staticmethod
    def enter(player, e):
        player.action = 1  # 점프 스매시
        play_mode.cock.current_time = time.time()
        play_mode.cock.sx, play_mode.cock.sy = player.x, player.y
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        play_mode.cock.state = 'JUMP_SMASH'
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 100, player.action * 100, 100, 100, player.x, player.y)

        pass

    pass

# 상태변환 클래스
class StateMachine:

    def __init__(self, player):
        self.player = player
        self.cur_state = Wait
        self.transition = {
            Wait : {right_down: Run, left_down: Run, right_up: Run, left_up: Run, z_down: Swing_short, x_down: Swing_long, shift_down: Smash, space_down: Jump},
            Run : {right_down: Wait, right_up: Wait, left_down: Wait, left_up: Wait, z_down: Swing_short, x_down: Swing_long, shift_down: Smash, space_down: Jump},
            Jump : {shift_down: Jump_smash, time_out: Landing},
            Landing : {time_out: Wait},
            Swing_short : {time_out: Wait},
            Swing_long : {time_out: Wait},
            Smash : {time_out: Wait},
            Jump_smash : {time_out: Landing}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transition[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                print(self.cur_state)
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)

# 플레이어 클래스
class Player:

    def __init__(self):
        self.x, self.y = 400, 100# 대충 임의의 값 넣음 수정필요
        self.frame = 0
        self.action = 0 # 임의의 값, 대기 액션으로 값 넣어야댐
        self.face_dir = 1
        self.dir = 0 # 플레이어 진행 방향
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.motion_time = 0

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50
    pass