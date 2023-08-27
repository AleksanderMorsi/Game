import pygame as pg
import os
import random
import math
from os import listdir
from os.path import isfile, join
import Characters
from customFunctions import load_sprite_sheets, Background
from Objects import Object

# to do:
# - add animation mechanic to character class

pg.init()
pg.display.set_caption("Game")

# default settings
WIN_SIZE = (1900, 900)
FPS = 60

# init & load
window = pg.display.set_mode(WIN_SIZE, pg.RESIZABLE)
surface = pg.Surface((1920, 1080))

def draw(surface, window, objects, background):
    win_center = (window.get_width()//2, window.get_height()//2)
    surface_center = (surface.get_width()//2, surface.get_height()//2)
    surface.blit(background.surface, (-win_center[0]+surface_center[0], -win_center[1]+surface_center[1]))

    for object in objects:
        object.draw(surface)

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
    objects.append(Object("Tileset", "Night", 32, 32,1000, 800))
    objects.append(Object("Tileset", "Night", 32, 32,1064, 800))
    objects.append(Object("Tileset", "Night", 32, 32,1128, 800))
    objects.append(Object("Tileset", "Night", 32, 32,968, 800))

    player = Characters.Player("MainCharacters", "Knight_1", 1000, 0, 10, 10)
    objects.append(player)

    while run:
        delta_time = clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                    break
                if event.key == pg.K_SPACE:
                    player.jump()
            if event.type == pg.VIDEORESIZE:
                background.update()

        update(objects, delta_time)
        draw(surface, window, objects, background)


    pg.quit()
    quit()

if __name__ == "__main__":
    main(window)
