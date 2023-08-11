import random
import os
import pygame
from property import ManageVariable, Border, Place, Guage

pygame.font.init()

manager = ManageVariable()

bg_y = 0
manager.isText = False
place_cnt = {}
place_now_set = [-1, -1, -1]
place_idx = 3
borders = [[], [], [], []]
guage = Guage()
gravity = 1
font = pygame.font.Font("./resources/fonts/NeoDunggeunmoPro-Regular.ttf", 30)
places = {"a": [], "b": [], "c": []}
place_now = -1
down = [False, False]


place_timer = pygame.USEREVENT + 0
text_timer = pygame.USEREVENT + 1


# * 이미지 불러오기
def load_images():
    global place_now
    place_path = "./resources/images/place/"
    guage_path = "./resources/images/guage/"
    manager.images = {
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

    for _, v in enumerate(manager.images["place"]):
        file_name = v[0]
        file = v[1]
        places[v[0][0]].append(Place(file, file_name[2:], (33, 480), file_name[0]))
        place_cnt[file_name[2:]] = 0
    place_now = places["a"][0]


# * 배경(배경+보더) 움직이기
def background_manager():
    global place_idx, place_now, bg_y
    manager.SCREEN.blit(manager.images["background"], (0, bg_y))
    manager.SCREEN.blit(manager.images["background"], (0, 640 + bg_y))
    for idx in range(32):
        if 12 <= idx < 16:
            if 2 < place_idx:
                for i in range(3):
                    place_now_set[i] = random.choice(places[chr(i + 97)])
                random.shuffle(place_now_set)
                manager.month += 1
                pygame.time.set_timer(text_timer, 2000)
                manager.isText = True
                place_idx = 0
            place_now = place_now_set[place_idx]
            place_now.update((31, bg_y + 480))
            place_now.draw(manager.SCREEN)
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

    bg_y -= 0.15 * manager.dt


"""
* guage 그리기, guage로 인한 게임 오버 처리
* 만약 게임 오버 될 시 True와 reason 값을 반환
"""


def guage_manager():
    manager.SCREEN.blit(manager.images["guage"]["frame"], (525, 440))
    manager.SCREEN.blit(manager.images["guage"]["frame"], (525, 400))
    manager.SCREEN.blit(manager.images["guage"]["frame"], (525, 360))
    manager.SCREEN.blit(manager.images["guage"]["frame"], (525, 320))

    for i in range(20):
        if guage.health // 5 <= i:
            break
        manager.SCREEN.blit(manager.images["guage"]["health"], (527 + 5 * i, 322))

    for i in range(20):
        if guage.future // 5 <= i:
            break
        manager.SCREEN.blit(manager.images["guage"]["future"], (527 + 5 * i, 362))

    for i in range(20):
        if guage.stress // 5 <= i:
            break
        manager.SCREEN.blit(manager.images["guage"]["stress"], (527 + 5 * i, 402))

    for i in range(20):
        if guage.grade // 5 <= i:
            break
        manager.SCREEN.blit(manager.images["guage"]["grade"], (527 + 5 * i, 442))


def ending_manager():
    if guage.stress == 100:
        return "stress"
    if guage.health == 0:
        return "health"

    if 12 < manager.month:
        if guage.grade < 30:
            return "grade"
        elif guage.future < 60:
            return "future"
        else:
            return "happy"

    return False


# * 입력
def event_handler(event):
    global bg_y, down
    if event.type == place_timer:
        manager.inPlace = False
        manager.player_x = 320
        manager.player.update((manager.player_x, 240))
        manager.all_sprites.draw(manager.SCREEN)
        pygame.time.set_timer(place_timer, 0)
        bg_y = -440
    if event.type == text_timer:
        manager.isText = False
        pygame.time.set_timer(text_timer, 0)

    if not manager.inPlace:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                manager.to_x -= manager.speed * 3 * manager.dt
                down[0] = True

            if event.key == pygame.K_RIGHT:
                manager.to_x += manager.speed * 3 * manager.dt
                down[1] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                down[0] = False
            if event.key == pygame.K_RIGHT:
                down[1] = False


# * a 스프라이트가 b 스프라이트 리스트에 부딪혔는가
def chk_collide(a, b):
    return pygame.Rect.collidelist(a, b)


# * 플레이어와 (어떤)장소가 충돌했는가를 리턴
def place_collide(player, place_type):
    col = chk_collide(player.rect, places[place_type]) + 1
    if col:
        return places[place_type][col - 1].name
    else:
        return False


# * 장소랑 보더의 충돌처리, 그로인한 게이지 변화 (횟수로 인한 변화도 포함)
def collide_manager():
    global bg_y, down
    if (
        chk_collide(manager.player.rect, borders[0]) + 1
        or chk_collide(manager.player.rect, borders[1]) + 1
    ):
        if manager.to_x < 0:
            manager.to_x = 0
    elif (
        chk_collide(manager.player.rect, borders[2]) + 1
        or chk_collide(manager.player.rect, borders[3]) + 1
    ):
        if 0 < manager.to_x:
            manager.to_x = 0

    col_place = place_collide(manager.player, "a")
    if col_place:
        manager.player_x = 140
        down = [False, False]
        pygame.time.set_timer(place_timer, 2000)
        bg_y = -300
        manager.inPlace = True
        place_cnt[col_place] += 1
        guage.stress -= 5

        if col_place == "alley":
            guage.health -= 5
        if col_place == "basketball":
            guage.health += 5
        if 5 <= place_cnt[col_place]:
            guage.grade -= 5
            place_cnt[col_place] = 0

    col_place = place_collide(manager.player, "b")
    if col_place:
        manager.player_x = 140
        down = [False, False]
        pygame.time.set_timer(place_timer, 2000)
        manager.bg_y = -300
        manager.inPlace = True
        place_cnt[col_place] += 1
        guage.stress += 5
        guage.grade += 5

        if 5 <= place_cnt[col_place]:
            guage.health -= 5
            place_cnt[col_place] = 0

    col_place = place_collide(manager.player, "c")
    if col_place:
        manager.player_x = 140
        down = [False, False]
        pygame.time.set_timer(place_timer, 2000)
        manager.bg_y = -300
        manager.inPlace = True
        place_cnt[col_place] += 1
        guage.stress -= 5
        guage.future += 5


# * 보더 이미지를 스프라이트로 만듦
def load_border():
    for i in range(32):
        now_y = i * 60
        manager.block = [
            Border(manager.images["border"], (171, now_y)),
            Border(manager.images["border"], (171, 480 + now_y)),
            Border(manager.images["border"], (456, now_y)),
            Border(manager.images["border"], (456, 480 + now_y)),
        ]
        for i in range(4):
            borders[i].append(manager.block[i])
            manager.all_sprites.add(manager.block[i])


# * 게이지 값에 따른 중력 값 설정
def make_gravity():
    global gravity
    if place_now.type == "a" or place_now.type == "c":
        gravity = guage.stress / 20
    elif place_now.type == "b":
        gravity = -(guage.stress / 40)

    if place_now.rect.y - 40 <= manager.player.rect.y <= place_now.rect.y + 200:
        manager.to_x -= gravity


def move_player():
    if not manager.inPlace:
        if down[0]:
            manager.to_x -= manager.speed * manager.dt
        if down[1]:
            manager.to_x += manager.speed * manager.dt
