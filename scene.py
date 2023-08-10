from property import *
from manager import *


manager = ManageVariable()

manager.player_x = 320
manager.to_x = 0
manager.all_sprites = pygame.sprite.Group()
manager.SCREEN = pygame.display.set_mode((640, 480))
manager.speed = 0.2
manager.inPlace = False
manager.month = 0

load_images()
load_border()


manager.player = Character(manager.images["player"])

manager.player.update((manager.player_x, 240))
manager.all_sprites.add(manager.player)

# * 씬 함수들은 RUNNING과 다음 씬을 리턴한다

isOver = False


def game_scene():
    global isOver
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, "END"
        event_handler(event)
    # * 꾹 누르고 있는 상태 움직임
    move_player()

    if not manager.inPlace:
        make_gravity()
        collide_manager()
        background_manager()
        guage_manager()

    reason = ending_manager()

    if manager.isText:
        title = font.render(f"{manager.month} 월", True, pygame.Color(0, 0, 0))
        manager.SCREEN.blit(title, (40, 40))
    # * 게임 캐릭터가 죽었으면 OVER {reason} 값을 리턴한다
    if reason:
        return True, "OVER" + f" {reason}"

    manager.player_x += manager.to_x

    manager.player.update((manager.player_x, 240))
    manager.all_sprites.draw(manager.SCREEN)
    manager.to_x = 0

    pygame.display.update()

    return True, "GAME"


def menu_scene():
    all_sprites = pygame.sprite.Group()
    obj = {
        "background": pygame.image.load("./resources/images/menu/menu_background.png"),
        "start": Button(pygame.image.load("./resources/images/menu/game_start.png")),
        "exit": Button(pygame.image.load("./resources/images/menu/game_exit.png")),
    }

    obj["start"].update((200, 200))
    obj["exit"].update((200, 260))

    all_sprites.add(obj["start"])
    all_sprites.add(obj["exit"])

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

    return True, "OVER " + reason
