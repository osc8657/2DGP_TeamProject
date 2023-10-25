from pico2d import *
import game_stadium


# 우측 키 이벤트
def right_down(e):
    pass
def right_up(e):
    pass

#좌측 키 이벤트
def left_down(e):
    pass
def left_up(e):
    pass

# 점프 이벤트
def alt_down(e):
    pass

# 스윙 이벤트
def ctrl_down(e):
    pass

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
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player, e):
        pass

    @staticmethod
    def draw(player, e):
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
        # player.frame = (boy.frame + 1) % 8 (애니메이션 프레임)
        # player.x += player.dir * 5 (dir : 플레이어가 향하는 방향 1,-1)
        pass

    @staticmethod
    def draw(player):
        #player.image.clip_draw()
        pass

    pass

# 스윙 클래스
class Swing:
    pass

# 점프 클래스
class Jump:
    pass

# 착지 클래스
class Landing:
    pass

# 점프 스매시 클래스
class Jump_smash:
    pass

# 상태변환 클래스
class StateMachine:

    def __init__(self, player):
        self.player = player
        self.cur_state = Wait
        self.transition = {
            Wait : {right_down: Run, left_down: Run, right_up: Run, left_up: Run, alt_down: Jump, ctrl_down: Swing},
            Run : {right_down: Wait, right_up: Wait, left_down: Wait, left_up: Wait, alt_down: Jump, ctrl_down: Swing},
            Jump : {ctrl_down: Jump_smash, jump_over: Landing},
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

# 플레이어 클래스
class Player:
    pass