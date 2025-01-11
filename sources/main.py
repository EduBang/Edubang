from ctypes import pythonapi, c_long, py_object
from json import load as loadJson
from json import dumps
from os import listdir, path, environ, getlogin
from platform import system
from sys import exit
from math import pi, sqrt
from importlib import util
from random import choice
from copy import deepcopy

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame as pg
from proto import proto
from eventListen import Events

pg.init()

# Initialisation
pg.display.set_caption("EduBang")
icon = pg.image.load("data/images/appicon.png")
pg.display.set_icon(icon)
MUSIC_END_EVENT: int = pg.USEREVENT + 1
hoverable: list = []
screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
pg.key.set_repeat(500, 50)

pg.font.init()
pg.mixer.init()
pg.mixer.music.set_endevent(MUSIC_END_EVENT)

clock = pg.time.Clock()

def getFont(font, size: int = 16) -> pg.font.Font:
    return pg.font.Font("data/fonts/Open_Sans/OpenSans-%s.ttf" % font, size)

with proto("Game") as Game:
    @Game
    def quit(self) -> None:
        isAlive = getattr(self.subprocess, "is_alive", False)
        if isAlive:
            threadId = self.subprocess.ident
            pythonapi.PyThreadState_SetAsyncExc(c_long(threadId), py_object(SystemExit))
            self.subprocess = None
        pg.quit()
        exit(0)
        return

    @Game
    def load(self) -> None:
        self.timeScale = 1 # seconde
        self.deltaTime = 0 # seconde
        self.DT = self.deltaTime * self.timeScale
        self.running = True
        self.space = []
        self.originSpace = []
        self.Camera = CameraHandler()
        self.window = ""
        self.windows = {}
        self.font = getFont("Medium")
        self.italic = getFont("MediumItalic")
        self.title = getFont("Regular", 32)
        self.keybinds = {}
        self.keys = {}
        self.invertedKeybinds = {}
        self.settings = {}
        self.musics = []
        self.music = None
        self.screen = screen
        self.os = system()
        self.user = getlogin()
        self.tmusic = None
        self.pause = False
        self.subprocess = None
        self.screenSize = screen.get_size()

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
                Game.keybinds.update(loadJson(f))
                f.close()

        with open("data/settings.json", "r", encoding="utf-8") as f:
            Game.settings = loadJson(f)
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
        self.invertedKeybinds = {}
        for key in self.keybinds:
            self.keys[key] = False
        for k, v in self.keybinds.items():
            self.invertedKeybinds[tuple(v["code"])] = k
        return
    
    @Game
    def getKeyFromCode(self, keys: list[int], default = None) -> str:
        keys = tuple(keys)
        return self.invertedKeybinds[keys] if keys in self.invertedKeybinds else default
    
    @Game
    def getCodeFromKey(self, key: str, default = None) -> list[int]:
        return self.keybinds[key] if key in self.keybinds else default

    @Game
    def draw(self) -> None:
        self.windows[self.window][1](screen)
        if self.tmusic and self.settings["volume"] != 0:
            Game.tmusic -= (Game.deltaTime * 2.195)
            width, height = self.screenSize
            text: str = "Playing %s" % self.music[12:-4]
            surface = Game.italic.render(text, False, (255, 255, 255))
            surface.set_alpha(int(255 * Game.tmusic / 5))
            tW, tH = Game.italic.size(text)
            screen.blit(surface, (width // 2 - tW // 2, height // 2 - tH // 2 + 200))
            if Game.tmusic <= 0:
                Game.tmusic = None
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
        self.pause = False
        return
    
    @Game
    def resetSpace(self) -> None:
        self.space = deepcopy(self.originSpace)
        return

    @Game
    def changeMusic(self) -> None:
        self.music = choice(self.musics)
        return
    
    @Game
    def playMusic(self) -> None:
        pg.mixer.music.load(self.music)
        pg.mixer.music.play()
        self.tmusic = 5
        return

    @Game
    def getHeaviest(self):
        c, m = self.space[0], self.space[0].mass
        for corps in self.space:
            if corps.mass > m:
                c, m = corps, corps.mass
        return c

    @Game
    def resetKeybinds(self):
        if self.os != "Windows": return
        camera: dict = {"cameraUp": {"name": "D\u00e9placement vers le haut", "code": [122], "key": ["z"]}, "cameraLeft": {"name": "D\u00e9placement vers la gauche", "code": [113], "key": ["q"]}, "cameraDown": {"name": "D\u00e9placement vers le bas", "code": [115], "key": ["s"]}, "cameraRight": {"name": "D\u00e9placement vers la droite", "code": [100], "key": ["d"]}, "resetCamera": {"name": "R\u00e9initialiser la cam\u00e9ra", "code": [114], "key": ["r"]}, "zoomIn": {"name": "Zoomer la cam\u00e9ra", "code": [1073741911], "key": ["+"]}, "zoomOut": {"name": "D\u00e9zoomer la cam\u00e9ra", "code": [45], "key": ["-"]}}
        editor: dict = {"inventory": {"name": "Ouvrir l'inventaire", "code": [9], "key": ["tab"]}, "delete": {"name": "Supprimer un corps", "code": [102], "key": ["f"]}, "selectAll": {"name": "Tout s\u00e9lectionner", "code": [1073742048, 97], "key": ["ctrl", "a"]}, "save": {"name": "Sauvegarder", "code": [1073742048, 115], "key": ["ctrl", "s"]}}
        simulation: dict = {"increaseTime": {"name": "Acc\u00e9l\u00e9rer le temps", "code": [101], "key": ["e"]}, "decreaseTime": {"name": "D\u00e9c\u00e9l\u00e9rer le temps", "code": [97], "key": ["a"]}, "pause": {"name": "Mettre la simulation en pause", "code": [32], "key": ["espace"]}, "resetSimulation": {"name": "R\u00e9initialiser la simulation", "code": [103], "key": ["g"]}}
        with open("data/settings/camera.json", "w", encoding="utf-8") as wf:
            wf.write(dumps(camera))
            wf.close()
        with open("data/settings/editor.json", "w", encoding="utf-8") as wf:
            wf.write(dumps(editor))
            wf.close()
        with open("data/settings/simulation.json", "w", encoding="utf-8") as wf:
            wf.write(dumps(simulation))
            wf.close()
        Game.keybinds = {**camera, **editor, **simulation}
        Game.resetKeys()
        return


with proto("CameraHandler") as CameraHandler:
    @CameraHandler
    def new(self) -> None:
        self.active = False
        self.x = 0
        self.y = 0
        self.speed = 5
        self.zoom = 0.00_000_1
        self.maxZoom = 200 # 10_000_000; Voir Trello
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
        self.maxZoom = 200 # 10_000_000; Voir Trello
        self.minZoom = 0.00_000_01
        self.focus = None
        return

Game.load()

@Events.observe
def window(w) -> None:
    hoverable.clear()
    return

@Events.observe
def hovering(element) -> None:
    if not element in hoverable:
        hoverable.append(element)
    return

@Events.observe
def unhovering(element) -> None:
    if element in hoverable:
        hoverable.remove(element)
    return

@Events.observe
def mousewheel(event) -> None:
    if not Game.Camera.active: return
    x, y = event.x, event.y
    if y == 1 and Game.Camera.zoom < Game.Camera.maxZoom: # scroll vers le haut: zoom
        Game.Camera.zoom *= 1.05
    if y == -1 and Game.Camera.zoom > Game.Camera.minZoom: # scroll vers le bas: dézoom
        Game.Camera.zoom /= 1.05
    return

@Events.observe
def mousebuttondown(event) -> None:
    if Game.window != "sandbox": return
    button = event.button
    x, y = event.pos
    if button == 1: # clique gauche
        if not Game.Camera.active: return
        for corps in Game.space:
            xC = (corps.pos[0] + Game.Camera.x / Game.Camera.zoom) * Game.Camera.zoom
            yC = (corps.pos[1] + Game.Camera.y / Game.Camera.zoom) * Game.Camera.zoom
            sqx = (x - xC) ** 2
            sqy = (y - yC) ** 2
            if pi * (corps.radius * Game.Camera.zoom) ** 2 < 10:
                if sqrt(sqx + sqy) < 10:
                    Game.Camera.focus = corps
                    Game.Camera.zoom = 1 / corps.radius * 51
                    break
            if sqrt(sqx + sqy) < corps.radius * Game.Camera.zoom:
                Game.Camera.focus = corps
                Game.Camera.zoom = 1 / corps.radius * 51
                break
    return

# Boucle principale
def main() -> None:
    while Game.running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Game.running = False
            if event.type == pg.KEYDOWN:
                Events.trigger("keydown", event)
            if event.type == pg.KEYUP:
                Events.trigger("keyup", event)
            if event.type == pg.MOUSEWHEEL:
                Events.trigger("mousewheel", event)
            if event.type == pg.MOUSEBUTTONDOWN:
                Events.trigger("mousebuttondown", event)
            if event.type == pg.MOUSEBUTTONUP:
                Events.trigger("mousebuttonup", event)
            if event.type == pg.MOUSEMOTION:
                Events.trigger("mousemotion", event)
            if event.type == MUSIC_END_EVENT:
                Game.changeMusic()
                Game.playMusic()

        if len(hoverable) == 0:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        # Constante de calibrage du temps
        Game.deltaTime = clock.tick(60) / 2195 # (1000 * 2.195)
        Game.DT = Game.deltaTime * Game.timeScale

        if Game.Camera.active:
            if Game.keys["cameraUp"]:
                Game.Camera.y += Game.Camera.speed
            if Game.keys["cameraLeft"]:
                Game.Camera.x += Game.Camera.speed
            if Game.keys["cameraDown"]:
                Game.Camera.y -= Game.Camera.speed
            if Game.keys["cameraRight"]:
                Game.Camera.x -= Game.Camera.speed

        Game.screenSize = screen.get_size()

        Game.draw()
        if Game.pause: continue
        Game.update()
    
    Game.quit()
    return

main()
