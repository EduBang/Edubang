from os import listdir, path
from importlib import util
from math import pi, sqrt

import pygame as pg

from proto import proto
from eventListen import Events

pg.init()

# Initialisation
pg.display.set_caption("EduBang")
icon = pg.image.load("source/Images/icon.png")
pg.display.set_icon(icon)
buttons = []
resolution = (1200, 1000)
screen = pg.display.set_mode(resolution)

with proto("Game") as Game:
    @Game
    def draw_screen(self):
        pg.display.update()

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

        ws = [w for w in listdir("./source/window") if path.isfile(path.join("./source/window", w))]
        for w in ws:
            module_name = w[:-3]
            file_path = path.join("./source/window", w)
            spec = util.spec_from_file_location(module_name, file_path)
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            loadFunction = getattr(module, "load")
            drawFunction = getattr(module, "draw")
            self.windows[module_name] = [loadFunction, drawFunction]

        self.select("menu")


    @Game
    def select(self, w):
        if not w in self.windows.keys(): return
        Events.trigger("window", w)
        self.windows[w][0]() # fonction load
        self.window = w
        return
    
    @Game
    def reset(self):
        self.Camera.reset()
        self.dt = 0
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

keys = {
    pg.K_z: False,
    pg.K_q: False,
    pg.K_s: False,
    pg.K_d: False,
    pg.K_UP: False,
    pg.K_LEFT: False,
    pg.K_DOWN: False,
    pg.K_RIGHT: False
}

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
def keydown(key: int) -> None:
    if key in keys:
        keys[key] = True
    if key == pg.K_a:
        Game.dt -= 5
    if key == pg.K_e:
        Game.dt += 5
    return

@Events.observe
def keyup(key: int) -> None:
    if key in keys:
        keys[key] = False
    return

@Events.observe
def mousewheel(x: int, y: int) -> None:
    if not Game.Camera.active: return
    if y == 1 and Game.Camera.zoom < Game.Camera.maxZoom: # scroll vers le haut: zoom
        Game.Camera.zoom *= 1.05
    if y == -1 and Game.Camera.zoom > Game.Camera.minZoom: # scroll vers le bas: dézoom
        Game.Camera.zoom /= 1.05
    return

@Events.observe
def mousebuttondown(position: tuple[int, int], button: int) -> None:
    if button in [4, 5]: # les scrolls bas et haut sont considirés comme des cliques de souris
        return
    if button == 1: # clique gauche
        if not Game.Camera.active: return
        for corps in Game.space:
            x = float((corps.pos[0] + Game.Camera.x / Game.Camera.zoom) * Game.Camera.zoom)
            y = float((corps.pos[1] + Game.Camera.y / Game.Camera.zoom) * Game.Camera.zoom)
            sqx = (position[0] - x) ** 2
            sqy = (position[1] - y) ** 2
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

# Boucle principale
clock = pg.time.Clock()
while Game.running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            Game.running = False

        if event.type == pg.KEYDOWN:
            Events.trigger("keydown", event.key)
        if event.type == pg.KEYUP:
            Events.trigger("keyup", event.key)
        if event.type == pg.MOUSEWHEEL:
            Events.trigger("mousewheel", event.x, event.y)
        if event.type == pg.MOUSEBUTTONDOWN:
            Events.trigger("mousebuttondown", event.pos, event.button)
        if event.type == pg.MOUSEBUTTONUP:
            Events.trigger("mousebuttonup", event.pos, event.button)
        if event.type == pg.MOUSEMOTION:
            Events.trigger("mousemotion", event.pos)
    
    if Game.Camera.active:
        if keys[pg.K_z] or keys[pg.K_UP]: # faire monter la caméra
            Game.Camera.y += Game.Camera.speed
        if keys[pg.K_q] or keys[pg.K_LEFT]: # faire aller la caméra à gauche
            Game.Camera.x += Game.Camera.speed
        if keys[pg.K_s] or keys[pg.K_DOWN]: # faire descendre la caméra
            Game.Camera.y -= Game.Camera.speed
        if keys[pg.K_d] or keys[pg.K_RIGHT]: # faire aller la caméra à droite
            Game.Camera.x -= Game.Camera.speed

        if Game.Camera.focus is not None:
            midScreenX = screen.get_width() // 2
            midScreenY = screen.get_height() // 2
            Game.Camera.x = midScreenX - Game.Camera.focus.pos[0]
            Game.Camera.y = midScreenY - Game.Camera.focus.pos[1]

    Game.windows[Game.window][1](screen) # fonction draw

    if len(buttons) == 0: # Si la souris ne hover plus rien
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    # Mettre à jour l'écran
    Game.draw_screen()
    # clock.tick(60)  # Limite à 60 FPS

Game.quit_algo()