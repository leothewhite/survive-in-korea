import random
import os
import pygame
from property import *

pygame.font.init()

manager = ManageVariable()


isText = 0
now_alpha = 0
month = 0
stress_cnt = 0
place_now_set = [-1, -1, -1]
place_idx = 3
borders = [[], [], [], []]
guage = Guage()
gravity = 1
font = pygame.font.Font("./resources/fonts/NeoDunggeunmoPro-Regular.ttf", 30)
places = {"a": [], "b": [], "c": []}
# place_now = -1
down = [False, False]
now_place_cnt = 0

border_size = Size(16, 32)
screen_size = Size(640, 480)
background_size = Size(640, 640)

border_cnt = 50

place_timer = pygame.USEREVENT + 1


# 배경(배경+보더) 움직이기
def background_manager():
    global now_place_cnt
    global place_idx, month, now_alpha, isText
    manager.bg_y -= 0.15 * manager.dt

    # idx는 보더블럭을 업데이트 하기 위한 것
    for idx in range(border_cnt):
        # 15*32 = 480, 23*32 = 736 (480 + 256)
        if 15 <= idx < 23:
            if 2 < place_idx:
                # 과로
                if 3 == now_place_cnt:
                    guage.health -= 10

                # 다음 place set을 고름
                for i in range(3):
                    place_now_set[i] = random.choice(places[chr(i + 97)])
                random.shuffle(place_now_set)

                place_idx = 0
                now_place_cnt = 0

                # 글자 관련
                month += 1
                isText = 1
                now_alpha += manager.dt

            # 오른쪽 보도블럭만 나타냄
            for t in range(2, 4):
                now = borders[t][idx]
                now.update((now.rect.x, manager.bg_y + idx * 32))

            # 장소 움직임
            manager.place_now = place_now_set[place_idx]
            manager.place_now.update((0, manager.bg_y + screen_size.y))

        else:
            for t in range(4):
                now = borders[t][idx]
                now.update((now.rect.x, manager.bg_y + idx * 32))

    # 640(그림 한 칸의 단위) + 256(건물의 높이)
    if manager.bg_y <= -(640 + 256):
        manager.bg_y = 0

        # 장소를 바꿔줌
        place_idx += 1


def ending_manager():
    if guage.stress == 100:
        return "stress"
    if guage.health == 0:
        return "health"

    if 1 < month:
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
    # 장소에서 기다림을 끝낼 떄
    if event.type == place_timer:
        manager.inPlace = False

        # 플레이어 움직임
        manager.player_x = 480
        manager.bg_y = -400
        manager.player.update((manager.player_x, screen_size.y / 2))

        # 안보이게 했던 플레이러를 다시 나타냄
        manager.all_sprites.add(manager.player)
        manager.all_sprites.draw(manager.SCREEN)

        # 타이머 취소
        pygame.time.set_timer(place_timer, 0)

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
    global stress_cnt

    if place_type == "a":
        guage.stress -= 5
        if col_place == "alley":
            guage.health -= 5
        if col_place == "basketball":
            guage.health += 5
        if 5 <= stress_cnt:
            guage.grade -= 5
            stress_cnt = 0

    if place_type == "b":
        guage.stress += 10
        guage.grade += 5

    if place_type == "c":
        guage.future += 10


# * 장소와의 충돌처리, 그로인한 게이지 변화 (횟수로 인한 변화도 포함)
def collide_manager():
    global down, now_place_cnt

    for key in places:
        col_place = list_collided(manager.player, key)

        # 장소 입장
        if col_place:
            manager.all_sprites.remove(manager.player)  # 플레이어를 안보이게
            down = [False, False]  # 키가 눌린 상태인지
            pygame.time.set_timer(place_timer, 2000)  # 언제 장소에서 나올지 타이머

            manager.bg_y = -400
            manager.inPlace = True

            now_place_cnt += 1

            guage_manager(key, col_place)


# * 게이지 값에 따른 중력 값 설정
def make_gravity():
    global gravity

    # 진로탐색/스트레스 형식이면 끌림
    if manager.place_now.type == "a" or manager.place_now.type == "c":
        gravity = guage.stress / 10

    # 독서실은 거부함
    elif manager.place_now.type == "b":
        gravity = -(guage.stress / 10)

    # 중력 적용
    if (
        manager.place_now.rect.y - 40
        <= manager.player.rect.y
        <= manager.place_now.rect.y + 200
    ):
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
    global isText, now_alpha
    print(isText)
    if now_alpha != 0:
        if isText == 1:
            now_alpha += 1 * manager.dt
            if 1000 <= now_alpha:
                isText = 2
        if isText == 2:
            now_alpha -= 1 * manager.dt
            if now_alpha <= 1:
                now_alpha = 0
                manager.title = -1
                isText = 0

    if isText == 1 or isText == 2:
        manager.title = font.render(f"{month} 월", True, pygame.Color(0, 0, 0))
        manager.title.set_alpha(now_alpha)
