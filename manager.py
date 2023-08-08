import random
import os
import pygame
from property import ManageVariable, Border, Place, Guage

intl = ManageVariable()

bg_y = 0
place_cnt = {}
place_now_set = [-1, -1, -1]
place_idx = 3
borders = [[], [], [], []]
guage = Guage()
gravity = 1


def load_images():
    place_path = "./resources/images/place/"
    guage_path = "./resources/images/guage/"
    intl.images = {
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
            if i != ".DS_Store"
        },
    }

    for _, v in enumerate(intl.images["place"]):
        file_name = v[0]
        file = v[1]
        intl.places[v[0][0]].append(Place(file, file_name[2:], (33, 480), file_name[0]))
        place_cnt[file_name[2:]] = 0


def background_manager():
    global bg_y, place_idx
    intl.SCREEN.blit(intl.images["background"], (0, bg_y))
    intl.SCREEN.blit(intl.images["background"], (0, 640 + bg_y))
    for idx in range(32):
        if 12 <= idx < 16:
            if 2 < place_idx:
                for i in range(3):
                    place_now_set[i] = random.choice(intl.places[chr(i + 97)])
                random.shuffle(place_now_set)
                place_idx = 0
            intl.place_now = place_now_set[place_idx]
            intl.place_now.update((31, bg_y + 480))
            intl.place_now.draw(intl.SCREEN)
            for t in range(2, 4):
                now = borders[t][idx]
                now.update((now.rect.x, bg_y + idx * 40))
        else:
            for t in range(4):
                now = borders[t][idx]
                now.update((now.rect.x, bg_y + idx * 40))
    if bg_y <= -480 - 160:
        place_idx += 1
        bg_y = 0

    bg_y -= 0.15 * intl.dt


def guage_manager():
    intl.SCREEN.blit(intl.images["guage"]["frame"], (525, 440))
    intl.SCREEN.blit(intl.images["guage"]["frame"], (525, 400))
    intl.SCREEN.blit(intl.images["guage"]["frame"], (525, 360))
    intl.SCREEN.blit(intl.images["guage"]["frame"], (525, 320))

    for i in range(20):
        if guage.health // 5 <= i:
            break
        intl.SCREEN.blit(intl.images["guage"]["health"], (527 + 5 * i, 322))

    for i in range(20):
        if guage.future // 5 <= i:
            break
        intl.SCREEN.blit(intl.images["guage"]["future"], (527 + 5 * i, 362))

    for i in range(20):
        if guage.stress // 5 <= i:
            break
        intl.SCREEN.blit(intl.images["guage"]["stress"], (527 + 5 * i, 402))

    for i in range(20):
        if guage.grade // 5 <= i:
            break
        intl.SCREEN.blit(intl.images["guage"]["grade"], (527 + 5 * i, 442))

    if guage.stress == 100:
        return True, "stress"
    if guage.health == 0:
        return True, "health"

    return False, "ok"


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

    return False


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
        chk_collide(intl.player.rect, borders[0]) + 1
        or chk_collide(intl.player.rect, borders[1]) + 1
    ):
        if intl.to_x < 0:
            intl.to_x = 0
    elif (
        chk_collide(intl.player.rect, borders[2]) + 1
        or chk_collide(intl.player.rect, borders[3]) + 1
    ):
        if 0 < intl.to_x:
            intl.to_x = 0

    # 스트레스 풀기
    col_place = place_collide(intl.player, "a")
    if col_place:
        place_cnt[col_place] += 1  # 장소 카운트
        guage.sub_stress(5)  # 스트레스 5 감소

        if col_place == "alley":  # 불건전 건강 5 감소
            guage.sub_health(5)
        if col_place == "basketball":  # 운동 건강 5 추가
            guage.add_health(5)
        if 5 <= place_cnt[col_place]:  # 5번 이상 들를시 성적 5 줄임
            guage.sub_grade(5)
            place_cnt[col_place] = 0

        intl.player_x = 320

    # 공부
    col_place = place_collide(intl.player, "b")
    if col_place:
        place_cnt[col_place] += 1
        guage.add_stress(5)
        guage.add_grade(5)

        if 5 <= place_cnt[col_place]:
            guage.sub_health(5)
            place_cnt[col_place] = 0

        intl.player_x = 320

    # 진로
    col_place = place_collide(intl.player, "c")
    if col_place:
        place_cnt[col_place] += 1
        guage.sub_stress(5)
        guage.add_future(5)
        intl.player_x = 320


def load_border():
    for i in range(32):
        now_y = i * 60
        intl.block = [
            Border(intl.images["border"], (171, now_y)),
            Border(intl.images["border"], (171, 480 + now_y)),
            Border(intl.images["border"], (456, now_y)),
            Border(intl.images["border"], (456, 480 + now_y)),
        ]
        for i in range(4):
            borders[i].append(intl.block[i])
            intl.all_sprites.add(intl.block[i])


def make_gravity():
    global gravity
    if intl.place_now.type == "a" or intl.place_now.type == "c":
        gravity = guage.stress / 20
    elif intl.place_now.type == "b":
        gravity = -(guage.stress / 40)

    if intl.place_now.rect.y - 40 <= intl.player.rect.y <= intl.place_now.rect.y + 200:
        intl.to_x -= gravity
