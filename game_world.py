

# 게임 월드의 표현
# 레이어로 다루도록 수정해야함
objects = [[] for _ in range(4)]

# 충돌 관점의 월드
# collision_pairs = {}

# 월드에 객체를 넣는 함수
def add_object(o, depth = 0):
    objects[depth].append(o)
    print('add complete')

def add_objects(ol, depth = 0):
    objects[depth] += ol

# 월드의 객체들을 모두 업데이트하는 함수
def update():
    for layer in objects:
        for o in layer:
            o.update()
    print('update complete')

# 월드 객체들을 모두 그리는 함수
def render():
    for layer in objects:
        for o in layer:
            o.draw()
    print("render complete")

def clear():
    for layer in objects:
        layer.clear()