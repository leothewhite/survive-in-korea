from property import ManageVariable

from manager import (
    event_handler,
    move_player,
    text_handler,
    make_gravity,
    collide_manager,
    background_manager,
    ending_manager,
)
from constants import *

from variable import initialize

manager = ManageVariable()


manager.player.update((manager.player_x, 240))
manager.all_sprites.add(manager.player)


def game_scene():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                manager.isStory = True
        if manager.isStory:
            event_handler(event)

    if not manager.isStory:
        manager.SCREEN.blit(pygame.image.load("./resources/images/background/story.png"), (0, 0))
    if manager.isStory:
        manager.SCREEN.blit(BG_IMAGE, (0, manager.bg_y))
        manager.SCREEN.blit(BG_IMAGE, (0, manager.bg_y + 896))

        text_handler()

        if not manager.inPlace:
            move_player() # 키 눌린 상태에서의 플레이어 이동
            make_gravity() # 게이지 값에 따라 끌어당김 변화
            collide_manager() # 장소와 충돌 시 처리
            background_manager() # 배경 관할

        reason = ending_manager() # 현재 상태 파악 후, 게임 오버 시 이유 리턴

        if reason:
            return True, "OVER" + f" {reason}" # 게임 종료 시 씬 전환



        ############### 플레이어 가두기, 이미지 화면에 표시 ###############
        manager.player_x += manager.to_x

        manager.place_now.draw(manager.SCREEN)

        if not -(200 + 256) <= manager.bg_y <= -200:
            manager.player_x = pygame.math.clamp(
                manager.player_x,
                320,
                SCREEN_SIZE[0] - manager.player.rect.width - BORDER_SIZE[0],
            )
        else:
            manager.player_x = pygame.math.clamp(manager.player_x, 0, 580)

        manager.player.update((manager.player_x, 240))
        manager.all_sprites.draw(manager.SCREEN)

        if manager.title != -1:
            manager.SCREEN.blit(manager.title, (40, 40))

        guages = [
            manager.guage.stress,
            manager.guage.health,
            manager.guage.grade,
            manager.guage.future,
        ]
        guage_name = ["stress", "health", "grade", "future"]

        for i in range(4):
            guages[i] = pygame.math.clamp(guages[i], 0, 100)
            for j in range(20):
                if j < guages[i] // 5:
                    manager.SCREEN.blit(
                        GUAGE_IMAGE[guage_name[i]], (527 + (5 * j), 322 + (40 * i))
                    )
            manager.SCREEN.blit(
                GUAGE_IMAGE["frame_" + guage_name[i]], (525, 320 + 40 * i)
            )
        manager.to_x = 0
    pygame.display.update()

    return True, "GAME"



select_idx = 0 # 어느 버튼이 선택되어 있는지 저장

def menu_scene():
    global select_idx

    MENU_BACKGROUND.update()
    manager.all_sprites_menu.add(MENU_BACKGROUND)
    
    event_list = pygame.event.get() # 시간 단축 위해 미리 이벤트 목록을 구해놓는다
    for event in event_list:
        if event.type == pygame.QUIT:
            return False, "END"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: # 위쪽 방향키를 누르면 인덱스 - 1
                select_idx -= 1

                if select_idx < 0:
                    select_idx = 0
            if event.key == pygame.K_DOWN: # 아래쪽 방향키를 누르면 인덱스 + 1
                select_idx += 1

                if 2 < select_idx:
                    select_idx = 2

            # 엔터/스페이스로 선택을 했을떄 선택한 버튼에 따라 씬을 바꿈
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if select_idx == 0:
                    initialize()
                    return True, "GAME"
                elif select_idx == 1:
                    return False, "END"
                elif select_idx == 2:
                    return True, "TUTORIAL"


    # 그리기
    manager.all_sprites_menu.draw(manager.SCREEN)
    manager.SCREEN.blit(pygame.image.load("./resources/images/menu/title.png"), (80, 40))
    manager.SCREEN.blit(pygame.image.load("./resources/images/menu/game_start.png"), (200, 200 + 60 * 0))
    manager.SCREEN.blit(pygame.image.load("./resources/images/menu/game_exit.png"), (200, 200 + 60 * 1))
    manager.SCREEN.blit(pygame.image.load("./resources/images/menu/game_tutorial.png"), (200, 200 + 60 * 2))
    manager.SCREEN.blit(pygame.image.load("./resources/images/menu/select.png"), (196, 196 + 60 * select_idx))
    pygame.display.update()

    return True, "MENU"


def over_scene(reason):
    all_sprites = pygame.sprite.Group()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE: # 엔터/스페이스로 메뉴로 돌아가기
                return True, "MENU"

    manager.SCREEN.blit(OVER[reason], (0, 0)) # 실행될때 받은 reason값에 맞는 엔딩 화면 띄우기
    all_sprites.draw(manager.SCREEN)
    pygame.display.update()

    return True, "OVER " + reason


img_idx = 0

clicked = 0


def tutorial_scene():
    global clicked, img_idx
    all_sprites = pygame.sprite.Group()

    if clicked == 0: # 처음 키보드 튜토리얼 화면
        img_idx += 1
        manager.SCREEN.blit(TUTORIAL_KEYBOARD[img_idx % 60], (0, 0))
    elif clicked == 1: # 한번 넘겼을때 게이지 튜토리얼 화면
        manager.SCREEN.blit(GUAGE_TUTORIAL, (0, 0))
    else: # 다시 넘겼을 때 메뉴로 돌아가는것
        clicked = 0
        img_idx = 0
        return True, "MENU"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"

        if event.type == pygame.KEYDOWN:
            # 엔터/스페이스로 다음 화면으로 넘김
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE: 
                clicked += 1

    all_sprites.draw(manager.SCREEN)
    pygame.display.update()
    return True, "TUTORIAL"
