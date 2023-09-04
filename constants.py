import pygame
from property import Size, MenuBackground
import os

pygame.font.init()


FONT = pygame.font.Font("./resources/fonts/NeoDunggeunmoPro-Regular.ttf", 30)
BORDER_SIZE = Size(16, 32)
SCREEN_SIZE = Size(640, 480)
BG_SIZE = Size(640, 480)
PLACE_PATH = "./resources/images/place/"
GUAGE_PATH = "./resources/images/guage/"


BORDER_IMAGE = pygame.image.load("./resources/images/background/border.png")
BG_IMAGE = pygame.image.load("./resources/images/background/background.png")

PLACE_IMAGE = [
    (i.split(".")[0], pygame.image.load(PLACE_PATH + i))
    for i in os.listdir(PLACE_PATH)
    if i != ".DS_Store"
]

GUAGE_IMAGE = {
    i.split(".")[0]: pygame.image.load(GUAGE_PATH + i)
    for i in os.listdir(GUAGE_PATH)
    if i != ".DS_Store"
}
TUTORIAL_KEYBOARD = []

for i in range(1, 4):
    for _ in range(20):
        TUTORIAL_KEYBOARD.append(
            pygame.image.load(f"./resources/images/menu/tutorial_keyboard{i}.png")
        )


MENU_BACKGROUND = MenuBackground()

SEMESTER = ["1학년 1학기", "1학년 2학기", "2학년 1학기", "2학년 2학기", "3학년 1학기", "3학년 2학기"]
