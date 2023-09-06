import pygame as pg
from customFunctions import load_sprite_sheets

class Object(pg.sprite.Sprite):
    def __init__(self, sprite_dir1, sprite_dir2,sprite_w, sprite_h, x, y, number=2, scale=2, collide=True):
        super().__init__()
        self.size = (sprite_w,sprite_h)
        self.sprites = load_sprite_sheets(sprite_dir1, sprite_dir2, sprite_w,sprite_h, direction=False, scale=scale)
        self.sprite = self.sprites[sprite_dir1][number]
        self.pos = list((x, y))
        self.rect = pg.Rect(x,y, sprite_w,sprite_h)
        self.mask = pg.mask.from_surface(self.sprite)
        self.vel = (0,0)
        if collide:
            self.type = "Object"
        else:
            self.type = "Object!collide"

    def get_parent(self):
        return "Objects"

    def draw(self, surface, offset, window):
        surface.blit(self.sprite, (self.pos[0]+offset[0], self.pos[1]+offset[1]))

    def update(self, objects, delta_time):
        pass

    def env_update(self, fps, *args):
        pass
    
class Grass_green(Object):
    def __init__(self, x, y):
        super().__init__("Tileset", "Night", 32,32,x, y)

    def get_class(self):
        return "Grass_green"
