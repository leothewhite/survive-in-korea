import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()

    def update(self, pos):
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class Border(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, pos):
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class Place(pygame.sprite.Sprite):
    def __init__(self, img, name, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, pos):
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Guage:
    def __init__(self, stress, grade, future, health):
        self.stress = stress
        self.grade = grade
        self.future = future
        self.health = health
