from random import randint
from math import pi

import pygame as pg
from eventListen import Events

from main import Game
from shared.utils.utils import updateCorps, process_collide, Button, C_EDUBANG, spacePosToScreenPos, DataKeeper
from shared.components.Corps import Corps
from shared.components.Captors import Captors
from shared.components.Prediction import Prediction

dk = DataKeeper()

dk.brand = None
dk.time = 15

def goSandbox() -> None:
    Game.reset()
    Game.select("sandbox")
    return

def goSettings() -> None:
    Game.reset()
    Game.select("settings")
    return

def goDiscover() -> None:
    Game.reset()
    Game.select("discover")
    return

def goEditor() -> None:
    Game.reset()
    Game.select("editor")
    return


def quitFunction() -> None:
    Game.running = False
    return

interface = []
v = [100, 1]

@Events.observe
def window(w) -> None:
    interface.clear()
    return

def loadRandomSpace() -> None:
    Game.Camera.zoom = 1
    x = 10
    for i in range(x):
        a = Corps(randint(5 * 10 ** 14, 20 * 10 ** 14),
                randint(10, 50),
                (randint(10, 1100), randint(10, 1100)),
                (randint(0, 255), randint(0, 255), randint(0, 255)),
                (randint(-100, 100) / 1000, randint(-100, 100) / 1000)
            )
        Game.space.append(a)
    v[0] = 100
    v[1] = 1
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
    v[0] = 20
    v[1] = 20
    return

def loadTest1() -> None:
    Game.Camera.zoom = 1
    a = Corps(6e15, 10, (100, 500), (255, 0, 0), (0, 0))
    b = Corps(6e17, 100, (600, 500), (0, 0, 255), (0, 0))
    Game.space.append(a)
    Game.space.append(b)
    v[0] = 100
    v[1] = 1
    return

def loadTest2() -> None:
    Game.Camera.zoom = 1
    terre = Corps(6e17, 50, (100, 500), (255, 0, 0), (0, 50))
    mars = Corps(6e17, 50, (600, 500), (0, 0, 255), (0, 0))
    Game.space.append(terre)
    Game.space.append(mars)
    v[0] = 100
    v[1] = 1
    Game.Camera.x = 600
    Game.Camera.y = 0
    return

cases = {
    0: loadRandomSpace,
    1: loadSolarSystem,
    2: loadTest1,
    3: loadTest2
}

def reset() -> None:
    Game.reset()
    cases[randint(0, 3)]()
    return

def load(*args, **kwargs) -> None:
    cases[randint(0, 3)]()

    discover = Button((100, 300), (180, 60))
    discover.text = "Découvrir"
    discover.onPressed = goSandbox
    interface.append(discover)

    editor = Button((100, 400), (180, 60))
    editor.text = "Éditer"
    editor.onPressed = goEditor
    interface.append(editor)

    settingsButton = Button((100, 500), (180, 60))
    settingsButton.text = "Paramètres"
    settingsButton.onPressed = goSettings
    interface.append(settingsButton)

    quitButton = Button((100, 600), (180, 60))
    quitButton.text = "Quitter"
    quitButton.onPressed = quitFunction
    interface.append(quitButton)

    dk.brand = pg.transform.scale(pg.image.load("./data/images/brand.png"), (426, 100))
    return

def draw(screen) -> None:
    screen.fill((0, 0 ,0))

    for corps in Game.space:
        corps.draw(screen, Game.Camera)
        if hasattr(corps, "name") and pi * (corps.radius * Game.Camera.zoom) ** 2 < 10:
            x, y = spacePosToScreenPos(corps.pos)
            pg.draw.line(screen, (255, 255, 255), (x + 4, y - 4), (x + 16, y - 16), 1)
            surface = Game.font.render(corps.name, False, (255, 255, 255))
            screen.blit(surface, (x + 18, y - 30))

    Prediction.predict(Game, v[0], v[1])
    
    if dk.time <= 5:
        k: float = 255 - (255 * dk.time / 5)
        surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
        surface.fill((0, 0, 0, k))
        screen.blit(surface, (0, 0))
    
    if dk.time >= 10:
        k: float = 255 - (255 * (15 - dk.time) / 5)
        surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
        surface.fill((0, 0, 0, k))
        screen.blit(surface, (0, 0))
    
    screen.blit(dk.brand, (100, 100))

    for element in interface:
        element.draw()

    return

def update() -> None:
    dk.time -= (Game.deltaTime * 2.195)
    if dk.time <= 0:
        dk.time = 15
        reset()

    for corps in Game.space:
        corps.update_position([0, 0], Game.DT)
        for otherCorps in Game.space:
            if corps == otherCorps: continue
            distance: float = updateCorps(corps, otherCorps)
            if Captors.collide(corps, otherCorps, distance):
                Game.space.remove(process_collide(corps, otherCorps))
    return