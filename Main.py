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
pg.display.set_caption("Game")

# default settings
WIN_SIZE = (1900, 900)
FPS = 60 # 9<FPS<145!!!

# init & load
window = pg.display.set_mode(WIN_SIZE)
surface = pg.Surface((1920, 1080))

def draw(surface, window, objects, background, player):
    win_center = (pg.display.get_surface().get_width()//2, pg.display.get_surface().get_height()//2)
    surface_center = (surface.get_width()//2, surface.get_height()//2)
    offset = [win_center[0]-player.pos[0]-(player.size[0]//2),
              win_center[1] - player.pos[1]]
    surface.blit(background.surface, (
        -win_center[0]+surface_center[0], -win_center[1]+surface_center[1]))

    for object in objects:
        object.draw(surface, offset)

    window.blit(surface,(win_center[0]-surface_center[0], win_center[1]-surface_center[1]))
    pg.display.update()

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

    paused  = False

    # spawns ------------------------------------------------------
    for i in range(surface.get_width()*5//64):
        objects.append(Objects.Grass_green(-surface.get_width()*2+i*64, surface.get_height()-64))

    objects.append(Characters.Knight(1200, surface.get_height()-64 - 86))
    objects.append(Characters.Knight(2200, surface.get_height()-64 - 86))
    objects.append(Characters.Knight(-1350, surface.get_height()-64 - 86))

    player = Characters.Player(1000, surface.get_height()-64 - 86, debug=True)
    objects.append(player)
    for object in objects:
        object.env_update(FPS)
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
                    player.attack()
                if event.key == pg.K_w:
                    w_pressed = True
                if event.key == pg.K_s:
                    s_pressed = True
                if event.key == pg.K_a:
                    a_pressed = True
                if event.key == pg.K_d:
                    d_pressed = True
                if event.key == pg.K_F11:
                    pg.display.toggle_fullscreen()
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
                player.defend(True)
            elif a_pressed:
                player.moveleft()
            elif d_pressed:
                player.moveright()
            if not s_pressed:
                player.defend(False)
            if w_pressed:
                player.jump()

            update(objects, delta_time)
            draw(surface, window, objects, background, player)


    pg.quit()
    quit()

if __name__ == "__main__":
    main(window)
