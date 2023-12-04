from pico2d import open_canvas, delay, close_canvas
import game_framework

import title_mode as start_mode

open_canvas(1200, 600)
game_framework.run(start_mode)
close_canvas()

# 공 구속 조정
# 상대 모션 재생 안됨 (이거 어케함 ㄹㅇ)
# 판정 범위 조정 (하이/언더 구별) X 너무 어려워짐

# 일시정지도 추가할까
