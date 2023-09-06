import Objects
import pygame as pg
import os
import random
import math
from os import listdir
from os.path import isfile, join
import Characters
from customFunctions import load_sprite_sheets, Background
from Objects import Object

pg.init()
pg.display.set_caption("Editor")

# editor settings:
map = "maps/map1"

# default settings
WIN_SIZE = (1900, 900)
FPS = 60 # 9<FPS<145!!!

# init & load
window = pg.display.set_mode(WIN_SIZE)
surface = pg.Surface((1920, 1080))
file = open(map+".txt", "r")
lines = file.readlines()
file.close()


def draw(surface, window, objects, background, player):
    win_center = (pg.display.get_surface().get_width()//2, pg.display.get_surface().get_height()//2)
    surface_center = (surface.get_width()//2, surface.get_height()//2)
    offset = [win_center[0]-player[0],
              win_center[1] - player[1]]
    surface.blit(background.surface, (offset[0], offset[1]))

    for object in objects:
        object.draw(surface, [0,0], window)

    window.blit(surface,(offset[0], offset[1]))

    pg.display.update()

def spawn(selceted, objects, mouse, surface, window, player):
    win_center = (pg.display.get_surface().get_width()//2, pg.display.get_surface().get_height()//2)
    surface_center = (surface.get_width()//2, surface.get_height()//2)
    offset = [win_center[0]-player[0],
              win_center[1] - player[1]]
    mousex = -offset[0]+mouse[0]
    mousey = player[1] - window.get_height()//2 + mouse[1]
    print(mousex, mousey, objects[0].pos)

def update(objects, delta_time):
    for object in objects:
        object.update(objects, delta_time)


def main(window):
    clock = pg.time.Clock()
    run = True

    objects = []
    background = Background("Tileset", "Night", 32, 32, 0)
    a_pressed = False
    d_pressed = False
    w_pressed = False
    s_pressed = False
    selected_object = None

    paused  = False

    camera = [0, 0]

    # spawns ------------------------------------------------------
    for line in lines:
        if len(line) > 3:
            words = line.split()
            command ="objects.append({}.{}({},{}))".format(words[0], words[1], words[2], words[3])
            exec(command)
    # --------------------------------------------------------------

    while run:
        delta_time = clock.tick(FPS)
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
                if event.key == pg.K_1:
                    selected_object = "Objects.Grass_green"
                if event.key == pg.K_2:
                    selected_object = None
                if event.key == pg.K_3:
                    selected_object = None
                if event.key == pg.K_4:
                    selected_object = None
                if event.key == pg.K_5:
                    selected_object = None
                if event.key == pg.K_6:
                    selected_object = None
                if event.key == pg.K_7:
                    selected_object = None
                if event.key == pg.K_8:
                    selected_object = None
                if event.key == pg.K_9:
                    selected_object = None
                if event.key == pg.K_0:
                    selected_object = None
                if event.key == pg.K_F11:
                    pg.display.toggle_fullscreen()
            if event.type == pg.MOUSEBUTTONUP:
                mouse = pg.mouse.get_pos()
                spawn(selected_object, objects, mouse, surface, window, camera)
            if event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    a_pressed = False
                if event.key == pg.K_d:
                    d_pressed = False
                if event.key == pg.K_s:
                    s_pressed = False
                if event.key == pg.K_w:
                    w_pressed = False

        if not paused:
            if s_pressed:
                camera[1] += 5
            elif a_pressed:
                camera[0] -= 5
            elif d_pressed:
                camera[0] += 5
            if w_pressed:
                camera[1] -= 5

            draw(surface, window, objects, background, camera)

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
