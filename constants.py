import pygame
from property import MenuBackground
import os
from property import Place

pygame.font.init()


FONT = pygame.font.Font("./resources/fonts/NeoDunggeunmoPro-Regular.ttf", 30)  # font 일일
BORDER_SIZE = (16, 32)
SCREEN_SIZE = (640, 480)
BG_SIZE = (640, 480)

SPEED = 0.2

# 파일들을 불러오기 위해 미리 경로 저장
PLACE_PATH = "./resources/images/place/"
GUAGE_PATH = "./resources/images/guage/"
OVER_PATH = "./resources/images/menu/ending/"

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

# a: 스트레스 해소 b: 공부 c: 진로
PLACES = {"a": [], "b": [], "c": []}
for _, v in enumerate(PLACE_IMAGE):
    file_name = v[0]
    file = v[1]
    PLACES[v[0][0]].append(
        Place(file, file_name[2:], (0, SCREEN_SIZE[1]), file_name[0])
    )

TUTORIAL_KEYBOARD = []

# 속도 조절 위해 한 프레임을 20번 넣어줌
for i in range(1, 4):
    for _ in range(20):
        TUTORIAL_KEYBOARD.append(
            pygame.image.load(f"./resources/images/menu/tutorial_keyboard{i}.png")
        )

GUAGE_TUTORIAL = pygame.image.load("./resources/images/menu/tutorial_guage.png")

MENU_BACKGROUND = MenuBackground()


SEMESTER = ["1학년 1학기", "1학년 2학기", "2학년 1학기", "2학년 2학기", "3학년 1학기", "3학년 2학기"]

OVER = {}

for i in os.listdir(OVER_PATH):
    name = i.split(".")[0].split("_")[-1]
    OVER[name] = pygame.image.load(OVER_PATH + i)
