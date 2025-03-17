# Projet : EduBang
# Auteurs : Anaël Pernot-Chevillard, Sacha Fréguin, Néji Lim

from ctypes import pythonapi, c_long, py_object
from inspect import stack
from json import load as loadJson
from json import dumps
from os import listdir, path, environ, getlogin, sep
from platform import system
from sys import exit
from math import pi, sqrt
from importlib import util
from random import choice
from copy import deepcopy

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from PIL import Image
import pygame as pg
from proto import proto
from eventListen import Events

def p(path: str) -> str:
    """
    Fonction permettant de formater les chemins comme spécifié dans le Règlement des Trophées NSI 4ème Édition (3.3.4. Inter-opérabilité)
    Le nom de cette fonction est intentionnellement courte pour optimiser le temps de développement
    (p)ath -> p

    Arguments:
        path (str): Chemins à formater
    
    Retourne:
        str: Le chemin
    """
    return sep.join(path.split("/"))

pg.init()

# Initialisation
pg.display.set_caption("EduBang")
icon = pg.image.load(p("data/images/appicon.png"))
pg.display.set_icon(icon)
MUSIC_END_EVENT: int = pg.USEREVENT + 1
hoverable: list = []
screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
pg.key.set_repeat(500, 50)

pg.font.init()
try:
    pg.mixer.init()
    pg.mixer.music.set_endevent(MUSIC_END_EVENT)
except pg.error as e:
    print("> Impossible d'initialiser le module mixer de PyGame : %s" % e)

clock = pg.time.Clock()

brand = Image.open(p("data/images/brand.png"))
brand = brand.resize((175, 41), Image.Resampling.BICUBIC)
brand = pg.image.fromstring(brand.tobytes(), brand.size, brand.mode)

languages: dict = {}

languageFiles = [path.join(p("data/language"), f) for f in listdir(p("data/language")) if path.isfile(path.join(p("data/language"), f))]
for languageFile in languageFiles:
    with open(languageFile, mode="r", encoding="utf-8") as f:
        languages[languageFile[14:-5]] = loadJson(f)
        f.close()

def getFont(font, size: int = 16, *, header: str = "OpenSans") -> pg.font.Font:
    """
    Fonction permettant de récupérer un type et une taille de police dans OpenSans

    Arguments:
        font (str): Type de police
        size (int): Taille de la police

    Retourne:
        pg.font.Font: Police
    """
    return pg.font.Font(p("data/fonts/%s/%s-%s.ttf" % (header, header, font)), size)

def l(ident: str, *, header: str = None) -> str:
    """
    Fonction permettant de récupérer la traduction d'un texte à partir de son code d'identification
    Le nom de cette fonction est intentionnellement courte pour optimiser le temps de développement
    (l)anguage -> l

    Argument:
        ident (str): Code d'identification
        header (str): L'entête du code d'identification
    
    Retourne:
        str: Texte dans la langue traduite
    """
    window = header or Game.window or path.basename(stack()[1].filename)[:-3]
    return languages[Game.language]["%s_%s" % (window, ident)]

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
        self.music = []
        self.sound = None
        self.screen = screen
        self.os = system()
        self.user = getlogin()
        self.tmusic = None
        self.pause = False
        self.subprocess = None
        self.screenSize = screen.get_size()
        self.language = "fr"
        self.rmb = None
        self.ormb = None

        ws = [w for w in listdir(p("sources/interface")) if path.isfile(path.join(p("sources/interface"), w))]
        for w in ws:
            module_name = w[:-3]
            file_path = path.join(p("sources/interface"), w)
            spec = util.spec_from_file_location(module_name, file_path)
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            loadFunction = getattr(module, "load")
            drawFunction = getattr(module, "draw")
            updateFunction = getattr(module, "update")
            self.windows[module_name] = (loadFunction, drawFunction, updateFunction)

        keybindsFiles = [path.join(p("data/settings"), f) for f in listdir(p("data/settings")) if path.isfile(path.join(p("data/settings"), f))]
        for keybindFile in keybindsFiles:
            with open(keybindFile, "r", encoding="utf-8") as f:
                Game.keybinds.update(loadJson(f))
                f.close()

        with open(p("data/settings.json"), "r", encoding="utf-8") as f:
            Game.settings = loadJson(f)
            f.close()

        music = [path.join(p("data/music"), f) for f in listdir(p("data/music")) if path.isfile(path.join(p("data/music"), f))]
        for sound in music:
            self.music.append(sound)
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
            text: str = "%s %s" % (l("playing", header="main"), self.sound[11:-4])
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
        self.window = w
        Events.trigger("window", w)
        self.windows[w][0]()
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
        self.sound = choice(self.music)
        return
    
    @Game
    def playMusic(self) -> None:
        pg.mixer.music.load(self.sound)
        pg.mixer.music.play()
        self.tmusic = 5
        return

    @Game
    def getHeaviest(self):
        return sorted(self.space, key=lambda corps: corps.mass, reverse=True)[0]

    @Game
    def resetKeybinds(self):
        camera: dict = {"cameraUp": {"name": "CDU", "code": [122], "key": ["z"]}, "cameraLeft": {"name": "CDL", "code": [113], "key": ["q"]}, "cameraDown": {"name": "CDD", "code": [115], "key": ["s"]}, "cameraRight": {"name": "CDR", "code": [100], "key": ["d"]}, "resetCamera": {"name": "CRC", "code": [114], "key": ["r"]}, "zoomIn": {"name": "CZC", "code": [1073741911], "key": ["+"]}, "zoomOut": {"name": "CDC", "code": [45], "key": ["-"]}}
        editor: dict = {"delete": {"name": "ED", "code": [127], "key": ["del"]}, "selectAll": {"name": "EGA", "code": [1073742048, 97], "key": ["ctrl", "a"]}, "save": {"name": "ESA", "code": [1073742048, 115], "key": ["ctrl", "s"]}}
        main: dict = {"help": {"name": "MH", "code": [1073741882], "key": ["F1"]}}
        renderer: dict = {"hideHUD": {"name": "RR", "code": [9], "key": ["tab"]}}
        simulation: dict = {"increaseTime": {"name": "SUT", "code": [101], "key": ["e"]}, "decreaseTime": {"name": "SDT", "code": [97], "key": ["a"]}, "pause": {"name": "SP", "code": [32], "key": ["espace"]}, "resetSimulation": {"name": "SRS", "code": [103], "key": ["g"]}, "next": {"name": "SCN", "code": [1073741903], "key": ["\u2192"]}, "previous": {"name": "SCP", "code": [1073741904], "key": ["\u2190"]}}
        for file in ("camera", "editor", "main", "renderer", "simulation"):
            with open(p("data/settings/%s.json" % file), "w", encoding="utf-8") as wf:
                wf.write(dumps(locals()[file]))
                wf.close()
        Game.keybinds = {**camera, **editor, **main, **renderer, **simulation}
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
    button = event.button
    x, y = event.pos
    if button == 1: # clique gauche
        if Game.window != "sandbox": return
        if not Game.Camera.active: return
        for corps in Game.space:
            xC = (corps.pos[0] + Game.Camera.x / Game.Camera.zoom) * Game.Camera.zoom
            yC = (corps.pos[1] + Game.Camera.y / Game.Camera.zoom) * Game.Camera.zoom
            sqx = (x - xC) ** 2
            sqy = (y - yC) ** 2
            if pi * (corps.radius * Game.Camera.zoom) ** 2 < 10:
                if sqrt(sqx + sqy) < 10:
                    Game.Camera.focus = corps
                    Game.Camera.zoom = 51 / corps.radius
                    break
            if sqrt(sqx + sqy) < corps.radius * Game.Camera.zoom:
                Game.Camera.focus = corps
                Game.Camera.zoom = 51 / corps.radius
                break
    if button == 3: # clique droit
        Game.rmb = (x, y)
        Game.ormb = (x, y)
    return

@Events.observe
def mousebuttonup(event) -> None:
    button = event.button
    x, y = event.pos
    if button == 3:
        if Game.ormb == (x, y):
            Events.trigger("contextMenu", event.pos)
        Game.rmb = None
        Game.ormb = None
    return
    
@Events.observe
def mousemotion(event) -> None:
    x, y = event.pos
    if Game.rmb:
        dX, dY = Game.rmb[0] - x, Game.rmb[1] - y
        Game.Camera.x -= dX
        Game.Camera.y -= dY
        Game.rmb = (x, y)
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
