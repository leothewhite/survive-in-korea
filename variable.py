from property import *
import pygame
from constants import *


def initialize():
    manager = ManageVariable()

    manager.all_sprites = pygame.sprite.Group()
    manager.all_sprites_menu = pygame.sprite.Group()

    manager.place_now_set = [-1, -1, -1]
    manager.place_idx = 3
    manager.place_timer = pygame.USEREVENT + 1
    manager.inPlace = False
    manager.place_now = PLACES["a"][0]
    manager.now_place_cnt = 0

    manager.borders = [[], [], [], []]

    for i in range(50):
        now_y = i * BORDER_SIZE[1]

        block = [
            Border(BORDER_IMAGE, (305, now_y)),
            Border(BORDER_IMAGE, (305, BG_SIZE[1] + now_y)),
            Border(BORDER_IMAGE, (625, now_y)),
            Border(BORDER_IMAGE, (625, BG_SIZE[1] + now_y)),
        ]
        for i in range(4):
            manager.borders[i].append(block[i])
            manager.all_sprites.add(block[i])

    manager.bg_y = 0

    manager.isText = 0
    manager.title = -1
    manager.now_alpha = 0
    manager.month = -1

    manager.player_x = 480
    manager.player = Character()
    manager.to_x = 0
    manager.down = [False, False]

    manager.stress_cnt = 0
    manager.guage = Guage()

    manager.gravity = 1

    manager.SCREEN = pygame.display.set_mode((640, 480))

    manager.player.update((manager.player_x, 240))
    manager.all_sprites.add(manager.player)
