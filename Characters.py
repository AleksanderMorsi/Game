import pygame as pg
import os
from customFunctions import load_sprite_sheets

class Characters(pg.sprite.Sprite):
    GRAVITY = 50
    def __init__(self, sprite_dir1, sprite_dir2,sprite_w, sprite_h, x, y, speed, jump_p, scale = 2):
        super().__init__()
        self.size = (sprite_w*scale, sprite_h*scale)
        self.sprites = load_sprite_sheets(sprite_dir1, sprite_dir2, sprite_w, sprite_h, scale=scale)
        self.sprite = self.sprites["Idle_right"][0]
        self.pos = list((x, y))
        self.vel = list((0, 0))
        self.rect = pg.Rect(x,y,sprite_w, sprite_h)
        self.jump_p = jump_p
        self.speed = speed
        self.anim_count = 0
        self.fall_count = 0
        self.mask = pg.mask.from_surface(self.sprite)
        self.collision_x = False
        self.collision_y = False

    def draw(self, surface):
        surface.blit(self.sprite, (self.pos[0], self.pos[1]))

    def update(self, objects, delta_time):
        self.gravity_acc = min(1,(self.fall_count/1000 /delta_time) * self.GRAVITY)
        self.vel[1] += self.gravity_acc
        self.fall_count += 1
        self.collide(objects, delta_time)
        if self.collision_y:
            self.vel[1] = 0
            self.fall_count =0
        if self.collision_x:
            self.vel[0] = 0
        self.pos[1] += self.vel[1] * delta_time
        self.pos[0] += self.vel[0] * delta_time
        self.collision_y = False
        self.collision_x = False
        self.rect.x, self.rect.y = self.pos

    def collide(self, objects, delta_time):
        for object in objects:
            if object != self:
                self.rect.x += (self.vel[0] * delta_time)
                if pg.sprite.collide_mask(self, object):
                    self.collision_x =True
                self.rect.x -= (self.vel[0] * delta_time)
                self.rect.y += (self.vel[1] * delta_time)
                if pg.sprite.collide_mask(self, object):
                    self.collision_y =True
                    self.pos[1] = object.pos[1]-self.size[1]
                self.rect.y -= (self.vel[1] * delta_time)
            # if object != self:
            #     self.pos[0] += (self.vel[0] * delta_time)
            #     if pg.sprite.collide_mask(self, object):
            #         self.collision_x =True
            #     self.pos[0] -= (self.vel[0] * delta_time)
            #     self.pos[1] += (self.vel[1] * delta_time)
            #     if pg.sprite.collide_mask(self, object):
            #         self.collision_y =True
            #         self.pos[1] = object.pos[1]-self.size[1]
            #     self.pos[1] += (self.vel[1] * delta_time)

    def jump(self):
        self.vel[1] -= self.jump_p//10

class Player(Characters):
    def __init__(self, dir1, dir2, x, y, speed, jump_p):
        super().__init__(dir1, dir2,86, 86, x, y, speed, jump_p)
