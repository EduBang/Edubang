import json
from os import listdir, path, environ
from math import pi, sqrt
from importlib import util
from random import choice

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide" # pour cacher le message de PyGame quand le programme se lance

import pygame as pg
from proto import proto
from eventListen import Events

from shared.components.Physics import Physics

pg.init()

# Initialisation
pg.display.set_caption("EduBang")
icon = pg.image.load("data/images/appicon.png")
pg.display.set_icon(icon)
MUSIC_END_EVENT = pg.USEREVENT + 1
buttons = []
resolution = (1280, 720)
screen = pg.display.set_mode((resolution), pg.RESIZABLE)
pg.key.set_repeat(500, 50)

pg.font.init()
pg.mixer.init()
pg.mixer.music.set_endevent(MUSIC_END_EVENT)

clock = pg.time.Clock()
FONTS: dict[str, int] = {
    "SemiBoldItalic": "data/fonts/Open_Sans/OpenSans-SemiBoldItalic.ttf",
    "SemiBold": "data/fonts/Open_Sans/OpenSans-SemiBold.ttf",
    "Regular": "data/fonts/Open_Sans/OpenSans-Regular.ttf",
    "MediumItalic": "data/fonts/Open_Sans/OpenSans-MediumItalic.ttf",
    "Medium": "data/fonts/Open_Sans/OpenSans-Medium.ttf",
    "LightItalic": "data/fonts/Open_Sans/OpenSans-LightItalic.ttf",
    "Light": "data/fonts/Open_Sans/OpenSans-Light.ttf",
    "Italic": "data/fonts/Open_Sans/OpenSans-Italic.ttf",
    "ExtraBoldItalic": "data/fonts/Open_Sans/OpenSans-ExtraBoldItalic.ttf",
    "ExtraBold": "data/fonts/Open_Sans/OpenSans-ExtraBold.ttf",
    "BoldItalic": "data/fonts/Open_Sans/OpenSans-BoldItalic.ttf",
    "Bold": "data/fonts/Open_Sans/OpenSans-Bold.ttf",
}

def getFont(font, size: int = 16) -> pg.font.Font:
    return pg.font.Font(FONTS[font], size)

font = getFont("Medium")

with proto("Game") as Game:
    @Game
    def quit_algo(self) -> None:
        pg.quit()
        quit()
        return

    @Game
    def load(self) -> None:

        self.timeScale = 1 # seconde
        self.deltaTime = 0 # seconde
        self.running = True
        self.space = []
        self.Camera = CameraHandler()
        self.window = ""
        self.windows = {}
        self.font = font
        self.keybinds = {}
        self.keys = {}
        self.invertedKeybinds = {}
        self.settings = {}
        self.musics = []
        self.music = None
        self.screen = screen

        ws = [w for w in listdir("sources/window") if path.isfile(path.join("sources/window", w))]
        for w in ws:
            module_name = w[:-3]
            file_path = path.join("./sources/window", w)
            spec = util.spec_from_file_location(module_name, file_path)
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            loadFunction = getattr(module, "load")
            drawFunction = getattr(module, "draw")
            updateFunction = getattr(module, "update")
            self.windows[module_name] = [loadFunction, drawFunction, updateFunction]

        keybindsFiles = [path.join("data/settings", f) for f in listdir("data/settings") if path.isfile(path.join("data/settings", f))]
        for keybindFile in keybindsFiles:
            with open(keybindFile, "r", encoding="utf-8") as f:
                Game.keybinds.update(json.load(f))
                f.close()

        with open("data/settings.json", "r", encoding="utf-8") as f:
            Game.settings = json.load(f)
            f.close()

        musics = [path.join("data/musics", f) for f in listdir("data/musics") if path.isfile(path.join("data/musics", f))]
        for music in musics:
            self.musics.append(music)
        pg.mixer.music.set_volume(self.settings["volume"] / 100)
        self.resetKeys()
        self.select("menu")

        self.changeMusic()
        self.playMusic()
        return

    @Game
    def resetKeys(self) -> None:
        for key in self.keybinds:
            self.keys[key] = False
        for k, v in self.keybinds.items():
            self.invertedKeybinds[v["code"]] = k
        return
    
    @Game
    def getKeyFromCode(self, code: int, default = None) -> str:
        return self.invertedKeybinds[code] if code in self.invertedKeybinds else default
    
    @Game
    def getCodeFromKey(self, key: str, default = None) -> int:
        return self.keybinds[key] if key in self.keybinds else default

    @Game
    def draw(self) -> None:
        self.windows[self.window][1](screen)
        pg.display.update()
        return

    @Game
    def update(self) -> None:
        self.windows[self.window][2]()
        return

    @Game
    def select(self, w) -> None:
        if not w in self.windows.keys(): return
        Events.trigger("window", w)
        self.windows[w][0]()
        self.window = w
        return
    
    @Game
    def reset(self) -> None:
        self.Camera.reset()
        self.timeScale = 1
        self.space = []
        return

    @Game
    def normalizeCinetic(self, corps = None) -> dict:
        values = {}
        for i in self.space:
            cinetic_energy = Physics.get_cinetic_energy(i.mass, Physics.get_velocity(i.path[-2], i.path[-1], Game.dt))
            values[i] = cinetic_energy

        valuesList = values.values()
        originalMin = min(valuesList)
        originalMax = max(valuesList)

        d = {}
        if originalMax - originalMin == 0:
            for value in values:
                d[value] = 0
        else:
            for value in values:
                d[value] = (values[value] - originalMin) / (originalMax - originalMin) * 100

        if corps and corps in d:
            return d[corps]
        return d

    @Game
    def changeMusic(self) -> None:
        self.music = choice(self.musics)
        return
    
    @Game
    def playMusic(self) -> None:
        pg.mixer.music.load(self.music)
        pg.mixer.music.play()
        return


with proto("CameraHandler") as CameraHandler:
    @CameraHandler
    def new(self) -> None:
        self.active = False
        self.x = 0
        self.y = 0
        self.speed = 5
        self.zoom = 0.00_000_1
        self.maxZoom = 10_000_000
        self.minZoom = 0.00_000_01
        self.focus = None
        return

    @CameraHandler
    def reset(self) -> None:
        self.active = False
        self.x = 0
        self.y = 0
        self.speed = 5
        self.zoom = 0.00_000_1
        self.maxZoom = 10_000_000
        self.minZoom = 0.00_000_01
        self.focus = None
        return

Game.load()

@Events.observe
def window(w) -> None:
    for i in buttons:
        buttons.remove(i)
    Game.space = []
    return

@Events.observe
def hovering(button) -> None:
    if not button in buttons:
        buttons.append(button)
    return

@Events.observe
def unhovering(button) -> None:
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
    if button in [4, 5]: # les scrolls bas et haut sont considérés comme des cliques de souris
        return
    if button == 1: # clique gauche
        if not Game.Camera.active: return
        for corps in Game.space:
            xC = float((corps.pos[0] + Game.Camera.x / Game.Camera.zoom) * Game.Camera.zoom)
            yC = float((corps.pos[1] + Game.Camera.y / Game.Camera.zoom) * Game.Camera.zoom)
            sqx = (x - xC) ** 2
            sqy = (y - yC) ** 2
            if pi * (corps.radius * Game.Camera.zoom) ** 2 < 10:
                if sqrt(sqx + sqy) < 10:
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
    return

def draw() -> None:
    Game.draw()
    return

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
            if event.type == MUSIC_END_EVENT:
                Game.changeMusic()
                Game.playMusic()

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

        # Constante de calibrage du temps
        Game.deltaTime = clock.tick(60) / (1000 * 2.195)

        draw()
        update()
    return

gameLoop()

Game.quit_algo()