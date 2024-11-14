import json
from os import listdir, path
from math import pi, sqrt
from importlib import util

import pygame as pg
from proto import proto
from eventListen import Events

pg.init()

# Initialisation
pg.display.set_caption("EduBang")
icon = pg.image.load("source/assets/images/icon.png")
pg.display.set_icon(icon)
buttons = []
resolution = (1280, 720)
screen = pg.display.set_mode((resolution), pg.RESIZABLE)
pg.key.set_repeat(500, 50)
pg.font.init()
black = pg.font.SysFont("FixelText-black.otf", 30)
extrabold = pg.font.SysFont("FixelText-ExtraBold.otf", 30)
bold = pg.font.SysFont("FixelText-bold.otf", 30)
semibold = pg.font.SysFont("FixelText-Semibold.otf", 30)
medium = pg.font.SysFont("FixelText-Medium.otf", 30)
regular = pg.font.SysFont("FixelText-Regular.otf", 30)
light = pg.font.SysFont("FixelText-Light.otf", 30)

with proto("Game") as Game:
    @Game
    def quit_algo(self):
        pg.quit()
        quit()

    @Game
    def load(self):

        self.dt = 1
        self.running = True
        self.space = []
        self.Camera = CameraHandler()
        self.window = ""
        self.windows = {}
        self.font = regular
        self.keybinds = {}
        self.keys = {}
        self.invertedKeybinds = {}

        ws = [w for w in listdir("./source/window") if path.isfile(path.join("./source/window", w))]
        for w in ws:
            module_name = w[:-3]
            file_path = path.join("./source/window", w)
            spec = util.spec_from_file_location(module_name, file_path)
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            loadFunction = getattr(module, "load")
            drawFunction = getattr(module, "draw")
            updateFunction = getattr(module, "update")
            self.windows[module_name] = [loadFunction, drawFunction, updateFunction]

        with open("source/data/keybind.json", "r", encoding="utf-8") as f:
            Game.keybinds = json.load(f)
            f.close()

        self.resetKeys()

        self.select("menu")

    @Game
    def resetKeys(self):
        for key in self.keybinds:
            self.keys[key] = False
        keys = self.keybinds.keys()
        values = self.keybinds.values()
        for v, k in zip(values, keys):
            self.invertedKeybinds[v] = k
        return
    
    @Game
    def getKeyFromCode(self, code: int, default = None) -> str:
        return self.invertedKeybinds[code] if code in self.invertedKeybinds else default
    
    @Game
    def getCodeFromKey(self, key: str, default = None) -> int:
        return self.keybinds[key] if key in self.keybinds else default

    @Game
    def draw(self):
        self.windows[self.window][1](screen)
        pg.display.update()

    @Game
    def update(self):
        self.windows[self.window][2]()

    @Game
    def select(self, w):
        if not w in self.windows.keys(): return
        Events.trigger("window", w)
        self.windows[w][0]()
        self.window = w
        return
    
    @Game
    def reset(self):
        self.Camera.reset()
        self.dt = 1
        self.space = []


with proto("CameraHandler") as CameraHandler:
    @CameraHandler
    def new(self):
        self.active = False
        self.x = 0
        self.y = 0
        self.speed = 5
        self.zoom = 1
        self.maxZoom = 1000
        self.minZoom = 0.001
        self.focus = None
        return

    @CameraHandler
    def reset(self):
        self.active = False
        self.x = 0
        self.y = 0
        self.speed = 5
        self.zoom = 1
        self.maxZoom = 1000
        self.minZoom = 0.001
        self.focus = None
        return

Game.load()

@Events.observe
def window(w):
    for i in buttons:
        buttons.remove(i)
    Game.space = []

@Events.observe
def hovering(button):
    if not button in buttons:
        buttons.append(button)
    return

@Events.observe
def unhovering(button):
    if button in buttons:
        buttons.remove(button)
    return

@Events.observe
def keydown(event) -> None:
    code = event.key
    key = Game.getKeyFromCode(code)
    if key:
        Game.keys[key] = True
    return

@Events.observe
def keyup(event) -> None:
    code = event.key
    key = Game.getKeyFromCode(code)
    if key:
        Game.keys[key] = False
    return

@Events.observe
def mousewheel(event) -> None:
    x, y = event.x, event.y
    if not Game.Camera.active: return
    if y == 1 and Game.Camera.zoom < Game.Camera.maxZoom: # scroll vers le haut: zoom
        Game.Camera.zoom *= 1.05
    if y == -1 and Game.Camera.zoom > Game.Camera.minZoom: # scroll vers le bas: dézoom
        Game.Camera.zoom /= 1.05
    return

@Events.observe
def mousebuttondown(event) -> None:
    button = event.button
    x, y = event.pos
    if button in [4, 5]: # les scrolls bas et haut sont considirés comme des cliques de souris
        return
    if button == 1: # clique gauche
        if not Game.Camera.active: return
        for corps in Game.space:
            xC = float((corps.pos[0] + Game.Camera.x / Game.Camera.zoom) * Game.Camera.zoom)
            yC = float((corps.pos[1] + Game.Camera.y / Game.Camera.zoom) * Game.Camera.zoom)
            sqx = (x - xC) ** 2
            sqy = (y - yC) ** 2
            if pi * (corps.radius * Game.Camera.zoom) ** 2 < 10:
                if sqrt(sqx + sqy) < corps.radius // 5:
                    Game.Camera.focus = corps
                    Game.Camera.zoom = 1
                    break
            if sqrt(sqx + sqy) < corps.radius * Game.Camera.zoom:
                Game.Camera.focus = corps
                Game.Camera.zoom = 1
                break
        else:
            Game.Camera.focus = None
    return

def update() -> None:
    Game.update()

def draw() -> None:
    Game.draw()

# Boucle principale
def gameLoop() -> None:
    while Game.running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Game.running = False

            if event.type == pg.KEYDOWN:
                Events.trigger("keydown", event) # key, unicode
            if event.type == pg.KEYUP:
                Events.trigger("keyup", event) # key
            if event.type == pg.MOUSEWHEEL:
                Events.trigger("mousewheel", event) # x, y
            if event.type == pg.MOUSEBUTTONDOWN:
                Events.trigger("mousebuttondown", event) # pos, button
            if event.type == pg.MOUSEBUTTONUP:
                Events.trigger("mousebuttonup", event) # pos, button
            if event.type == pg.MOUSEMOTION:
                Events.trigger("mousemotion", event) # pos
        
        if Game.Camera.active:
            if Game.keys["cameraUp"]: # faire monter la caméra
                Game.Camera.y += Game.Camera.speed
            if Game.keys["cameraLeft"]: # faire aller la caméra à gauche
                Game.Camera.x += Game.Camera.speed
            if Game.keys["cameraDown"]: # faire descendre la caméra
                Game.Camera.y -= Game.Camera.speed
            if Game.keys["cameraRight"]: # faire aller la caméra à droite
                Game.Camera.x -= Game.Camera.speed

            if Game.Camera.focus is not None:
                midScreenX = screen.get_width() // 2
                midScreenY = screen.get_height() // 2
                Game.Camera.x = midScreenX - Game.Camera.focus.pos[0] * Game.Camera.zoom
                Game.Camera.y = midScreenY - Game.Camera.focus.pos[1] * Game.Camera.zoom

        if len(buttons) == 0: # Si la souris ne hover plus rien
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        draw()
        update()

gameLoop()

Game.quit_algo()