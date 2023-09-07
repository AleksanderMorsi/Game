import os
import pygame as pg

def flip_sprites(sprites):
    return [pg.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=True, scale=1):
    # gives -> {"spriteSetName":[sprite1,sprite2...],...}
    path = "assets/" + dir1 + "/" + dir2
    images = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pg.image.load(os.path.join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            for j in range(sprite_sheet.get_height() // height):
                surface = pg.Surface((width, height), pg.SRCALPHA, 32)
                rect = pg.Rect(i * width, j * height, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pg.transform.scale_by(surface, scale))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip_sprites(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites
