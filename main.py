import pygame
import os
import random

from myclass import *

pygame.init()


size_x, size_y = 640, 480
player_x = 320
to_x = 0
gravity = 1

place_path = "./resources/images/place/"
guage_path = "./resources/images/guage/"
images = {
    "player": pygame.image.load("./resources/images/character/player.png"),
    "border": pygame.image.load("./resources/images/background/border.png"),
    "background": pygame.image.load("./resources/images/background/background.png"),
    "place": [
        (i.split(".")[0], pygame.image.load(place_path + i))
        for i in os.listdir(place_path)
    ],
    "guage": {
        i.split(".")[0]: pygame.image.load(guage_path + i)
        for i in os.listdir(guage_path)
    },
}

print(images["guage"])

guage = Guage(20, 50, 0, 100)

down_left, down_right = False, False

all_sprites = pygame.sprite.Group()

SCREEN = pygame.display.set_mode((size_x, size_y))
CLOCK = pygame.time.Clock()
RUNNING = True

speed = 0.2

borders = [[], [], [], []]
# a: 놀기 b: 공부 c: 취미
places = {"a": [], "b": [], "c": []}
place_cnt = {}

player = Character(images["player"])

for i in range(32):
    now_y = i * 40
    block = [
        Border(images["border"], (214, now_y)),
        Border(images["border"], (214, size_y + now_y)),
        Border(images["border"], (498, now_y)),
        Border(images["border"], (498, size_y + now_y)),
    ]
    for i in range(4):
        borders[i].append(block[i])
        all_sprites.add(block[i])

for i, v in enumerate(images["place"]):
    file_name = v[0]
    file = v[1]
    places[v[0][0]].append(Place(file, file_name[2:], (33, size_y)))
    place_cnt[file_name[2:]] = 0


place_now_set = [-1, -1, -1]
place_now = places["a"][0]
place_idx = 3

player.update((player_x, 240))
all_sprites.add(player)

bg_y = 0


def move_background():
    global bg_y, place_idx, place_now

    SCREEN.blit(images["background"], (0, bg_y))
    SCREEN.blit(images["background"], (0, 640 + bg_y))
    for idx in range(32):
        if 12 <= idx <= 16:
            if 2 < place_idx:
                for i in range(3):
                    place_now_set[i] = random.choice(places[chr(i + 97)])
                random.shuffle(place_now_set)
                place_idx = 0
            place_now = place_now_set[place_idx]
            place_now.update((33, bg_y + size_y))
            place_now.draw(SCREEN)
            for t in range(2, 4):
                now = borders[t][idx]
                now.update((now.rect.x, bg_y + idx * 40))
        else:
            for t in range(4):
                now = borders[t][idx]
                now.update((now.rect.x, bg_y + idx * 40))
    if bg_y <= -size_y - 200:
        place_idx += 1
        bg_y = 0

    bg_y -= 0.15 * dt


def input_manager(event):
    global to_x, down_left, down_right
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            to_x -= speed * 3 * dt
            down_left = True

        if event.key == pygame.K_RIGHT:
            to_x += speed * 3 * dt
            down_right = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            down_left = False
        if event.key == pygame.K_RIGHT:
            down_right = False


def chk_collide(a, b):
    return pygame.Rect.collidelist(a, b)


def place_collide(player, place_type):
    col = chk_collide(player.rect, places[place_type]) + 1
    if col:
        return places[place_type][col - 1].name
    else:
        return False


while RUNNING:
    dt = CLOCK.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        input_manager(event)
    if down_left:
        to_x -= speed * dt
    if down_right:
        to_x += speed * dt

    move_background()

    if place_now.rect.y - 40 <= player.rect.y <= place_now.rect.y + 200:
        to_x -= gravity

    if (
        chk_collide(player.rect, borders[0]) + 1
        or chk_collide(player.rect, borders[1]) + 1
    ):
        if to_x < 0:
            to_x = 0
    elif (
        chk_collide(player.rect, borders[2]) + 1
        or chk_collide(player.rect, borders[3]) + 1
    ):
        if 0 < to_x:
            to_x = 0

    # 스트레스 풀기
    col_place = place_collide(player, "a")
    if col_place:
        guage.stress -= 5
        place_cnt[col_place] += 1
        if col_place == "alley":
            guage.health -= 5
        if col_place == "basketball":
            guage.health += 5
        if 3 <= place_cnt[col_place]:
            guage.grade -= 5

    col_place = place_collide(player, "b")
    if col_place:
        guage.stress += 5
        guage.grade += 5

    col_place = place_collide(player, "c")
    if col_place:
        guage.stress -= 5
        guage.future += 5

    player_x += to_x
    player.update((player_x, 240))
    all_sprites.draw(SCREEN)
    to_x = 0

    pygame.display.update()


pygame.quit()
