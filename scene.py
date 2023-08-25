from property import *
from manager import *


manager = ManageVariable()


############### 이미지+스프라이트 로딩 #################
place_path = "./resources/images/place/"
guage_path = "./resources/images/guage/"

border_image = pygame.image.load("./resources/images/background/border.png")
background_image = pygame.image.load("./resources/images/background/background.png")
place_image = [
    (i.split(".")[0], pygame.image.load(place_path + i))
    for i in os.listdir(place_path)
    if i != ".DS_Store"
]
guage_image = {
    i.split(".")[0]: pygame.image.load(guage_path + i)
    for i in os.listdir(guage_path)
    if i != ".DS_Store"
}

for _, v in enumerate(place_image):
    file_name = v[0]
    file = v[1]
    places[v[0][0]].append(Place(file, file_name[2:], (0, screen_size.y), file_name[0]))
    place_cnt[file_name[2:]] = 0
manager.place_now = places["a"][0]

for i in range(50):
    now_y = i * border_size.y

    manager.block = [
        # 두세트를 만듦
        Border(border_image, (305, now_y)),
        Border(border_image, (305, background_size.y + now_y)),
        Border(border_image, (625, now_y)),
        Border(border_image, (625, background_size.y + now_y)),
    ]
    for i in range(4):
        borders[i].append(manager.block[i])
        manager.all_sprites.add(manager.block[i])
# * 씬 함수들은 RUNNING과 다음 씬을 리턴한다

#######################################################


def game_scene():
    manager.SCREEN.blit(background_image, (0, manager.bg_y))

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

    # * 게임 캐릭터가 죽었으면 OVER {reason} 값을 리턴한다
    if reason:
        return True, "OVER" + f" {reason}"

    manager.player_x += manager.to_x
    print(manager.bg_y)
    if not -(200 + 256) <= manager.bg_y <= -200:
        manager.player_x = pygame.math.clamp(manager.player_x, 320, 580)
    else:
        manager.player_x = pygame.math.clamp(manager.player_x, 0, 580)
    manager.player.update((manager.player_x, 240))

    manager.all_sprites.draw(manager.SCREEN)

    if manager.title != -1:
        manager.SCREEN.blit(manager.title, (40, 40))

    guages = [guage.stress, guage.health, guage.grade, guage.future]
    guage_name = ["stress", "health", "grade", "future"]

    for i in range(4):
        manager.SCREEN.blit(guage_image["frame"], (525, 320 + 40 * i))

        guages[i] = pygame.math.clamp(guages[i], 0, 100)
        for j in range(20):
            if j < guages[i] // 5:
                manager.SCREEN.blit(
                    guage_image[guage_name[i]], (527 + (5 * j), 322 + (40 * i))
                )

    manager.to_x = 0

    pygame.display.update()

    return True, "GAME"


def menu_scene():
    all_sprites = pygame.sprite.Group()
    obj = {
        "background": pygame.image.load("./resources/images/menu/menu_background.png"),
        "start": Button(pygame.image.load("./resources/images/menu/game_start.png")),
        "exit": Button(pygame.image.load("./resources/images/menu/game_exit.png")),
        "tutorial": Button(
            pygame.image.load("./resources/images/menu/game_tutorial.png")
        ),
    }

    obj["start"].update((200, 200))
    obj["exit"].update((200, 260))
    obj["tutorial"].update((200, 320))

    all_sprites.add(obj["start"])
    all_sprites.add(obj["exit"])
    all_sprites.add(obj["tutorial"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"

        #  * 마우스 버튼 클릭
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if obj["start"].rect.collidepoint(x, y):
                print("start game")
                return True, "GAME"
            if obj["exit"].rect.collidepoint(x, y):
                print("exit game")
                return False, "END"
            if obj["tutorial"].rect.collidepoint(x, y):
                print("tutorial")
                return False, "TUTORIAL"

    manager.SCREEN.blit(obj["background"], (0, 0))

    all_sprites.draw(manager.SCREEN)

    pygame.display.update()

    return True, "MENU"


def over_scene(reason):
    all_sprites = pygame.sprite.Group()
    return_menu = Button(pygame.image.load("./resources/images/menu/return.png"))
    return_menu.update((200, 400))
    all_sprites.add(return_menu)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if return_menu.rect.collidepoint(x, y):
                return True, "MENU"

    over = {}

    over_path = "./resources/images/menu/ending/"
    for i in os.listdir(over_path):
        name = i.split(".")[0].split("_")[-1]
        over[name] = pygame.image.load(over_path + i)

    manager.SCREEN.blit(over[reason], (0, 0))
    all_sprites.draw(manager.SCREEN)
    pygame.display.update()
    manager.clear()

    return True, "OVER " + reason


clicked = 0

# TODO: 게임 오버시 변수 초기화


def tutorial_scene():
    global clicked
    all_sprites = pygame.sprite.Group()
    keyboard_tutorial = pygame.image.load(
        "./resources/images/menu/tutorial_keyboard.png"
    )
    guage_tutorial = pygame.image.load("./resources/images/menu/tutorial_guage.png")

    if clicked == 0:
        manager.SCREEN.blit(keyboard_tutorial, (0, 0))
    elif clicked == 1:
        manager.SCREEN.blit(guage_tutorial, (0, 0))
    else:
        return True, "MENU"

    next_button = Button(pygame.image.load("./resources/images/menu/button_next.png"))
    next_button.update((500, 30))
    all_sprites.add(next_button)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"

        #  * 마우스 버튼 클릭
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if next_button.rect.collidepoint(x, y):
                clicked += 1

    all_sprites.draw(manager.SCREEN)
    pygame.display.update()
    return True, "TUTORIAL"
