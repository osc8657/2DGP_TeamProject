from pico2d import *
import game_stadium

# 조작
def handle_event():
    pass

# 월드 생성
def create_world():
    global running
    global stadium  # 경기장
    global field    # 필드
    global net      # 네트
    global player   # 플레이어
    global opponent # 상대방

    running = True

    #stadium = Stadium()
    game_stadium.add(stadium)

    #field = Field()
    game_stadium.add(field)

    #net = Net()
    game_stadium.add(net)

    #player = Player()
    game_stadium.add(player)

    #opponent = Opponent()
    game_stadium.add(opponent)


    pass

# 월드 업데이트
def update_world():
    game_stadium.update()
    pass

# 월드 그리기
def render_world():
    clear_canvas()
    game_stadium.render()
    update_canvas()
    pass

while running:
    handle_event()
    update_world()
    render_world()
    delay(0.01)

close_canvas()