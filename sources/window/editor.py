from json import load as loadJson
from os import listdir, path
from math import pi, sqrt

import pygame as pg
from eventListen import Events

from main import Game, getFont
from shared.components.Corps import Corps
from shared.components.Prediction import predict
from shared.utils.utils import DataKeeper, Button, spacePosToScreenPos, getSize, Inventory, screenPosToSpacePos, Input

dk = DataKeeper()
dk.body = None
dk.inventory = None
dk.mouseselection = None
dk.selected = []

interface: list = []

unitFont = getFont("Regular", 12)

def minimum(startPos, endPos) -> tuple:
    x1, y1 = startPos
    x2, y2 = endPos
    return (min(x1, x2), min(y1, y2))

def maximum(startPos, endPos) -> tuple:
    x1, y1 = startPos
    x2, y2 = endPos
    return (max(x1, x2), max(y1, y2))

@Events.observe
def keydown(event) -> None:
    if Game.window != "editor": return
    keys = []
    
    mods = pg.key.get_mods()
    if mods & pg.KMOD_LCTRL:
        keys.append(0x400000e0)
    if mods & pg.KMOD_LALT:
        keys.append(0x400000e2)
    keys.append(event.key)

    key = Game.getKeyFromCode(keys)
    if key:
        Game.keys[key] = True
    if Game.keys["inventory"]:
        dk.inventory.active = not dk.inventory.active
    if Game.keys["delete"]:
        for corps in dk.selected:
            Game.space.remove(corps)
        dk.selected.clear()

    key = event.key
    
    if key == pg.K_KP_PLUS and Game.Camera.zoom < Game.Camera.maxZoom:
        Game.Camera.zoom *= 1.05
    elif key == pg.K_KP_MINUS and Game.Camera.zoom > Game.Camera.minZoom:
        Game.Camera.zoom /= 1.05
    return

@Events.observe
def inventory(body) -> None:
    dk.body = body
    Game.Camera.zoom = 1 / body["radius"] * 51
    return

@Events.observe
def mousebuttondown(event) -> None:
    if Game.window != "editor": return
    button = event.button
    pos = event.pos
    if button != 1: return
    if dk.inventory.active: return
    body = dk.body
    if body:
        pos = event.pos
        corps = Corps(body["mass"], body["radius"], screenPosToSpacePos(pos), body["color"], (0, 0))
        Game.space.append(corps)
        dk.body = None
    else:
        for corps in Game.space:
            x, y = spacePosToScreenPos(corps.pos)
            sqx, sqy = (pos[0] - x) ** 2, (pos[1] - y) ** 2
            if pi * (corps.radius * Game.Camera.zoom) ** 2 < 10:
                if sqrt(sqx + sqy) < 10:
                    Game.Camera.focus = corps
                    break
            if sqrt(sqx + sqy) < corps.radius * Game.Camera.zoom:
                Game.Camera.focus = corps
                break
        else:
            Game.Camera.focus = None
            dk.selected.clear()
            dk.mouseselection = screenPosToSpacePos(pos)
    return

@Events.observe
def mousebuttonup(event) -> None:
    if Game.window != "editor": return
    button = event.button
    if button != 1: return
    if dk.mouseselection:
        dk.mouseselection = None
    return

def drawGrid() -> None:
    w, distance, unit = getSize()
    screen = Game.screen
    width, height = Game.screenSize
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

def drawMouseSelection() -> None:
    if dk.mouseselection:
        startPos = spacePosToScreenPos(dk.mouseselection)
        endPos = pg.mouse.get_pos()
        pos = minimum(startPos, endPos)
        w, h = abs(endPos[0] - startPos[0]), abs(endPos[1] - startPos[1])
        surface = pg.Surface((w, h))
        surface.set_alpha(100)
        surface.fill((54, 156, 235))
        Game.screen.blit(surface, pos)
    return

def drawSelected() -> None:
    for selected in dk.selected:
        pg.draw.circle(Game.screen, (255, 255, 255), spacePosToScreenPos(selected.pos), selected.radius * Game.Camera.zoom, 1)
    return

def load() -> None:
    Game.Camera.active = True
    Game.Camera.zoom = 1
    w, h = Game.screenSize
    Game.Camera.x = w // 2
    Game.Camera.y = h // 2

    inventory = Inventory()
    dk.inventory = inventory
    interface.append(inventory)
    return

def stats(corps, width, height) -> None:
    screen = Game.screen

    pg.draw.rect(screen, (10, 9, 9), (width - 350, 0, 350, height))
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))
    width, height = Game.screenSize

    drawGrid()

    for corps in Game.space:
        corps.draw(screen, Game.Camera)

    drawSelected()
    drawMouseSelection()

    if dk.body:
        pos = pg.mouse.get_pos()
        radius: float | int = dk.body["radius"]
        pg.draw.circle(screen, (255, 255, 255), pos, radius * Game.Camera.zoom, 1)

    if Game.Camera.focus:
        stats(Game.Camera.focus, width, height)

    pg.draw.rect(screen, (10, 9, 9), (0, 0, width, 100))
    pg.draw.line(screen, (255, 255, 255), (0, 100), (width, 100))

    for element in interface:
        element.draw()
    return

def update() -> None:
    if dk.mouseselection:
        pos = screenPosToSpacePos(pg.mouse.get_pos())
        mini = minimum(dk.mouseselection, pos)
        maxi = maximum(dk.mouseselection, pos)
        for corps in Game.space:
            if mini[0] < corps.pos[0] < maxi[0] and mini[1] < corps.pos[1] < maxi[1]:
                if corps not in dk.selected:
                    dk.selected.append(corps)
            else:
                if corps in dk.selected:
                    dk.selected.remove(corps)
    return