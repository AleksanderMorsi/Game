import copy
import Backgrounds
import Objects
import customFunctions
import pygame as pg
import os
import random
import math
from os import listdir
from os.path import isfile, join
import Characters
from customFunctions import load_sprite_sheets
from Objects import Object

pg.init()
pg.display.set_caption("Editor")

# controlls:
# select: 0 to 9 keys (0 is None)
# mouse1 spawn, mouse3 delete
# snap to grid: press "g"
# camera speed: "z" lower, "x" higher
# drag spawn: "q"

# editor settings:
map = "maps/map1"

# default settings
WIN_SIZE = (1900, 900)
FPS = 60 # 9<FPS<145!!!
snap_to_grid = True
camera_speed = 10
drag_spawn = False # works only with grid snap
spawn_always = True

# init & load
window = pg.display.set_mode(WIN_SIZE)
surface = pg.Surface((3840, 2160))
try:
    file = open(map+".txt", "r")
except:
    file = open(map+".txt", "w+")
lines = file.readlines()
file.close()

class Mouse(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pg.Rect(0,0,1,1)
        self.mask = pg.mask.Mask((1,1))
        self.mask.fill()
        self.pos = [0,0]
        self.screenrect = pg.Rect(0,0,1,1)
        self.screenpos = [0,0]

    def update(self,objects, surface, window, player):
        x, y = pg.mouse.get_pos()
        self.screenpos[0] = x
        self.screenpos[1] = y
        self.screenrect.x = x
        self.screenrect.y = y
        win_center = (pg.display.get_surface().get_width()//2, pg.display.get_surface().get_height()//2)
        surface_center = (surface.get_width()//2, surface.get_height()//2)
        offset = [win_center[0]-player[0],
                  win_center[1] - player[1]]
        mousex = -offset[0]+x
        mousey = player[1] - window.get_height()//2 + y
        self.pos[0] = mousex
        self.pos[1] = mousey
        self.rect.x = mousex
        self.rect.y = mousey

def draw(surface, window, objects, background, player, selected, mouse):
    win_center = (pg.display.get_surface().get_width()//2, pg.display.get_surface().get_height()//2)
    surface_center = (surface.get_width()//2, surface.get_height()//2)
    offset = [surface_center[0]-player[0],
              surface_center[1] - player[1]]
    surface.blit(background.surface, (
        -win_center[0]+surface_center[0], -win_center[1]+surface_center[1]))

    for object in objects:
        object.anim_lock = True
        object.draw(surface, offset, window)

    mousex, mousey = mouse.pos
    if selected != None:
        if snap_to_grid:
            surface.blit(selected.sprite, (mousex//selected.size[0] * selected.size[0]+offset[0]    ,
                                       mousey//selected.size[1] * selected.size[1]+offset[1]    ))
        else:
            surface.blit(selected.sprite, (mousex+offset[0]    ,mousey+offset[1]))

    window.blit(surface,(win_center[0]-surface_center[0], win_center[1]-surface_center[1]))

    pg.display.update()

def spawn(selected, objects, mouse, surface, window, player):
    if selected != None:
        win_center = (pg.display.get_surface().get_width()//2, pg.display.get_surface().get_height()//2)
        surface_center = (surface.get_width()//2, surface.get_height()//2)
        offset = [win_center[0]-player[0],
                  win_center[1] - player[1]]
        mousex, mousey = mouse.pos
        occupied = False
        for object in objects:
            selected.rect.x = mousex//selected.size[0] * selected.size[0]
            selected.rect.y = mousey//selected.size[1] * selected.size[1]
            if pg.sprite.collide_mask(selected, object):
                occupied = True
        if not occupied or spawn_always:
            if snap_to_grid:
                command = "objects.append({}.{}({},{}))".format(selected.get_parent(), selected.get_class(),
                                                mousex//selected.size[0] * selected.size[0],
                                                mousey//selected.size[1] * selected.size[1])
            else:
                command ="objects.append({}.{}({},{}))".format(selected.get_parent(), selected.get_class(),
                                                mousex,mousey)
            exec (command, globals(), locals())

def delete(objects, mouse, surface, window, player):
    win_center = (pg.display.get_surface().get_width()//2, pg.display.get_surface().get_height()//2)
    surface_center = (surface.get_width()//2, surface.get_height()//2)
    offset = [win_center[0]-player[0],
              win_center[1] - player[1]]
    mousex, mousey = mouse.pos
    for i in range(len(objects)):
        object = objects[i]
        if pg.sprite.collide_mask(mouse, object):
            objects.pop(i)
            break

def update(objects, delta_time, mouse):
    pass

def main(window):
    global snap_to_grid, camera_speed, drag_spawn
    clock = pg.time.Clock()
    run = True

    objects = []
    background = Backgrounds.Night()
    a_pressed = False
    d_pressed = False
    w_pressed = False
    s_pressed = False
    z_pressed = False
    x_pressed = False
    selected_object = None
    mouse1_pressed = False
    mouse3_pressed = False

    paused  = False

    camera = [0, 0]

    mouse = Mouse()

    # spawns ------------------------------------------------------
    for line in lines:
        if len(line) > 3:
            words = line.split()
            command ="objects.append({}.{}({},{}))".format(words[0], words[1], words[2], words[3])
            exec(command)
    # --------------------------------------------------------------

    while run:
        delta_time = clock.tick(FPS)
        mouse.update(objects, surface, window, camera)
        fps = 1000/delta_time
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            if event.type == pg.VIDEORESIZE:
                background.update()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                    break
                if event.key == pg.K_p:
                    if paused:
                        paused = False
                    else:
                        paused = True
                if event.key == pg.K_SPACE:
                    pass
                if event.key == pg.K_w:
                    w_pressed = True
                if event.key == pg.K_s:
                    s_pressed = True
                if event.key == pg.K_a:
                    a_pressed = True
                if event.key == pg.K_d:
                    d_pressed = True
                if event.key == pg.K_z:
                    z_pressed = True
                if event.key == pg.K_x:
                    x_pressed = True
                if event.key == pg.K_g:
                    snap_to_grid = not snap_to_grid
                if event.key == pg.K_q:
                    drag_spawn = not drag_spawn
                if event.key == pg.K_1:
                    selected_object = Characters.Player(0,0)
                if event.key == pg.K_2:
                    selected_object = Characters.Knight(0,0)
                if event.key == pg.K_3:
                    selected_object = Objects.Stone3(0,0)
                if event.key == pg.K_4:
                    selected_object = Objects.Tree1(0,0)
                if event.key == pg.K_5:
                    selected_object = Objects.Tree2(0,0)
                if event.key == pg.K_6:
                    selected_object = Objects.Tree3(0,0)
                if event.key == pg.K_7:
                    selected_object = Objects.Tree4(0,0)
                if event.key == pg.K_8:
                    selected_object = Objects.Tree5(0,0)
                if event.key == pg.K_9:
                    selected_object = Objects.Tree6(0,0)
                if event.key == pg.K_0:
                    selected_object = None
                if event.key == pg.K_F11:
                    pg.display.toggle_fullscreen()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if drag_spawn:
                        mouse3_pressed = True
                    else:
                        delete(objects, mouse, surface, window, camera)
                if event.button == 1:
                    if drag_spawn:
                        mouse1_pressed = True
                    else:
                        spawn(selected_object, objects, mouse, surface, window, camera)

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    mouse3_pressed = False
                if event.button == 1:
                    mouse1_pressed = False

            if event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    a_pressed = False
                if event.key == pg.K_d:
                    d_pressed = False
                if event.key == pg.K_s:
                    s_pressed = False
                if event.key == pg.K_w:
                    w_pressed = False
                if event.key == pg.K_z:
                    z_pressed = False
                if event.key == pg.K_x:
                    x_pressed = False

        if mouse1_pressed:
            spawn(selected_object, objects, mouse, surface, window, camera)
        elif mouse3_pressed:
            delete(objects, mouse, surface, window, camera)

        if s_pressed:
            camera[1] += camera_speed
        elif a_pressed:
            camera[0] -= camera_speed
        elif d_pressed:
            camera[0] += camera_speed
        if w_pressed:
            camera[1] -= camera_speed
        if z_pressed:
            camera_speed -= 0.05
        if x_pressed:
            camera_speed += 0.05


        draw(surface, window, objects, background, camera, selected_object, mouse)

    key = lambda object :object.priority
    objects.sort(key=key, reverse=True)

    file = open(map+".txt", "w")
    for object in objects:
        parent_name = object.get_parent()
        class_name = object.get_class()
        x = object.pos[0]
        y = object.pos[1]
        line = "{} {} {} {}\n".format(parent_name, class_name, x, y)
        file.write(line)
    file.close()

    pg.quit()
    quit()

if __name__ == "__main__":
    main(window)
