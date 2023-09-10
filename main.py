import pygame
from variable import initialize

initialize()  # 싱글턴 클래스의 변수들을 초기화해줌

from property import *
from manager import *
from scene import *

pygame.init()

CLOCK = pygame.time.Clock()

RUNNING = True  # 실행 여부

now_scene = "MENU"  # 현재 씬을 씬 함수로부터 리턴 받음

while RUNNING:
    manager.dt = CLOCK.tick(60)  # 60프레임으로 설정

    # 현재 씬에 맞는 씬을 표시하는 함수를 실행
    if now_scene == "MENU":
        # 다음 루프때 실행 여부와 다음 씬을 리턴 받음
        RUNNING, now_scene = menu_scene()

    if now_scene == "GAME":
        RUNNING, now_scene = game_scene()

    if now_scene[:4] == "OVER":
        RUNNING, now_scene = over_scene(
            now_scene.split()[1]
        )  # 공백 기준으로 분할 (OVER stress -> ["OVER", "stress"])

    if now_scene == "TUTORIAL":
        RUNNING, now_scene = tutorial_scene()

pygame.quit()  # while 문이 끝날 시 창 종료
