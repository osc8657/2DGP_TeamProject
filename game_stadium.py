

# 게임 월드의 표현
# 레이어로 다루도록 수정해야함
objects = []

# 월드에 객체를 넣는 함수
def add(o):
    objects.append(o)
    print('add complete')

# 월드의 객체들을 모두 업데이트하는 함수
def update():
    for o in objects:
        objects.update()
    print('update complete')

# 월드 객체들을 모두 그리는 함수
def render():
    for o in objects:
        objects.draw()
    print("render complete")