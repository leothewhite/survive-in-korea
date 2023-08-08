import pygame

from property import *
from manager import *
from scene import game_scene, menu_scene

pygame.init()

CLOCK = pygame.time.Clock()
RUNNING = True

now_scene = "GAME"

while RUNNING:
    intl.dt = CLOCK.tick(60)
    print(now_scene)

    if now_scene == "MENU":
        intl.SCREEN.fill((255, 255, 0))
        RUNNING, now_scene = menu_scene()

    if now_scene == "GAME":
        RUNNING, now_scene = game_scene()

pygame.quit()
