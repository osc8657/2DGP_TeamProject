from pico2d import *
import game_stadium


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

# 점프 이벤트
def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x

# 스윙 이벤트
def z_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_z

# 점프 중 이벤트 발생 없을 시
def jump_over(e):
    pass

# 착지 모션 끝
def L_motion_over(e):
    pass

# 스윙 모션 끝
def S_motion_over(e):
    pass

# 점프 스매시 모션 끝
def JS_motion_over(e):
    pass

# 대기 클래스
class Wait:
    @staticmethod
    def enter(player, e):
        player.action = 0 # 시트의 대기모션의 buttom위치
        player.dir = 0
        player.frame = 0
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player, e):
        player.frame = (player.frame + 1) % 8
        pass

    @staticmethod
    def draw(player, e):
        player.image.clip_draw()
        pass

# 이동 클래스
class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e):
            #오른쪽 이동
            pass
        elif left_down(e) or right_up(e):
            # 왼쪽 이동
            pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        # 이동에 따른 프레임 추가
        player.frame = (player.frame + 1) % 8 #(애니메이션 프레임)
        player.x += player.dir * 5 #(dir : 플레이어가 향하는 방향 1,-1)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw()
        pass

    pass

# 스윙 클래스
class Swing:
    @staticmethod
    def enter(player, e):
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass

    pass

# 점프 클래스
class Jump:
    @staticmethod
    def enter(player, e):
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass

    pass

# 착지 클래스
class Landing:
    @staticmethod
    def enter(player, e):
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass

    pass

# 점프 스매시 클래스
class Jump_smash:
    @staticmethod
    def enter(player, e):
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass

    pass

# 상태변환 클래스
class StateMachine:

    def __init__(self, player):
        self.player = player
        self.cur_state = Wait
        self.transition = {
            Wait : {right_down: Run, left_down: Run, right_up: Run, left_up: Run, x_down: Jump, z_down: Swing},
            Run : {right_down: Wait, right_up: Wait, left_down: Wait, left_up: Wait, x_down: Jump, z_down: Swing},
            Jump : {z_down: Jump_smash, jump_over: Landing},
            Landing : {L_motion_over: Wait},
            Swing : {S_motion_over: Wait},
            Jump_smash : {JS_motion_over: Landing}
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
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)

# 플레이어 클래스
class Player:

    def __init__(self):
        self.x, self.y = 50, 50 # 대충 임의의 값 넣음 수정필요
        self.frame = 0
        self.action = 0 # 임의의 값, 대기 액션으로 값 넣어야댐
        self.dir = 0 # 플레이어 진행 방향
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    pass