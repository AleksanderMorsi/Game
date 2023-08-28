import pygame as pg
from customFunctions import load_sprite_sheets

class Object(pg.sprite.Sprite):
    def __init__(self, sprite_dir1, sprite_dir2,sprite_w, sprite_h, x, y, number=2, scale=2, collide=True):
        super().__init__()
        self.size = (sprite_w,sprite_h)
        self.sprites = load_sprite_sheets(sprite_dir1, sprite_dir2, sprite_w,sprite_h, direction=False, scale=scale)
        self.sprite = self.sprites["Tileset"][number]
        self.pos = list((x, y))
        self.rect = pg.Rect(x,y, sprite_w,sprite_h)
        self.mask = pg.mask.from_surface(self.sprite)
        if collide:
            self.type = "Object"
        else:
            self.type = "Object!collide"

    def draw(self, surface, offset):
        surface.blit(self.sprite, (self.pos[0]+offset[0], self.pos[1]+offset[1]))

    def update(self, objects, delta_time):
        pass
