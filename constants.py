import pygame
from property import MenuBackground
import os
from property import *

pygame.font.init()


FONT = pygame.font.Font("./resources/fonts/NeoDunggeunmoPro-Regular.ttf", 30)
BORDER_SIZE = (16, 32)
SCREEN_SIZE = (640, 480)
BG_SIZE = (640, 480)
PLACE_PATH = "./resources/images/place/"
GUAGE_PATH = "./resources/images/guage/"
SPEED = 0.2

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

PLACES = {"a": [], "b": [], "c": []}

for _, v in enumerate(PLACE_IMAGE):
    file_name = v[0]
    file = v[1]
    PLACES[v[0][0]].append(
        Place(file, file_name[2:], (0, SCREEN_SIZE[1]), file_name[0])
    )

TUTORIAL_KEYBOARD = []

for i in range(1, 4):
    for _ in range(20):
        TUTORIAL_KEYBOARD.append(
            pygame.image.load(f"./resources/images/menu/tutorial_keyboard{i}.png")
        )


MENU_BACKGROUND = MenuBackground()

SEMESTER = ["1학년 1학기", "1학년 2학기", "2학년 1학기", "2학년 2학기", "3학년 1학기", "3학년 2학기"]
