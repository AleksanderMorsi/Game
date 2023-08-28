import pygame as pg
import os
from customFunctions import load_sprite_sheets

class Characters(pg.sprite.Sprite):
    GRAVITY = 50
    def __init__(self, sprite_dir1, sprite_dir2,sprite_w, sprite_h, x, y,speed, jump_p,
                 strength,dmg,hp, scale = 2):
        super().__init__()
        self.size = (sprite_w*scale, sprite_h*scale)
        self.sprites = load_sprite_sheets(sprite_dir1, sprite_dir2, sprite_w, sprite_h, scale=scale)
        self.sprite = self.sprites["Idle_right"][0]
        self.pos = list((x, y))
        self.vel = list((0, 0))
        self.hp = hp
        self.rect = pg.Rect(x,y,sprite_w, sprite_h)
        self.jump_p = jump_p
        self.speed = speed / 20
        self.str = strength /20
        self.dmg = dmg
        self.anim_count = 0
        self.animation_time = 7
        self.fall_count = 0
        self.mask = pg.mask.from_surface(self.sprite)
        self.collision_x = False
        self.collision_y = False
        self.dead = False
        self.direction = "right"
        self.type = "Character"
        self.collide_with = ["Object"]
        self.attack_rect = pg.Rect(x+self.size[0]//2, y + self.size[1] //2, sprite_w, sprite_h//3)

    def draw(self, surface, offset):
        if self.vel[0] == 0 and self.vel[1] == 0:
            self.sprite = self.sprites["Idle_"+self.direction][
                self.anim_count // self.animation_time % len(self.sprites["Idle_"+self.direction])]
        elif self.vel[0] != 0 and self.vel[1] == 0:
            self.sprite = self.sprites["Run_"+self.direction][
                self.anim_count // self.animation_time % len(self.sprites["Run_"+self.direction])]
        elif self.vel[1] != 0:
            self.sprite = self.sprites["Fall_"+self.direction][
                self.anim_count // self.animation_time % len(self.sprites["Fall_"+self.direction])]

        self.attack_rect.x += offset[0]
        self.attack_rect.y += offset[1]
        pg.draw.rect(surface, (255, 0, 0), self.attack_rect, 2)
        self.attack_rect.x -= offset[0]
        self.attack_rect.y -= offset[1]
        surface.blit(self.sprite, (self.pos[0] + offset[0], self.pos[1]+offset[1]))
        self.anim_count += 1

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
        if self.direction == "right":
            self.attack_rect.x, self.attack_rect.y = (self.pos[0] + self.size[0]//2,
                                                  self.pos[1] + self.size[1] //2)
        if self.direction == "left":
            self.attack_rect.x, self.attack_rect.y = (self.pos[0] ,
                                                  self.pos[1] + self.size[1] //2)

    def attack(self):
        self.attack = True

    def get_attacked(self, dmg):
        self.hp -= dmg
        if self.hp <=0:
            self.dead = True

    def collide(self, objects, delta_time):
        for object in objects:
            if object != self:
                if (object.type == "Enemy" and self.attack and self.melee and
                        pg.sprite.collide_rect(self.attack_rect, object)):
                    object.get_attacked(self.dmg, self.strength)
                if object.type not in self.collide_with:
                    continue
                self.rect.y += (self.vel[1] * delta_time)+2
                if pg.sprite.collide_mask(self, object):
                    self.collision_y =True
                    self.pos[1] = object.pos[1]-self.size[1]
                self.rect.y -= (self.vel[1] * delta_time)+2
                self.rect.x += (self.vel[0] * delta_time)+50
                if pg.sprite.collide_mask(self, object):
                    self.collision_x =True
                self.rect.x -= (self.vel[0] * delta_time)+50
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

    def moveright(self):
        self.vel[0] = self.speed
        self.anim_count = 0
        self.direction = "right"

    def moveleft(self):
        self.vel[0] = -self.speed
        self.anim_count = 0
        self.direction = "left"

    def stop(self):
        self.vel[0] = 0
        self.anim_count = 0

class Player(Characters):
    def __init__(self, x, y):
        super().__init__("MainCharacters", "Knight_1",86, 86, x, y,
                         10,10, 10, 10, 100)
