import os
import pygame as pg
from customFunctions import load_sprite_sheets
class Background(pg.sprite.Sprite):
    def __init__(self,dir1, dir2, width, height, number, planetnum, planetscale):
        self.sprites = load_sprite_sheets(dir1, dir2, width, height, False)
        self.image = self.sprites[dir1][number]
        self.planet =pg.transform.scale_by(self.sprites[dir1][planetnum], planetscale)
        WIDTH = pg.display.get_surface().get_width()
        HEIGHT = pg.display.get_surface().get_height()
        width, height = self.image.get_width(), self.image.get_height()
        self.tiles = []
        for i in range(WIDTH // width + 1):
            for j in range(HEIGHT // height + 1):
                pos = [i * width, j * height]
                self.tiles.append(pos)
        self.surface = pg.Surface(pg.display.get_window_size())
        for tile in self.tiles:
            self.surface.blit(self.image, tile)
        self.surface.blit(self.planet, (int(WIDTH*0.7),HEIGHT//3))
    def update(self):
        WIDTH = pg.display.get_surface().get_width()
        HEIGHT = pg.display.get_surface().get_height()
        width, height = self.image.get_width(), self.image.get_height()
        self.tiles = []
        for i in range(WIDTH // width + 1):
            for j in range(HEIGHT // height + 1):
                pos = [i * width, j * height]
                self.tiles.append(pos)
        self.surface = pg.Surface(pg.display.get_window_size())
        for tile in self.tiles:
            self.surface.blit(self.image, tile)
        self.surface.blit(self.planet, (int(WIDTH*0.7),HEIGHT//3))


    def draw(self, surface):
        surface.blit(self.surface, (0,0))

class Night(Background):
    def __init__(self):
        super().__init__("Tileset", "Night", 32, 32, 0, 89, 2)

