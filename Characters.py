import pygame as pg
import os
from customFunctions import load_sprite_sheets

class Characters(pg.sprite.Sprite):
    GRAVITY = 50
    def __init__(self, sprite_dir1, sprite_dir2,sprite_w, sprite_h, x, y,speed, jump_p,
                 strength,dmg,hp, range, scale = 2, death_offset = 0, debug = False):
        super().__init__()
        self.size = (sprite_w*scale, sprite_h*scale)
        self.sprites = load_sprite_sheets(sprite_dir1, sprite_dir2, sprite_w, sprite_h, scale=scale)
        self.sprite = self.sprites["Idle_right"][0]
        self.pos = list((x, y))
        self.vel = list((0, 0))
        self.hp_bar_width = 80
        self.hp_bar_height = 10
        self.hp = hp
        self.hp_max = hp
        self.hp_bar = pg.Rect(x+self.size[0]//2 - self.hp_bar_width//2,
                                  y, self.hp_bar_width, self.hp_bar_height)
        self.hp_green = (30, 222, 30)
        self.hp_red = (222, 30, 30)
        self.range = range
        self.reach = 0
        self.rect = pg.Rect(x,y,sprite_w *scale , sprite_h * scale) # collision rect (collision with mask)
        self.jump_p = jump_p
        self.speed = speed / 20
        self.str = strength /20
        self.dmg = dmg
        self.anim_count = 0 # animation frame counter
        self.fps = 10
        self.animation_time = int(0.11 * self.fps) # frames before next animation frame
        self.fall_count = 0
        self.deathoffset = death_offset # adjusts death animation to fit
        self.dead = False
        self.melee = False
        self.direction = "right"
        self.type = "Character"
        self.collide_with = ["Object"] # list of object types that player can't walk through
        self.mask = pg.mask.from_surface(self.sprite)
        self.mask_image = self.mask.to_surface()
        self.collision_x = False
        self.collision_y = False
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_frame = False # frame in which collision test takes place
        self.hit = False
        self.is_defending = False
        self.on_ground = False
        self.disappear_time_s = 120 # after death
        self.chase_range = 1500
        self.debug = debug

    def draw(self, surface, offset):
        if not self.dead:
            if self.hit:
                self.sprite = self.sprites["Hurt_"+self.direction][self.anim_count//self.animation_time]
                if self.anim_count+1 == (len(self.sprites["Hurt_"+self.direction]))*self.animation_time:
                    self.hit = False
                    self.anim_count = 0

            elif self.is_defending:
                self.sprite = self.sprites["Protect_" + self.direction][
                    self.anim_count//self.animation_time % len(self.sprites["Protect_" + self.direction])-1]

            elif not self.on_ground:
                if self.anim_count // self.animation_time <= len(self.sprites["Jump_"+self.direction])-1:
                    self.sprite = self.sprites["Jump_" + self.direction][
                        self.anim_count // self.animation_time % len(self.sprites["Jump_"+self.direction])
                    ]
                else:
                    self.sprite = self.sprites["Idle_"+self.direction][
                        self.anim_count // self.animation_time % len(self.sprites["Idle_"+self.direction])]
                if self.anim_count / self.animation_time == len(self.sprites["Jump_"+self.direction])-1:
                    self.attack_frame = True
                    self.is_attacking = True
                else:
                    self.is_attacking = False

            elif self.is_attacking:
                if self.anim_count // self.animation_time <= len(self.sprites["Attack1_"+self.direction]):
                    self.sprite = self.sprites["Attack1_"+self.direction][
                        self.anim_count // self.animation_time % len(self.sprites["Attack1_"+self.direction])]
                else:
                    self.is_attacking = False
                if self.anim_count / self.animation_time == len(self.sprites["Attack1_" + self.direction])-1:
                    self.attack_frame = True
                else:
                    self.attack_frame = False

            elif self.vel[0] == 0 and self.vel[1] == 0:
                self.sprite = self.sprites["Idle_"+self.direction][
                    self.anim_count // self.animation_time % len(self.sprites["Idle_"+self.direction])]

            elif self.vel[0] != 0 and self.vel[1] == 0:
                self.sprite = self.sprites["Run_"+self.direction][
                    self.anim_count // self.animation_time % len(self.sprites["Run_"+self.direction])]

            elif self.vel[1] != 0:
                self.sprite = self.sprites["Idle_"+self.direction][
                    self.anim_count // self.animation_time % len(self.sprites["Idle_"+self.direction])]

            pg.draw.rect(surface, self.hp_red, pg.Rect(self.hp_bar.x + offset[0], self.hp_bar.y + offset[1],
                                                       self.hp_bar.width, self.hp_bar.height))
            pg.draw.rect(surface, self.hp_green, pg.Rect(self.hp_bar.x + offset[0], self.hp_bar.y + offset[1],
                                                       self.hp_bar.width*(self.hp/self.hp_max),
                                                         self.hp_bar.height))
            surface.blit(self.sprite, (self.pos[0] + offset[0], self.pos[1]+offset[1]))
            self.anim_count += 1
            if self.type=="Enemy":
                pass
        else:
            if self.anim_count >= 0:
                self.sprite = self.sprites["Dead_"+self.direction][
                    min(len(self.sprites["Dead_" + self.direction]) -1,
                        self.anim_count // self.animation_time)]
                surface.blit(self.sprite, (self.pos[0] + offset[0] + self.deathoffset,
                                           self.pos[1]+offset[1]))
                self.anim_count += 1
            else:
                self.anim_count = -1
        if self.debug == True:
            print("is_attacking: ", self.is_attacking)
            print("-------------------------------------")

    def update(self, objects, delta_time):
        if not self.dead:
            self.loop(delta_time, objects)

            self.attack_cooldown = max(0, self.attack_cooldown-1)
            self.gravity_acc = min(1,(self.fall_count/10000000) * self.GRAVITY  *delta_time*delta_time)
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
            self.hp_bar.x = self.pos[0] +self.size[0]//2 - self.hp_bar_width//2
            self.hp_bar.y = self.pos[1]
        else:
            self.stop(delta_time)
            self.gravity_acc = min(1,(self.fall_count/10000000) * self.GRAVITY  *delta_time*delta_time)
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
            self.rect.x, self.rect.y = self.pos
            self.collision_y = False
            self.collision_x = False

            if self.anim_count*delta_time > self.disappear_time_s*1000:
                self.anim_count = -1

    def attack(self):
        if self.attack_cooldown == 0 and not self.hit:
            self.is_attacking = True
            self.anim_count = 0
            self.vel[0] = 0
            self.attack_cooldown = len(self.sprites["Attack1_right"])*self.animation_time

    def get_attacked(self, dmg, str, object):
        if not self.dead:
            if not self.is_defending:
                self.hit = True
                self.is_attacking = False
                self.hp -= dmg
                if self.hp <=0:
                    self.dead = True
            self.anim_count = 0
            if object.direction == "right":
                self.direction = "left"
                self.vel[0] += str
            else:
                self.direction = "right"
                self.vel[0] -= str
            self.vel[1] -= 0.2 * str

    def defend(self, defend):
        if not self.hit and defend:
            self.is_defending = True
            self.is_attacking = False
        else:
            self.is_defending = False

    def env_update(self, fps):
        self.animation_time = int(0.11 * fps)

    def collide(self, objects, delta_time):
        self.mask = pg.mask.from_surface(self.sprite)
        self.onground = False
        if self.debug == True:
            print("---------------------------------------")
        on_ground= False
        for object in objects:
            if object != self and abs(object.pos[0] - self.pos[0]) < 200:
                if (object.type != self.type and self.is_attacking and self.melee and
                        pg.sprite.collide_mask(self, object) and self.attack_frame):
                    object.get_attacked(self.dmg, self.str, self)
                    self.attack_frame = False
                if object.type not in self.collide_with:
                    continue
                self.rect.y += 5
                if self.debug == True:
                    print(self.on_ground, self.pos[1], self.rect.y, object.pos[1])
                if pg.sprite.collide_mask(self, object):
                    on_ground = True
                self.rect.y -= 5
                self.rect.y += (self.vel[1] * delta_time)+2
                if pg.sprite.collide_mask(self, object):
                    self.collision_y =True
                    self.pos[1] = object.pos[1]-self.size[1]
                self.rect.y -= (self.vel[1] * delta_time)+2
                self.rect.x += (self.vel[0] * delta_time)+5
                if pg.sprite.collide_mask(self, object):
                    self.collision_x =True
                self.rect.x -= (self.vel[0] * delta_time)+5
        self.on_ground = on_ground

    def jump(self):
        if self.on_ground:
            self.anim_count = 0
            self.vel[1] -= self.jump_p/100

    def moveright(self):
        if not self.is_attacking and not self.hit  and self.on_ground:
            if self.direction != "right":
                self.anim_count = 0
            self.vel[0] = self.speed
        if self.on_ground:
            self.direction = "right"

    def moveleft(self):
        if not self.is_attacking and not self.hit  and self.on_ground:
            if self.direction != "left":
                self.anim_count = 0
            self.vel[0] = -self.speed
        if self.on_ground:
            self.direction = "left"

    def stop(self, delta_time):
        if self.on_ground:
            if self.vel[0] > 0.1 or self.vel[0] < -0.1:
                self.vel[0] -= self.vel[0]/100 * delta_time
            else:
                self.vel[0] = 0

    def move_to_player(self,player):
        dist = player.pos[0]-self.pos[0]
        if abs(dist) > self.reach and abs(dist) < self.chase_range:
            if dist > 0:
                self.moveright()
            else:
                self.moveleft()

    def melee_attack_player(self, player):
        dist = player.pos[0]-self.pos[0]
        if abs(dist) <= self.reach:
            self.attack()
            if dist > 0:
                self.moveright()
            else:
                self.moveleft()

# creating new character template:
# class Name(Characters):
#     def __init__(self, x, y, debug=False):
#         super().__init__(...)
#         self.debug = debug
#         self.type = "type"  # "Enemy" only, for now
#         self.melee = False  # Temporary maybe
#
#     def loop(self, delta_time, objects):  # every loop action
#         self.stop(delta_time)
#         # player = objects[-1]
#         # self.move_to_player/melee_attack_player/moveright/moveleft/jump/stop

class Player(Characters):
    def __init__(self, x, y, debug = False):
        super().__init__("MainCharacters", "Knight_1",86, 86, x, y,
                         10,10, 10, 10, 80, 10)
        self.debug = debug
        self.type = "Player"
        self.melee = True

    def loop(self, delta_time, objects):
        self.stop(delta_time)
        
class Knight(Characters):
    def __init__(self, x, y, debug = False):
        super().__init__("MainCharacters", "Knight_3",86, 86, x, y,
                         6,10, 8, 8, 20, 10, death_offset=30)
        self.debug = debug
        self.type = "Enemy"
        self.melee = True
        self.reach = 100

    def loop(self, delta_time, objects):
        self.stop(delta_time)
        player = objects[-1]
        self.move_to_player(player)
        self.melee_attack_player(player)

