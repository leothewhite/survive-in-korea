import random
from constants import *
import pygame
from property import *

pygame.font.init()

manager = ManageVariable()


# 배경(배경+보더) 움직이기
def background_manager():
    manager.bg_y -= 0.15 * manager.dt

    # idx는 보더블럭을 업데이트 하기 위한 것
    for idx in range(50):
        # 15*32 = 480, 23*32 = 736 (480 + 256)
        if 15 <= idx < 23:
            if 2 < manager.place_idx:
                # 과로
                if 3 == manager.now_place_cnt:
                    manager.guage.health -= 10

                # 다음 place set을 고름
                for i in range(3):
                    manager.place_now_set[i] = random.choice(
                        manager.places[chr(i + 97)]
                    )
                random.shuffle(manager.place_now_set)

                manager.place_idx = 0
                manager.now_place_cnt = 0

                # 글자 관련
                manager.month += 1
                manager.isText = 1
                manager.now_alpha += manager.dt

            # 오른쪽 보도블럭만 나타냄
            for t in range(2, 4):
                now = manager.borders[t][idx]
                now.update((now.rect.x, manager.bg_y + idx * 32))

            # 장소 움직임
            manager.place_now = manager.place_now_set[manager.place_idx]
            manager.place_now.update((0, manager.bg_y + SCREEN_SIZE.y))

        else:
            for t in range(4):
                now = manager.borders[t][idx]
                now.update((now.rect.x, manager.bg_y + idx * 32))

    # 640(그림 한 칸의 단위) + 256(건물의 높이)
    if manager.bg_y <= -(640 + 256):
        manager.bg_y = 0

        # 장소를 바꿔줌
        manager.place_idx += 1


def ending_manager():
    if manager.guage.stress == 100:
        return "stress"
    if manager.guage.health == 0:
        return "health"

    if 1 < manager.month:
        if manager.guage.grade < 30:
            return "grade"
        elif manager.guage.future < 50:
            return "future"
        else:
            return "happy"

    return False


# * 입력
def event_handler(event):
    # 장소에서 기다림을 끝낼 떄
    if event.type == manager.place_timer:
        manager.inPlace = False

        # 플레이어 움직임
        manager.player_x = 480
        manager.bg_y = -400
        manager.player.update((manager.player_x, SCREEN_SIZE.y / 2))

        # 안보이게 했던 플레이러를 다시 나타냄
        manager.all_sprites.add(manager.player)
        manager.all_sprites.draw(manager.SCREEN)

        # 타이머 취소
        pygame.time.set_timer(manager.place_timer, 0)

    if not manager.inPlace:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                manager.to_x -= manager.SPEED * 3 * manager.dt
                manager.down[0] = True

            if event.key == pygame.K_RIGHT:
                manager.to_x += manager.SPEED * 3 * manager.dt
                manager.down[1] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                manager.down[0] = False
            if event.key == pygame.K_RIGHT:
                manager.down[1] = False


# * a 스프라이트가 b 스프라이트 리스트에 부딪혔는가
def is_collided(a, b):
    return pygame.Rect.collidelist(a, b)


# * 플레이어와 (어떤)장소가 충돌했는가를 리턴
def list_collided(player, place_type):
    col = is_collided(player.rect, manager.places[place_type]) + 1
    if col:
        return manager.places[place_type][col - 1].name
    else:
        return False


def guage_manager(place_type, col_place):
    if place_type == "a":
        manager.guage.stress -= 5
        if col_place == "alley":
            manager.guage.health -= 5
        if col_place == "basketball":
            manager.guage.health += 5
        if 5 <= manager.stress_cnt:
            manager.guage.grade -= 5
            manager.stress_cnt = 0

    if place_type == "b":
        manager.guage.stress += 10
        manager.guage.grade += 5

    if place_type == "c":
        manager.guage.future += 10


# * 장소와의 충돌처리, 그로인한 게이지 변화 (횟수로 인한 변화도 포함)
def collide_manager():
    for key in manager.places:
        col_place = list_collided(manager.player, key)

        # 장소 입장
        if col_place:
            manager.all_sprites.remove(manager.player)  # 플레이어를 안보이게
            manager.down = [False, False]  # 키가 눌린 상태인지
            pygame.time.set_timer(manager.place_timer, 2000)  # 언제 장소에서 나올지 타이머

            manager.bg_y = -400
            manager.inPlace = True

            manager.now_place_cnt += 1

            guage_manager(key, col_place)


# * 게이지 값에 따른 중력 값 설정
def make_gravity():
    # 진로탐색/스트레스 형식이면 끌림
    if manager.place_now.type == "a" or manager.place_now.type == "c":
        manager.gravity = manager.guage.stress / 10

    # 독서실은 거부함
    elif manager.place_now.type == "b":
        manager.gravity = -(manager.guage.stress / 10)

    # 중력 적용
    if (
        manager.place_now.rect.y - manager.player.rect.height
        <= manager.player.rect.y
        <= manager.place_now.rect.y + 200
    ):
        manager.to_x -= manager.gravity


# 키를 누르는 중에 플레이어를 움직임
def move_player():
    if not manager.inPlace:
        if manager.down[0]:
            manager.to_x -= manager.SPEED * manager.dt
        if manager.down[1]:
            manager.to_x += manager.SPEED * manager.dt


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
        manager.title = FONT.render(f"{manager.month} 월", True, pygame.Color(0, 0, 0))
        manager.title.set_alpha(manager.now_alpha)
