from property import Border, Character, Guage, ManageVariable
import pygame
from constants import *


def initialize():
    manager = ManageVariable()  # 전역변수 관리 싱글턴 클래스

    manager.all_sprites = pygame.sprite.Group()  # game scene의 스프라이트 그룹
    manager.all_sprites_menu = pygame.sprite.Group()  # menu scene의 스프라이트 그룹

    manager.place_now_set = [-1, -1, -1]  # 한 학기의 장소 리스트
    manager.place_idx = 3  # 지금 몇 번째 장소인지 (처음 시작할때 0으로 초기화 될꺼임)
    manager.place_timer = pygame.USEREVENT + 1  # 장소 입장 시 잠시 기다렸다가 게임 재개
    manager.inPlace = False  # 현재 장소에 들어가 있는지
    manager.place_now = PLACES["a"][0]  # 현재 표시되는 장소
    manager.now_place_cnt = 0  # 이번 학기에 몇군데의 장소를 들렀는지

    manager.borders = [[], [], [], []]  # 양 옆의 회색 보더 저장 (위쪽 좌우, 아랫쪽 좌우)

    # 보더 배열 저장
    for i in range(50):
        now_y = i * BORDER_SIZE[1]

        # 위쪽의 왼쪽, 아랫쪽의 왼쪽, 위쪽의 오른쪽, 아랫쪽의 왼쪽
        block = [
            Border(BORDER_IMAGE, (305, now_y)),
            Border(BORDER_IMAGE, (305, BG_SIZE[1] + now_y)),
            Border(BORDER_IMAGE, (625, now_y)),
            Border(BORDER_IMAGE, (625, BG_SIZE[1] + now_y)),
        ]

        # borders[0]에는 위쪽의 왼쪽 보더만 저장해놓고 ...
        for i in range(4):
            manager.borders[i].append(block[i])
            manager.all_sprites.add(block[i])

    manager.bg_y = 0  # 배경 사진을 (0, bg_y)에 두고, bg_y에 일정한 숫자를 뺴서 배경이 뒤로 움직이게 함

    # 학기를 표시하는 글자의 존재여부
    # 0: 없음 1: 페이드인 2: 페이드아웃
    manager.isText = 0
    manager.title = -1  # 글자가 표시될때는 글자 객체, 아닐때는 -1
    manager.now_alpha = 0  # 글자의 알파값. 더하고 빼서 페이드인/아웃 구현
    manager.month = -1  # 지금이 언제인지

    manager.player = Character()  # 플레이어 스프라이트
    manager.player_x = 480  # 플레이어의 x좌표
    manager.to_x = 0  # 플레이어를 움직일떄는 to_x을 더하고 빼고, 마지막에 player_x에 더한다
    manager.down = [False, False]  # 왼쪽, 오른쪽 방향키가 눌러진 상태인지

    manager.stress_cnt = 0  # 스트레스 해소 장소 방문 횟수
    manager.guage = Guage()  # 게이지를 저장하는 객체

    manager.gravity = 1  # 중력값(가변적)

    manager.SCREEN = pygame.display.set_mode((640, 480))  # 화면

    manager.player.update((manager.player_x, 240))
    manager.all_sprites.add(manager.player)

    manager.isStory = False
