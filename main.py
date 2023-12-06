from pico2d import open_canvas, delay, close_canvas
import game_framework

import title_mode as start_mode

open_canvas(1200, 650)
game_framework.run(start_mode)
close_canvas()

# 공 구속 조정
# 상대 모션 재생 안됨 (이거 어케함 ㄹㅇ)
# 상대 스매시 공 높을때만 하도록
# 상대 모션 점프 스매시 추가
# 상대 공 놓칠 확률 조정
# 판정 범위 조정 (하이/언더 구별) X 너무 어려워짐

# 일시정지도 추가할까
