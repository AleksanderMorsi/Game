import os
import pygame as pg

def flip_sprites(sprites):
    return [pg.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=True):
    path = "assets/" + dir1 + "/" + dir2
    images = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pg.image.load(os.path.join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pg.Surface((width, height), pg.SRCALPHA, 32)
            rect = pg.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pg.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip_sprites(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

class Background(pg.sprite.Sprite):
    def __init__(self,dir1, dir2, width, height, number):
        self.sprites = load_sprite_sheets(dir1, dir2, width, height, False)
        self.image = self.sprites["Tileset"][number]
        WIDTH = pg.display.get_surface().get_width()
        HEIGHT = pg.display.get_surface().get_height()
        width, height = self.image.get_width(), self.image.get_height()
        self.tiles = []
        for i in range(WIDTH // width + 1):
            for j in range(HEIGHT // height + 1):
                pos = [i * width, j * height]
                self.tiles.append(pos)
        # self.surface = pg.Surface((surface.get_width(), surface.get_height()))
   # def set(self,dir1, dir2, width, height, number):
   #      sprites = load_sprite_sheets(dir1, dir2, width, height, False)
   #      return sprites["Tileset"][number]
    def get_background(self):
        return self.tiles, self.image

    # def draw(self, surface):
    #     surface.blit(self.sprite, (0,0))
    #     for i in range(surface.get_width()//self.sprite.get_width()):
    #         for j in range(surface.get_height()//self.sprite.get_height()):
    #             surface.blit(self.sprite, (i*self.sprite.get_width(), j*self.sprite.get_height()))
