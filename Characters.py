import pygame as pg
import os
from customFunctions import load_sprite_sheets

class Characters(pg.sprite.Sprite):
    GRAVITY = 1
    def __init__(self, sprite_dir1, sprite_dir2,sprite_w, sprite_h, x, y, speed, jump_p):
        super().__init__()
        self.sprites = load_sprite_sheets(sprite_dir1, sprite_dir2, sprite_w, sprite_h)
        self.sprite = self.sprites["Idle_right"][0]
        self.pos = list((x, y))
        self.vel = list((0, 0))
        self.jump_p = jump_p
        self.speed = speed
        self.anim_count = 0
        self.fall_count = 0

    def draw(self, surface):
        surface.blit(self.sprite, (self.pos[0], self.pos[1]))

    def update(self, objects, delta_time):
        self.vel[1] += min(0.1,(self.fall_count) * self.GRAVITY)
        self.fall_count += 1

        self.pos[0] += self.vel[0] * delta_time
        self.pos[1] += self.vel[1] * delta_time

class Player(Characters):
    def __init__(self, dir1, dir2, x, y, speed, jump_p):
        super().__init__(dir1, dir2,86, 86, x, y, speed, jump_p)
