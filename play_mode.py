import random

from pico2d import *
import game_framework

import game_world
from stadium import Stadium
from player import Player
from cock import Cock
from opponent import Opponent
from player import Player
from net import Net
from ground import Ground
# ...

# 조작
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)
    pass

# 월드 생성
def init():
    global stadium  # 경기장
    global ground
    global net      # 네트
    global player   # 플레이어
    global opponent # 상대방

    running = True

    stadium = Stadium()
    game_world.add_object(stadium, 0)

    ground = Ground()
    game_world.add_object(ground, 1)
    game_world.add_collision_pair('cock:ground', None, ground)

    net = Net()
    game_world.add_object(net, 1)
    game_world.add_collision_pair('cock:net', None, net)

    player = Player()
    game_world.add_object(player, 2)

    global cock
    cock = Cock()
    game_world.add_object(cock, 3)
    game_world.add_collision_pair('cock:ground', cock, None)
    game_world.add_collision_pair('cock:net', cock, None)

    #opponent = Opponent()
    #game_world.add_object(opponent, 2)




    pass

def finish():
    game_world.clear()
    pass

# 월드 업데이트
def update():
    game_world.update()
    game_world.handle_collisions()
    pass

# 월드 그리기
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass