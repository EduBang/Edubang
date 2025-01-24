from random import randint
from math import pi

import pygame as pg
from PIL import Image
from eventListen import Events
from nsi25perlin import PerlinNoise

from main import Game, getFont
from shared.utils.utils import updateCorps, process_collide, Button, C_EDUBANG, spacePosToScreenPos, DataKeeper, loadSpace, l
from shared.components.Corps import Corps
from shared.components.Captors import isColliding
from shared.components.Prediction import predict

dk = DataKeeper()

space, size = loadSpace(PerlinNoise())
img = Image.new("RGB", (size, size))
for pos in space:
    img.putpixel(pos, (space[pos]))
img = img.resize((8 * size, 6 * size), Image.Resampling.LANCZOS)

dk.image = pg.image.fromstring(img.tobytes(), img.size, img.mode)
dk.brand = None
dk.time = 15

semibold = getFont("SemiBold", 20)

def goDiscover() -> None:
    Game.reset()
    Game.select("discover")
    return

def goEditor() -> None:
    Game.reset()
    Game.select("editor")
    return

def goSettings() -> None:
    Game.reset()
    Game.select("settings")
    return

def quitFunction() -> None:
    Game.running = False
    return

interface: list = []
v: list[int, int] = [100, 1]

@Events.observe
def window(w) -> None:
    if w != "menu": return
    interface.clear()
    return

def loadRandomSpace() -> None:
    Game.Camera.zoom = 1
    x: int = 10
    for i in range(x):
        a = Corps(randint(5 * 10 ** 14, 20 * 10 ** 14),
                randint(10, 50),
                (randint(10, 1100), randint(10, 1100)),
                (randint(0, 255), randint(0, 255), randint(0, 255)),
                (randint(-100, 100) / 1000, randint(-100, 100) / 1000)
            )
        Game.space.append(a)
    return

def loadSolarSystem() -> None:
    soleil = Corps(1.9885e30, 696342, (0, 0), (255, 255, 0), (0, 0))
    soleil.name = "Sun"
    mercure = Corps(3.3011e23, 2439.7, (57_909_050, 0), (127, 127, 127), (0, -47.362 * C_EDUBANG))
    mercure.name = "Mercury"
    venus = Corps(4.8675e24, 6051.8, (108_209_500, 0), (255, 127, 127), (0, -35.02571 * C_EDUBANG))
    venus.name = "Venus"
    terre = Corps(5.9736e24, 6371.008, (149_597_887.5 , 0), (0, 0, 255), (0, -29.783 * C_EDUBANG))
    terre.name = "Earth"
    mars = Corps(6.4185e23, 3389.5, (227_944_000, 0), (255, 50, 50), (0, -24.080 * C_EDUBANG))
    mars.name = "Mars"
    jupiter = Corps(1.8986e27, 69911, (778_340_000, 0), (255, 255, 230), (0, -13.0585 * C_EDUBANG))
    jupiter.name = "Jupiter"
    saturne = Corps(5.6846e26, 58232, (1_426_700_000, 0), (255, 240, 240), (0, -9.6407 * C_EDUBANG))
    saturne.name = "Saturn"
    uranus = Corps(8.681e25, 25362, (2_870_700_000, 0), (100, 100, 200), (0, -6.796732 * C_EDUBANG))
    uranus.name = "Uranus"
    neptune = Corps(1.0243e26, 24622, (4_498_400_000, 0), (100, 100, 255), (0, -5.43248 * C_EDUBANG))
    neptune.name = "Neptune"

    Game.space.append(soleil)
    Game.space.append(mercure)
    Game.space.append(venus)
    Game.space.append(terre)
    Game.space.append(mars)
    Game.space.append(jupiter)
    Game.space.append(saturne)
    Game.space.append(uranus)
    Game.space.append(neptune)

    Game.timeScale = 30
    Game.Camera.zoom = 0.00_000_4
    Game.Camera.x = 600
    Game.Camera.y = 500
    v[0] = 10
    v[1] = 40
    return

def loadTest1() -> None:
    Game.Camera.zoom = 1
    a = Corps(6e15, 10, (100, 500), (255, 0, 0), (0, 0))
    b = Corps(6e17, 100, (900, 500), (0, 0, 255), (0, 0))
    Game.space.append(a)
    Game.space.append(b)
    return

def loadTest2() -> None:
    Game.Camera.zoom = 1
    terre = Corps(6e17, 50, (100, 500), (255, 0, 0), (0, 50))
    mars = Corps(6e17, 50, (900, 500), (0, 0, 255), (0, 0))
    Game.space.append(terre)
    Game.space.append(mars)
    Game.Camera.x = 600
    Game.Camera.y = 0
    return

def loadTest3() -> None:
    Game.Camera.zoom = 1
    a = Corps(6e17, 50, (100, 100), (255, 0, 0), (-100, 100))
    b = Corps(6e17, 50, (100, 900), (0, 0, 255), (-100, -100))
    Game.space.append(a)
    Game.space.append(b)
    Game.Camera.x = 1000
    Game.Camera.y = 0
    return

cases = {
    0: loadRandomSpace,
    1: loadSolarSystem,
    2: loadTest1,
    3: loadTest2,
    4: loadTest3
}

def reset() -> None:
    Game.reset()
    v[0] = 100
    v[1] = 1
    cases[randint(0, 4)]()
    return

def load() -> None:
    cases[randint(0, 4)]()

    icons: list = [pg.transform.scale(pg.image.load("./data/images/%s.png" % i), (38, 50)) for i in ("play", "pencil", "settings", "power")]

    discoverButton = Button((100, 300), (170, 60), color=(13, 178, 190))
    discoverButton.text = l("discover")
    discoverButton.font = semibold
    discoverButton.textColor = (255, 255, 255)
    discoverButton.icon = icons[0]
    discoverButton.onPressed = goDiscover
    interface.append(discoverButton)

    editorButton = Button((100, 400), (265, 60), color=(13, 178, 190))
    editorButton.text = l("editor")
    editorButton.font = semibold
    editorButton.textColor = (255, 255, 255)
    editorButton.icon = icons[1]
    editorButton.onPressed = goEditor
    interface.append(editorButton)

    settingsButton = Button((100, 500), (190, 60), color=(13, 178, 190))
    settingsButton.text = l("settings")
    settingsButton.font = semibold
    settingsButton.textColor = (255, 255, 255)
    settingsButton.icon = icons[2]
    settingsButton.onPressed = goSettings
    interface.append(settingsButton)

    quitButton = Button((100, 600), (240, 60), color=(13, 178, 190))
    quitButton.text = l("quit")
    quitButton.font = semibold
    quitButton.textColor = (255, 255, 255)
    quitButton.icon = icons[3]
    quitButton.onPressed = quitFunction
    interface.append(quitButton)

    dk.brand = pg.transform.scale(pg.image.load("./data/images/brand.png"), (426, 100))
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))

    w, h = Game.screenSize

    screen.blit(dk.image, (0, 0))

    for corps in Game.space:
        corps.draw(screen, Game.Camera)
        if hasattr(corps, "name") and pi * (corps.radius * Game.Camera.zoom) ** 2 < 10:
            x, y = spacePosToScreenPos(corps.pos)
            pg.draw.line(screen, (255, 255, 255), (x + 4, y - 4), (x + 16, y - 16), 1)
            surface = Game.font.render(corps.name, False, (255, 255, 255))
            screen.blit(surface, (x + 18, y - 30))

    predict(Game, v[0], v[1])
    
    if dk.time <= 5:
        k: float = 255 - (255 * dk.time / 5)
        surface = pg.Surface((w, h), pg.SRCALPHA)
        surface.fill((0, 0, 0, k))
        screen.blit(surface, (0, 0))
    
    if dk.time >= 10:
        k: float = 255 - (255 * (15 - dk.time) / 5)
        surface = pg.Surface((w, h), pg.SRCALPHA)
        surface.fill((0, 0, 0, k))
        screen.blit(surface, (0, 0))
    
    screen.blit(dk.brand, (100, 100))

    for element in interface:
        element.draw()

    surface = semibold.render(l("notShare"), False, (128, 128, 128))
    screen.blit(surface, (w - 450, h - 100))

    return

def update() -> None:
    dk.time -= (Game.deltaTime * 2.195)
    if dk.time <= 0:
        dk.time = 15
        reset()

    for corps in Game.space:
        # corps.update_position([0, 0], Game.DT)
        for otherCorps in Game.space:
            if corps == otherCorps: continue
            distance: float = updateCorps(corps, otherCorps)
            if isColliding(corps, otherCorps, distance):
                Game.space.remove(process_collide(corps, otherCorps))
    return