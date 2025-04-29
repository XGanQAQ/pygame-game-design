import os
import pygame as pg

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    """
    loads an image, prepares it for play
    执行的路径为~/assets/images/file
    所以直接传入文件名即可
    """
    file = os.path.join(main_dir, "assets/images", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()


def load_sound(file):
    """
    because pygame can be compiled without mixer.
    执行的路径为~/assets/musics/file
    所以直接传入文件名即可
    """

    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "assets/musics", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print(f"Warning, unable to load, {file}")
    return None