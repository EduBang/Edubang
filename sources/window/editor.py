from json import load as loadJson
from os import listdir, path

import pygame as pg
from eventListen import Events

from main import Game, getFont
from shared.utils.utils import DataKeeper, Button, spacePosToScreenPos, getSize

unitFont = getFont("Regular", 12)

def drawGrid() -> None:
    w, distance, unit = getSize()
    screen = Game.screen
    width, height = screen.get_size()
    k: int = int(width // w)
    for i in range(-5 * k, 5 * k):
        color: tuple[int, int, int] = (100, 100, 100) if i != 0 else (255, 255, 255)
        s: float = i * w / Game.Camera.zoom
        pg.draw.line(screen, color, spacePosToScreenPos((s, -Game.Camera.y / Game.Camera.zoom)), spacePosToScreenPos((s, (height - Game.Camera.y) / Game.Camera.zoom)), 1)
        pg.draw.line(screen, color, spacePosToScreenPos((-Game.Camera.x / Game.Camera.zoom, s)), spacePosToScreenPos(((width - Game.Camera.x) / Game.Camera.zoom, s)), 1)
        text: str = "%s %s" % (abs(distance * i), unit)
        surface = unitFont.render(text, False, (255, 255, 255))
        screen.blit(surface, spacePosToScreenPos((s, 0)))
        screen.blit(surface, spacePosToScreenPos((0, s)))
    return

def load() -> None:
    Game.Camera.active = True
    Game.Camera.zoom = 1
    w, h = Game.screen.get_size()
    Game.Camera.x = w // 2
    Game.Camera.y = h // 2
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))

    drawGrid()
    return

def update() -> None:
    return