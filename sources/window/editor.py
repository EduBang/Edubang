from json import load as loadJson
from os import listdir, path

import pygame as pg
from eventListen import Events

from main import Game, getFont
from shared.components.Corps import Corps
from shared.utils.utils import DataKeeper, Button, spacePosToScreenPos, getSize, Inventory, screenPosToSpacePos

dk = DataKeeper()
dk.body = None
dk.inventory = None

interface: list = []

unitFont = getFont("Regular", 12)

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
    if Game.keys["openInventory"]:
        dk.inventory.active = not dk.inventory.active

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
    return

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

    inventory = Inventory()
    dk.inventory = inventory
    interface.append(inventory)
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))

    drawGrid()

    for corps in Game.space:
        corps.draw(screen, Game.Camera)

    if dk.body:
        pos = pg.mouse.get_pos()
        radius: float | int = dk.body["radius"]
        pg.draw.circle(screen, (255, 255, 255), pos, radius * Game.Camera.zoom, 1)
    
    for element in interface:
        element.draw()
    return

def update() -> None:
    return