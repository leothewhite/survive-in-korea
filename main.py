import pygame

from property import *
from manager import *
from scene import game_scene, menu_scene

pygame.init()

CLOCK = pygame.time.Clock()
RUNNING = True

now_scene = "MENU"

while RUNNING:
    intl.dt = CLOCK.tick(60)
    # print(now_scene)

    if now_scene == "MENU":
        RUNNING, now_scene = menu_scene()

    if now_scene == "GAME":
        RUNNING, now_scene = game_scene()

pygame.quit()
