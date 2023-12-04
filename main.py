from pico2d import open_canvas, delay, close_canvas
import game_framework

import title_mode as start_mode

open_canvas(1200, 600)
game_framework.run(start_mode)
close_canvas()

# 공 구속 조정
# 상대 모션 재생 안됨 (이거 어케함 ㄹㅇ)
# 플레이어 프레임 재생 조정
# 판정 범위 조정 (하이/언더 구별)
# 점프키 위쪽 방향키로 변경
# 게임 방법 설명 추가 (게임방식, 듀스, 점프 스매시 주의사항, press space or esc)
# 일시정지도 추가할까
