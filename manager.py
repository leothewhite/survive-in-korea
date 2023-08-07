import random
import os
import pygame
from property import ManageVariable, Border, Place, Guage

intl = ManageVariable()


def make_variable():
    intl.size_x, intl.size_y = 640, 480
    intl.player_x = 320
    intl.to_x = 0
    intl.gravity = 1
    intl.guage = Guage()
    intl.down_left, intl.down_right = False, False
    intl.all_sprites = pygame.sprite.Group()
    intl.SCREEN = pygame.display.set_mode((intl.size_x, intl.size_y))
    intl.CLOCK = pygame.time.Clock()
    intl.RUNNING = True
    intl.speed = 0.2
    intl.borders = [[], [], [], []]
    intl.places = {"a": [], "b": [], "c": []}
    intl.place_cnt = {}
    intl.bg_y = 0
    intl.place_now_set = [-1, -1, -1]
    intl.place_idx = 3


def load_images():
    intl.place_path = "./resources/images/place/"
    intl.guage_path = "./resources/images/guage/"
    intl.images = {
        "player": pygame.image.load("./resources/images/character/player.png"),
        "border": pygame.image.load("./resources/images/background/border.png"),
        "background": pygame.image.load("./resources/images/background/background.png"),
        "place": [
            (i.split(".")[0], pygame.image.load(intl.place_path + i))
            for i in os.listdir(intl.place_path)
        ],
        "guage": {
            i.split(".")[0]: pygame.image.load(intl.guage_path + i)
            for i in os.listdir(intl.guage_path)
            if i != ".DS_Store"
        },
    }

    for _, v in enumerate(intl.images["place"]):
        file_name = v[0]
        file = v[1]
        intl.places[v[0][0]].append(Place(file, file_name[2:], (33, intl.size_y)))
        intl.place_cnt[file_name[2:]] = 0


def background_manager():
    intl.SCREEN.blit(intl.images["background"], (0, intl.bg_y))
    intl.SCREEN.blit(intl.images["background"], (0, 640 + intl.bg_y))
    for idx in range(32):
        if 12 <= idx < 16:
            if 2 < intl.place_idx:
                for i in range(3):
                    intl.place_now_set[i] = random.choice(intl.places[chr(i + 97)])
                random.shuffle(intl.place_now_set)
                intl.place_idx = 0
            intl.place_now = intl.place_now_set[intl.place_idx]
            intl.place_now.update((31, intl.bg_y + intl.size_y))
            intl.place_now.draw(intl.SCREEN)
            for t in range(2, 4):
                now = intl.borders[t][idx]
                now.update((now.rect.x, intl.bg_y + idx * 40))
        else:
            for t in range(4):
                now = intl.borders[t][idx]
                now.update((now.rect.x, intl.bg_y + idx * 40))
    if intl.bg_y <= -intl.size_y - 160:
        intl.place_idx += 1
        intl.bg_y = 0

    intl.bg_y -= 0.15 * intl.dt


def guage_manager():
    intl.SCREEN.blit(intl.images["guage"]["frame"], (525, 440))
    intl.SCREEN.blit(intl.images["guage"]["frame"], (525, 400))
    intl.SCREEN.blit(intl.images["guage"]["frame"], (525, 360))
    intl.SCREEN.blit(intl.images["guage"]["frame"], (525, 320))

    for i in range(20):
        if intl.guage.health // 5 <= i:
            break
        intl.SCREEN.blit(intl.images["guage"]["health"], (527 + 5 * i, 322))

    for i in range(20):
        if intl.guage.future // 5 <= i:
            break
        intl.SCREEN.blit(intl.images["guage"]["future"], (527 + 5 * i, 362))

    for i in range(20):
        if intl.guage.stress // 5 <= i:
            break
        intl.SCREEN.blit(intl.images["guage"]["stress"], (527 + 5 * i, 402))

    for i in range(20):
        if intl.guage.grade // 5 <= i:
            break
        intl.SCREEN.blit(intl.images["guage"]["grade"], (527 + 5 * i, 442))


def input_manager(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            intl.to_x -= intl.speed * 3 * intl.dt
            intl.down_left = True

        if event.key == pygame.K_RIGHT:
            intl.to_x += intl.speed * 3 * intl.dt
            intl.down_right = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            intl.down_left = False
        if event.key == pygame.K_RIGHT:
            intl.down_right = False


def chk_collide(a, b):
    return pygame.Rect.collidelist(a, b)


def place_collide(player, place_type):
    col = chk_collide(player.rect, intl.places[place_type]) + 1
    if col:
        return intl.places[place_type][col - 1].name
    else:
        return False


def collide_manager():
    if (
        chk_collide(intl.player.rect, intl.borders[0]) + 1
        or chk_collide(intl.player.rect, intl.borders[1]) + 1
    ):
        if intl.to_x < 0:
            intl.to_x = 0
    elif (
        chk_collide(intl.player.rect, intl.borders[2]) + 1
        or chk_collide(intl.player.rect, intl.borders[3]) + 1
    ):
        if 0 < intl.to_x:
            intl.to_x = 0

    # # 스트레스 풀기
    col_place = place_collide(intl.player, "a")
    if col_place:
        intl.guage.stress -= 5
        intl.place_cnt[col_place] += 1
        if col_place == "alley":
            intl.guage.health -= 5
        if col_place == "basketball":
            intl.guage.health += 5
        if 3 <= intl.place_cnt[col_place]:
            intl.guage.grade -= 5

        intl.player_x = 320

    col_place = place_collide(intl.player, "b")
    if col_place:
        intl.guage.stress += 5
        intl.guage.grade += 5
        intl.player_x = 320

    col_place = place_collide(intl.player, "c")
    if col_place:
        intl.guage.stress -= 5
        intl.guage.future += 5
        intl.player_x = 320


def load_border():
    for i in range(32):
        now_y = i * 60
        intl.block = [
            Border(intl.images["border"], (171, now_y)),
            Border(intl.images["border"], (171, intl.size_y + now_y)),
            Border(intl.images["border"], (456, now_y)),
            Border(intl.images["border"], (456, intl.size_y + now_y)),
        ]
        for i in range(4):
            intl.borders[i].append(intl.block[i])
            intl.all_sprites.add(intl.block[i])
