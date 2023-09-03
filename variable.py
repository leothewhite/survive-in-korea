from property import ManageVariable, Guage, Character, Place, Border
import pygame
from constants import *


def initialize():
    manager = ManageVariable()

    manager.isText = 0
    manager.now_alpha = 0
    manager.month = 0
    manager.stress_cnt = 0
    manager.place_now_set = [-1, -1, -1]
    manager.place_idx = 3
    manager.borders = [[], [], [], []]
    manager.guage = Guage()
    manager.gravity = 1
    manager.places = {"a": [], "b": [], "c": []}
    manager.down = [False, False]
    manager.now_place_cnt = 0

    manager.place_timer = pygame.USEREVENT + 1

    manager.player_x = 480
    manager.to_x = 0
    manager.all_sprites = pygame.sprite.Group()
    manager.all_sprites_menu = pygame.sprite.Group()

    manager.SCREEN = pygame.display.set_mode((640, 480))
    manager.SPEED = 0.2
    manager.inPlace = False
    manager.title = -1
    manager.bg_y = 0
    manager.player = Character()

    # place_image에 이미지들을 스프라이트로 바꿔 places 딕셔네리에 넣음
    for _, v in enumerate(PLACE_IMAGE):
        file_name = v[0]
        file = v[1]
        manager.places[v[0][0]].append(
            Place(file, file_name[2:], (0, SCREEN_SIZE.y), file_name[0])
        )
    manager.place_now = manager.places["a"][0]

    # 보더 이미지를 가지고 borders배열에 스프라이트로 저장
    for i in range(50):
        now_y = i * BORDER_SIZE.y

        block = [
            # 두세트를 만듦
            Border(BORDER_IMAGE, (305, now_y)),
            Border(BORDER_IMAGE, (305, BG_SIZE.y + now_y)),
            Border(BORDER_IMAGE, (625, now_y)),
            Border(BORDER_IMAGE, (625, BG_SIZE.y + now_y)),
        ]
        for i in range(4):
            manager.borders[i].append(block[i])
            manager.all_sprites.add(block[i])

    manager.player.update((manager.player_x, 240))
    manager.all_sprites.add(manager.player)
