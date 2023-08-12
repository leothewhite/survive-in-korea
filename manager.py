import random
import os
import pygame
from property import ManageVariable, Border, Place, Guage

pygame.font.init()

manager = ManageVariable()


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
now_place_cnt = 0

place_timer = pygame.USEREVENT + 1


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
    global now_place_cnt
    global place_idx, place_now
    for idx in range(32):
        if 12 <= idx < 16:
            if 2 < place_idx:
                if 3 == now_place_cnt:
                    guage.health -= 10
                for i in range(3):
                    place_now_set[i] = random.choice(places[chr(i + 97)])

                random.shuffle(place_now_set)
                place_idx = 0
                now_place_cnt = 0

                manager.month += 1
                manager.isText = 1
                manager.now_alpha += manager.dt

            place_now = place_now_set[place_idx]
            place_now.update((31, manager.bg_y + 480))

            for t in range(2, 4):
                now = borders[t][idx]
                now.update((now.rect.x, manager.bg_y + idx * 40))
        else:
            for t in range(4):
                now = borders[t][idx]
                now.update((now.rect.x, manager.bg_y + idx * 40))

    if manager.bg_y <= -480 - 160:
        place_idx += 1
        manager.bg_y = 0

    manager.bg_y -= 0.15 * manager.dt

    return place_now


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
    global down
    if event.type == place_timer:
        manager.inPlace = False
        manager.player_x = 320
        manager.player.update((manager.player_x, 240))
        manager.all_sprites.draw(manager.SCREEN)
        pygame.time.set_timer(place_timer, 0)
        manager.bg_y = -440

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
def is_collided(a, b):
    return pygame.Rect.collidelist(a, b)


# * 플레이어와 (어떤)장소가 충돌했는가를 리턴
def list_collided(player, place_type):
    col = is_collided(player.rect, places[place_type]) + 1
    if col:
        return places[place_type][col - 1].name
    else:
        return False


def guage_manager(place_type, col_place):
    if place_type == "a":
        guage.stress -= 5
        if col_place == "alley":
            guage.health -= 5
        if col_place == "basketball":
            guage.health += 5
        if 5 <= place_cnt[col_place]:
            guage.grade -= 5
            place_cnt[col_place] = 0

    if place_type == "b":
        guage.stress += 10
        guage.grade += 5
        if 5 <= place_cnt[col_place]:
            guage.health -= 5
            place_cnt[col_place] = 0

    if place_type == "c":
        guage.future += 10


# * 장소와의 충돌처리, 그로인한 게이지 변화 (횟수로 인한 변화도 포함)
def collide_manager():
    global down, now_place_cnt

    for key in places:
        col_place = list_collided(manager.player, key)

        if col_place:
            manager.player_x = 140
            down = [False, False]
            pygame.time.set_timer(place_timer, 2000)
            manager.bg_y = -300
            manager.inPlace = True
            place_cnt[col_place] += 1
            now_place_cnt += 1

            guage_manager(key, col_place)


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
        gravity = guage.stress / 10
    elif place_now.type == "b":
        gravity = -(guage.stress / 10)

    if place_now.rect.y - 40 <= manager.player.rect.y <= place_now.rect.y + 200:
        manager.to_x -= gravity


# 키를 누르는 중에 플레이어를 움직임
def move_player():
    if not manager.inPlace:
        if down[0]:
            manager.to_x -= manager.speed * manager.dt
        if down[1]:
            manager.to_x += manager.speed * manager.dt


# 텍스트 나타나고 없어지기
def text_handler():
    if manager.now_alpha != 0:
        if manager.isText == 1:
            manager.now_alpha += 1 * manager.dt
            if 1000 <= manager.now_alpha:
                manager.isText = 2
        if manager.isText == 2:
            manager.now_alpha -= 1 * manager.dt
            if manager.now_alpha <= 1:
                manager.now_alpha = 0
                manager.title = -1
                manager.isText = 0

    if manager.isText == 1 or manager.isText == 2:
        manager.title = font.render(f"{manager.month} 월", True, pygame.Color(0, 0, 0))
        manager.title.set_alpha(manager.now_alpha)


def draw_guage():
    for i in range(4):
        manager.SCREEN.blit(manager.images["guage"]["frame"], (525, 320 + 40 * i))

    guage.stress = pygame.math.clamp(guage.stress, 0, 100)
    guage.health = pygame.math.clamp(guage.health, 0, 100)
    guage.grade = pygame.math.clamp(guage.grade, 0, 100)
    guage.future = pygame.math.clamp(guage.future, 0, 100)
    for i in range(20):
        if i < guage.health // 5:
            manager.SCREEN.blit(manager.images["guage"]["health"], (527 + 5 * i, 322))
        if i < guage.future // 5:
            manager.SCREEN.blit(manager.images["guage"]["future"], (527 + 5 * i, 362))
        if i < guage.stress // 5:
            manager.SCREEN.blit(manager.images["guage"]["stress"], (527 + 5 * i, 402))
        if i < guage.grade // 5:
            manager.SCREEN.blit(manager.images["guage"]["grade"], (527 + 5 * i, 442))
