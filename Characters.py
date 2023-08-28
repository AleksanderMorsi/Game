import pygame as pg
import os
from customFunctions import load_sprite_sheets

class Characters(pg.sprite.Sprite):
    GRAVITY = 50
    def __init__(self, sprite_dir1, sprite_dir2,sprite_w, sprite_h, x, y,speed, jump_p,
                 strength,dmg,hp, range,  scale = 2):
        super().__init__()
        self.size = (sprite_w*scale, sprite_h*scale)
        self.sprites = load_sprite_sheets(sprite_dir1, sprite_dir2, sprite_w, sprite_h, scale=scale)
        self.sprite = self.sprites["Idle_right"][0]
        self.pos = list((x, y))
        self.vel = list((0, 0))
        self.hp = hp
        self.range = range
        self.rect = pg.Rect(x,y,sprite_w *scale , sprite_h * scale) # collision rect (collision with mask)
        self.jump_p = jump_p
        self.speed = speed / 20
        self.str = strength /20
        self.dmg = dmg
        self.anim_count = 0 # animation frame counter
        self.animation_time = 7 # frames before next animation frame
        self.fall_count = 0
        self.mask = pg.mask.from_surface(self.sprite)
        self.collision_x = False
        self.collision_y = False
        self.dead = False
        self.is_attacking = False
        self.melee = False
        self.direction = "right"
        self.type = "Character"
        self.collide_with = ["Object"] # list of object types that player can't walk through
        self.attack_cooldown = 0
        self.attack_frame = False # frame in which collision test takes place

    def draw(self, surface, offset):
        if not self.dead:
            if self.vel[0] == 0 and self.vel[1] == 0:
                self.sprite = self.sprites["Idle_"+self.direction][
                    self.anim_count // self.animation_time % len(self.sprites["Idle_"+self.direction])]
            elif self.vel[0] != 0 and self.vel[1] == 0:
                self.sprite = self.sprites["Run_"+self.direction][
                    self.anim_count // self.animation_time % len(self.sprites["Run_"+self.direction])]
            elif self.vel[1] != 0:
                self.sprite = self.sprites["Fall_"+self.direction][
                    self.anim_count // self.animation_time % len(self.sprites["Fall_"+self.direction])]
            if self.is_attacking:
                if self.anim_count // self.animation_time <= len(self.sprites["Attack1_"+self.direction]):
                    self.sprite = self.sprites["Attack1_"+self.direction][
                        self.anim_count // self.animation_time % len(self.sprites["Attack1_"+self.direction])]
                else:
                    self.is_attacking = False
                if self.anim_count / self.animation_time == len(self.sprites["Attack1_" + self.direction]):
                    self.attack_frame = True
                else:
                    self.attack_frame = False

            self.rect.x += offset[0]
            self.rect.y += offset[1]
            pg.draw.rect(surface, (0, 0, 255), self.rect, 2)
            self.rect.x -= offset[0]
            self.rect.y -= offset[1]
            surface.blit(self.sprite, (self.pos[0] + offset[0], self.pos[1]+offset[1]))
            self.anim_count += 1
        else:
            self.sprite = self.sprites["Dead_"+self.direction][
                self.anim_count // self.animation_time % len(self.sprites["Dead_"+self.direction])]
            surface.blit(self.sprite, (self.pos[0] + offset[0], self.pos[1]+offset[1]))
            self.anim_count += 1

    def update(self, objects, delta_time):
        if not self.dead:
            self.attack_cooldown = max(0, self.attack_cooldown-1)
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
        else:
            pass

    def attack(self):
        if self.attack_cooldown == 0:
            self.is_attacking = True
            self.anim_count = 0
            self.vel[0] = 0
            self.attack_cooldown = len(self.sprites["Attack1_right"])*self.animation_time

    def get_attacked(self, dmg, str):
        if not self.dead:
            self.hp -= dmg
            if self.hp <=0:
                self.dead = True
                self.anim_count = 0

    def collide(self, objects, delta_time):
        for object in objects:
            if object != self:
                if (object.type == "Enemy" and self.is_attacking and self.melee and
                        pg.sprite.collide_mask(self, object) and self.attack_frame):
                    object.get_attacked(self.dmg, self.str)
                    self.attack_frame = False
                    print(object.hp)
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

    def jump(self):
        self.vel[1] -= self.jump_p//10

    def moveright(self):
        if not self.is_attacking:
            if self.direction != "right":
                self.anim_count = 0
            self.vel[0] = self.speed
        self.direction = "right"

    def moveleft(self):
        if not self.is_attacking:
            if self.direction != "left":
                self.anim_count = 0
            self.vel[0] = -self.speed
        self.direction = "left"

    def stop(self):
        if not self.is_attacking:
            self.anim_count = 0
        self.vel[0] = 0


class Player(Characters):
    def __init__(self, x, y):
        super().__init__("MainCharacters", "Knight_1",86, 86, x, y,
                         10,10, 10, 10, 100, 10)
        self.melee = True

    def loop(self):
        pass
        
class Knight(Characters):
    def __init__(self, x, y):
        super().__init__("MainCharacters", "Knight_3",86, 86, x, y,
                         8,10, 8, 8, 20, 10)
        self.type = "Enemy"
        self.melee = True

    def loop(self):
        pass

