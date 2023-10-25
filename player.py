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

#위쪽 키 이벤트
def up_down(e):
    pass
def up_up(e):
    pass

# 스페이스 키 이벤트
def space_down(e):
    pass
def space_up(e):
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

# 점프 스매시 클래스
class Jump_smash:
    pass

# idle 클래스
class Idle:
    pass

# 상태변환 클래스
class StateMachine:
    pass

# 플레이어 클래스
class Player:
    pass