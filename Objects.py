import pygame as pg
from customFunctions import load_sprite_sheets

class Object(pg.sprite.Sprite):
    def __init__(self,name, sprite_dir1, sprite_dir2,sprite_w, sprite_h, x, y, number, scale=2, collide=True):
        super().__init__()
        self.size = (sprite_w*scale,sprite_h*scale)
        self.sprites = load_sprite_sheets(sprite_dir1, sprite_dir2, sprite_w,sprite_h, direction=False, scale=scale)
        self.sprite = self.sprites[name][number]
        self.pos = list((x, y))
        self.rect = pg.Rect(x,y, sprite_w,sprite_h)
        self.mask = pg.mask.from_surface(self.sprite)
        self.vel = (0,0)
        self.anim_lock = False
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

    def get_attacked(self, dmg, str, object):
        pass

# template:
# class name(Object):
#     def __init__(self, x, y):
#         super().__init__("name", "dir1", "dir2", w,h,
#                          x, y, number)
#         self.priority = 100
#
#     def get_class(self):
#         return "name"
    
class Grass_green(Object):
    def __init__(self, x, y):
        super().__init__("Tileset","Tileset", "Night", 32,32,
                         x, y, 2)
        self.priority = 100

    def get_class(self):
        return "Grass_green"

class Tree1(Object):
    def __init__(self, x, y):
        super().__init__("Trees","Tileset", "Night", 64,64,
                         x, y, 0, collide=False, scale=3)
        self.priority = 105

    def get_class(self):
        return "Tree1"
class Tree2(Object):
    def __init__(self, x, y):
        super().__init__("Trees","Tileset", "Night", 64,64,
                         x, y, 2, collide=False, scale=3)
        self.priority = 105

    def get_class(self):
        return "Tree2"
class Tree3(Object):
    def __init__(self, x, y):
        super().__init__("Trees","Tileset", "Night", 64,64,
                         x, y, 4, collide=False, scale=3)
        self.priority = 105

    def get_class(self):
        return "Tree3"
class Tree4(Object):
    def __init__(self, x, y):
        super().__init__("Trees","Tileset", "Night", 64,64,
                         x, y, 1, collide=False)
        self.priority = 105

    def get_class(self):
        return "Tree4"
class Tree5(Object):
    def __init__(self, x, y):
        super().__init__("Trees","Tileset", "Night", 64,64,
                         x, y, 3, collide=False)
        self.priority = 105

    def get_class(self):
        return "Tree5"
class Tree6(Object):
    def __init__(self, x, y):
        super().__init__("Trees","Tileset", "Night", 64,64,
                         x, y, 5, collide=False)
        self.priority = 105

    def get_class(self):
        return "Tree6"

class Stone1(Object):
    def __init__(self, x, y):
        super().__init__("Misc", "Tileset", "Night", 32,32,
                         x, y, 2, collide=False)
        self.priority = 80

    def get_class(self):
        return "Stone1"

class Stone2(Object):
    def __init__(self, x, y):
        super().__init__("Misc", "Tileset", "Night", 32,32,
                         x, y, 3, collide=False)
        self.priority = 80

    def get_class(self):
        return "Stone2"

class Stone3(Object):
    def __init__(self, x, y):
        super().__init__("Misc", "Tileset", "Night", 32,32,
                         x, y, 4, collide=False)
        self.priority = 80

    def get_class(self):
        return "Stone3"
