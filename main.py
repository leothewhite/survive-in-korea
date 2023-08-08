import pygame

from property import *
from manager import *
from scene import game_scene, menu_scene, over_scene

pygame.init()

CLOCK = pygame.time.Clock()
RUNNING = True

now_scene = "MENU"

while RUNNING:
    intl.dt = CLOCK.tick(60)

    if now_scene == "MENU":
        RUNNING, now_scene = menu_scene()

    if now_scene == "GAME":
        # TODO: 장소에 들어갔을때 2초동안 있고 바로 밑으로 이동
        RUNNING, now_scene = game_scene()

    if now_scene[:4] == "OVER":
        # TODO: 이유마다 다른 game over 씬
        RUNNING, now_scene = over_scene(now_scene.split()[1])

pygame.quit()
