from pico2d import *
import game_framework

import play_mode
import title_mode

import player
import game_world

import time

def init():
    play_mode.player.x, play_mode.player.y = 400, 150

    play_mode.opponent.x, play_mode.opponent.y = 850, 150

    if play_mode.who_sub == 'player':
        play_mode.cock.x, play_mode.cock.y = play_mode.player.x+25, play_mode.player.y-25
        play_mode.player.state_machine.cur_state = player.Serve
    else:
        play_mode.cock.x, play_mode.cock.y = play_mode.opponent.x-25, play_mode.opponent.y-25
        play_mode.player.state_machine.cur_state = player.Wait
    play_mode.cock.state = 'NONE'


    global x
    x = time.time()

    global state
    state = 'cannot'

    global count
    count = 0

    global count_notice_font
    count_notice_font = load_font('ENCR10B.TTF', 30)

    global count_font
    count_font = load_font('ENCR10B.TTF', 200)

    global win_font
    win_font = load_font('ENCR10B.TTF', 100)

    global regame_font
    regame_font = load_font('ENCR10B.TTF', 30)

    global exit_font
    exit_font = load_font('ENCR10B.TTF', 30)

    pass


def finish():
    pass

def update():
    global state
    global count
    if time.time() - x > 3:
        state = 'can'
    else:
        count = 3 - int(time.time() - x)
    pass

def draw():
    global state

    clear_canvas()
    game_world.render()
    if play_mode.who_win != None:
        win_font.draw(280, 400, play_mode.who_win, (255,255,255))
        regame_font.draw(410, 280, 'press space to regame', (255,255,255))
        exit_font.draw(440, 240, 'press esc to quit', (255,255,255))
    else:
        if state == 'cannot':
            count_font.draw(550, 400, str(count), (255,255,255))
            count_notice_font.draw(500, 550, 'serve count', (255,255,255))
    update_canvas()

def handle_events():
    events = get_events()

    if play_mode.who_win == None:
        if state == 'can':
            game_framework.pop_mode()
    elif play_mode.who_win != None:
        for event in events:
            if event.type == SDL_QUIT:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN:
                match event.key:
                    case pico2d.SDLK_SPACE:
                        game_world.clear()
                        game_framework.change_mode(title_mode)
                    case pico2d.SDLK_ESCAPE:
                        game_framework.quit()

def pause():
    pass

def resume():
    pass