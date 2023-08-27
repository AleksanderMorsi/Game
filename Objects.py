import pygame as pg
from customFunctions import load_sprite_sheets

class Object(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = load_sprite_sheets("Tileset", "Night", 32,32, direction=False)
        self.sprite = self.sprites["Tileset"][25]
        self.pos = list((1000,500))

    def draw(self, surface):
        surface.blit(self.sprite, (self.pos[0], self.pos[1]))

    def update(self):
        pass
