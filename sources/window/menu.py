from random import randint

from eventListen import Events

from main import Game
from shared.utils.utils import updateCorps, process_collide, Captors, Button, Corps



def goSandbox() -> None:
    Game.reset()
    Game.select("sandbox")
    return

def goSettings() -> None:
    Game.reset()
    Game.select("settings")
    return

def quitFunction() -> None:
    Game.running = False
    return

interface = []

@Events.observe
def window(w) -> None:
    interface.clear()
    return

def load(*args, **kwargs) -> None:
    if randint(0, 1) == 0:
        Game.Camera.zoom = 1
        x = 10
        for i in range(x):
            a = Corps(randint(5 * 10 ** 14, 20 * 10 ** 14),
                    randint(10, 50),
                    (randint(10, 1100), randint(10, 1100)),
                    (randint(0, 255), randint(0, 255), randint(0, 255)),
                    randint(-100, 100) / 10000, randint(-100, 100) / 10000
                    )
            Game.space.append(a)
    elif randint(0, 1) == 0:
        # La constante d'EduBang
        # valeur de calibrage, origine à déterminer
        C_EDUBANG = 10750

        soleil = Corps(1.9885e30, 696342, (0, 0), (255, 255, 0), 0, 0)
        soleil.name = "Soleil"
        mercure = Corps(3.3011e23, 2439.7, (57_909_050, 0), (127, 127, 127), 0, -47.362 * C_EDUBANG)
        mercure.name = "Mercure"
        venus = Corps(4.8675e24, 6051.8, (108_209_500, 0), (255, 127, 127), 0, -35.02571 * C_EDUBANG)
        venus.name = "Vénus"
        terre = Corps(5.9736e24, 6371.008, (149_597_887.5 , 0), (0, 0, 255), 0, -29.783 * C_EDUBANG)
        terre.name = "Terre"
        mars = Corps(6.4185e23, 3389.5, (227_944_000, 0), (255, 50, 50), 0, -24.080 * C_EDUBANG)
        mars.name = "Mars"
        jupiter = Corps(1.8986e27, 69911, (778_340_000, 0), (255, 255, 230), 0, -13.0585 * C_EDUBANG)
        jupiter.name = "Jupiter"
        saturne = Corps(5.6846e26, 58232, (1_426_700_000, 0), (255, 240, 240), 0, -9.6407 * C_EDUBANG)
        saturne.name = "Saturne"
        uranus = Corps(8.681e25, 25362, (2_870_700_000, 0), (100, 100, 200), 0, -6.796732 * C_EDUBANG)
        uranus.name = "Uranus"
        neptune = Corps(1.0243e26, 24622, (4_498_400_000, 0), (100, 100, 255), 0, -5.43248 * C_EDUBANG)
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

        Game.timeScale = 20
        Game.Camera.zoom = 0.00_000_4
        Game.Camera.x = 100
        Game.Camera.y = 500
    elif randint(0, 1) == 0:
        Game.Camera.zoom = 1
        a = Corps(6e17, 10, (100, 500), (255, 0, 0), 0, 0)
        b = Corps(6e17, 100, (600, 500), (0, 0, 255), 0, 0)
        Game.space.append(a)
        Game.space.append(b)
    else:
        Game.Camera.zoom = 1
        terre = Corps(6e17, 50, (100, 500), (255, 0, 0), 0, 0.1)
        mars = Corps(6e17, 50, (600, 500), (0, 0, 255), 0, 0)
        Game.space.append(terre)
        Game.space.append(mars)

    sandbox = Button((100, 100), (180, 60))
    sandbox.text = "Accéder au Sandbox"
    sandbox.onPressed = goSandbox
    interface.append(sandbox)

    settingsButton = Button((100, 200), (180, 60))
    settingsButton.text = "Paramètres"
    settingsButton.onPressed = goSettings
    interface.append(settingsButton)

    quitButton = Button((100, 300), (180, 60))
    quitButton.text = "Quitter"
    quitButton.onPressed = quitFunction
    interface.append(quitButton)
    return

def draw(screen) -> None:
    screen.fill((0, 0 ,0))

    for corps in Game.space:
        corps.draw(screen, Game.Camera)
    
    for element in interface:
        element.draw()
    
    return

def update() -> None:
    for corps in Game.space:
        for otherCorps in Game.space:
            if corps == otherCorps:
                continue
            distance = updateCorps(corps, otherCorps)
            if Captors.collide(corps, otherCorps, distance):
                removedCorps = process_collide(corps, otherCorps)
                Game.space.remove(removedCorps)
        
        corps.update_position([0, 0], Game.deltaTime * Game.timeScale)
    return