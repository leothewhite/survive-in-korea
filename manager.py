import random
from constants import *
import pygame
from property import ManageVariable

pygame.font.init()

manager = ManageVariable()


def background_manager():
    manager.bg_y -= 0.15 * manager.dt  # 배경 사진의 y 좌표

    for idx in range(50):
        # 장소 있는곳 뚫어놓기
        if 15 <= idx < 23:
            if 2 < manager.place_idx:  # 만약 한 place set이 끝났다면
                # 과로 시 건강 - 10
                if 3 == manager.now_place_cnt:
                    manager.guage.health -= 10

                # 새로 place set를 뽑아줌
                for i in range(3):
                    manager.place_now_set[i] = random.choice(PLACES[chr(i + 97)])
                random.shuffle(manager.place_now_set)

                manager.place_idx = 0
                manager.now_place_cnt = 0

                manager.month += 1

                # 한 학기가 지난 것이므로 글자 표시 시켜줌
                manager.isText = 1
                manager.now_alpha += manager.dt

            # 보더 움직이기
            for t in range(2, 4):
                now = manager.borders[t][idx]
                now.update((now.rect.x, manager.bg_y + idx * 32))

            manager.place_now = manager.place_now_set[manager.place_idx]
            manager.place_now.update((0, manager.bg_y + SCREEN_SIZE[1]))

        else:
            for t in range(4):
                now = manager.borders[t][idx]
                now.update((now.rect.x, manager.bg_y + idx * 32))

    # 배경 끝까지 가면 처음부터 시작
    if manager.bg_y <= -(640 + 256):
        manager.bg_y = 0

        manager.place_idx += 1


def ending_manager():
    if manager.guage.stress == 100:
        return "stress"
    if manager.guage.health == 0:
        return "health"

    if 5 < manager.month:
        if manager.guage.grade < 30:
            return "grade"
        elif manager.guage.future < 50:
            return "future"
        else:
            return "happy"

    return False


def event_handler(event):
    if event.type == manager.place_timer:  # 장소에 2초동안 들어가 있었다면
        manager.inPlace = False

        manager.player_x = 480
        manager.bg_y = -400
        manager.player.update((manager.player_x, SCREEN_SIZE[1] / 2))

        manager.all_sprites.add(manager.player)
        manager.all_sprites.draw(manager.SCREEN)

        pygame.time.set_timer(manager.place_timer, 0)

    if not manager.inPlace:  # 플레이어가 장소에 들어가 있지 않다면 움직이게 함
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                manager.to_x -= SPEED * 3 * manager.dt
                manager.down[0] = True

            if event.key == pygame.K_RIGHT:
                manager.to_x += SPEED * 3 * manager.dt
                manager.down[1] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                manager.down[0] = False
            if event.key == pygame.K_RIGHT:
                manager.down[1] = False

def guage_manager(place_type, col_place):
    if place_type == "a": # 스트레스 해소 장소라면
        manager.guage.stress -= 5
        if col_place == "alley":
            manager.guage.health -= 5
        if col_place == "basketball":
            manager.guage.health += 5
        if 5 <= manager.stress_cnt:
            manager.guage.grade -= 5
            manager.stress_cnt = 0

    if place_type == "b": # 공부하는 장소라면
        manager.guage.stress += 10
        manager.guage.grade += 5

    if place_type == "c": # 진로탐색 장소라면
        manager.guage.future += 10


def collide_manager():
    for key in PLACES:  # PLACES {"a": [...], "b": [...], "c": [...]}
        # 플레이어와
        col = pygame.Rect.collidelist(manager.player.rect, PLACES[key]) + 1

        if col:
            manager.all_sprites.remove(manager.player)  # 플레이어 안보여야해서
            manager.down = [False, False]
            pygame.time.set_timer(manager.place_timer, 2000)  # 2초 후 장소에서 나와야 하기 때문에

            manager.bg_y = -400
            manager.inPlace = True

            manager.now_place_cnt += 1

            guage_manager(key, PLACES[key][col - 1].name)  # 게이지 이동


def make_gravity():
    # 이끌림 값 조정
    if manager.place_now.type == "a" or manager.place_now.type == "c":
        manager.gravity = manager.guage.stress / 10

    elif manager.place_now.type == "b":
        manager.gravity = -(manager.guage.stress / 10)

    if (
        manager.place_now.rect.y - manager.player.rect.height
        <= manager.player.rect.y
        <= manager.place_now.rect.y + 200
    ):  # 이끌림 적용
        manager.to_x -= manager.gravity


def move_player():
    if manager.down[0]:
        manager.to_x -= SPEED * manager.dt
    if manager.down[1]:
        manager.to_x += SPEED * manager.dt


def text_handler():
    if manager.isText == 1:  # 페이드 인
        manager.now_alpha += 1 * manager.dt
        if 1000 <= manager.now_alpha:
            manager.isText = 2
    if manager.isText == 2:  # 페이드 아웃
        manager.now_alpha -= 1 * manager.dt
        if manager.now_alpha <= 1:
            manager.now_alpha = 0
            manager.title = -1
            manager.isText = 0

    if manager.isText == 1 or manager.isText == 2:
        manager.title = FONT.render(
            SEMESTER[manager.month], True, pygame.Color(0, 0, 0)
        )
        manager.title.set_alpha(manager.now_alpha)
