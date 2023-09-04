from property import *
from manager import *
from constants import *
from variable import initialize

manager = ManageVariable()


#######################################################


manager.player.update((manager.player_x, 240))
manager.all_sprites.add(manager.player)


def game_scene():
    manager.SCREEN.blit(BG_IMAGE, (0, manager.bg_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"
        event_handler(event)

    # * 꾹 누르고 있는 상태 움직임
    move_player()
    text_handler()

    if not manager.inPlace:
        make_gravity()
        collide_manager()
        background_manager()

    reason = ending_manager()
    manager.place_now.draw(manager.SCREEN)

    # 캐릭터가 죽었으면 OVER {reason} 값을 리턴한다
    if reason:
        return True, "OVER" + f" {reason}"

    manager.player_x += manager.to_x

    ################ 플레이어 가두기 ##################
    if not -(200 + 256) <= manager.bg_y <= -200:
        manager.player_x = pygame.math.clamp(
            manager.player_x,
            320,
            SCREEN_SIZE.x - manager.player.rect.width - BORDER_SIZE.x,
        )
    else:
        manager.player_x = pygame.math.clamp(manager.player_x, 0, 580)
    ##############################################

    ########## 화면에 그리기 ###############
    manager.player.update((manager.player_x, 240))
    manager.all_sprites.draw(manager.SCREEN)

    if manager.title != -1:
        manager.SCREEN.blit(manager.title, (40, 40))
    ####################################

    ################## 게이지 그리기 ##################
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
        manager.SCREEN.blit(GUAGE_IMAGE["frame_" + guage_name[i]], (525, 320 + 40 * i))
    #################################################
    manager.to_x = 0
    pygame.display.update()

    return True, "GAME"


select_idx = 0


def menu_scene():
    global select_idx
    obj = {
        "start": Button(
            pygame.image.load("./resources/images/menu/game_start.png"), (200, 200)
        ),
        "exit": Button(
            pygame.image.load("./resources/images/menu/game_exit.png"), (200, 260)
        ),
        "tutorial": Button(
            pygame.image.load("./resources/images/menu/game_tutorial.png"), (200, 320)
        ),
        "select": pygame.image.load("./resources/images/menu/select.png"),
    }

    title = pygame.image.load("./resources/images/menu/title.png")
    MENU_BACKGROUND.update()
    manager.all_sprites_menu.add(MENU_BACKGROUND)

    manager.all_sprites_menu.add(obj["start"])
    manager.all_sprites_menu.add(obj["exit"])
    manager.all_sprites_menu.add(obj["tutorial"])
    event_list = pygame.event.get()
    print(select_idx)
    for event in event_list:
        if event.type == pygame.QUIT:
            return False, "END"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                select_idx -= 1

                if select_idx < 0:
                    select_idx = 0
            if event.key == pygame.K_DOWN:
                select_idx += 1

                if 2 < select_idx:
                    select_idx = 2

            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if select_idx == 0:
                    return True, "GAME"
                elif select_idx == 1:
                    return False, "END"
                elif select_idx == 2:
                    return False, "TUTORIAL"

    event_list = []

    manager.all_sprites_menu.draw(manager.SCREEN)
    manager.SCREEN.blit(title, (80, 40))
    manager.SCREEN.blit(obj["select"], (196, 196 + 60 * select_idx))
    pygame.display.update()

    return True, "MENU"


def over_scene(reason):
    all_sprites = pygame.sprite.Group()
    return_menu = pygame.image.load("./resources/images/menu/return.png")
    return_menu.blit(manager.SCREEN, (200, 400))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return True, "MENU"

    over = {}

    over_path = "./resources/images/menu/ending/"
    for i in os.listdir(over_path):
        name = i.split(".")[0].split("_")[-1]
        over[name] = pygame.image.load(over_path + i)

    manager.SCREEN.blit(over[reason], (0, 0))
    all_sprites.draw(manager.SCREEN)
    pygame.display.update()

    return True, "OVER " + reason


img_idx = 0

clicked = 0


def tutorial_scene():
    global clicked, img_idx
    print(clicked)
    all_sprites = pygame.sprite.Group()

    guage_tutorial = pygame.image.load("./resources/images/menu/tutorial_guage.png")
    if clicked == 0:
        img_idx += 1
        manager.SCREEN.blit(TUTORIAL_KEYBOARD[img_idx % 60], (0, 0))
    elif clicked == 1:
        manager.SCREEN.blit(guage_tutorial, (0, 0))
    else:
        clicked = 0
        return True, "MENU"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                clicked += 1

    all_sprites.draw(manager.SCREEN)
    pygame.display.update()
    return True, "TUTORIAL"
