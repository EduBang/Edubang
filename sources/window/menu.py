from random import randint

from eventListen import Events

from main import Game
from shared.utils.utils import updateCorps, process_collide, Captors, Button, Corps



def playSandbox():
    Game.reset()
    Game.select("sandbox")

def goKeybind():
    Game.reset()
    Game.select("keybind")

def quitFunction():
    Game.running = False

interface = []

@Events.observe
def window(w):
    interface.clear()

def load(*args, **kwargs):
    if randint(0, 1) == 0:
        x = 10
        for i in range(x):
            a = Corps(randint(5 * 10 ** 9, 20 * 10 ** 9),
                    randint(10, 50),
                    (randint(10, 1100), randint(10, 1100)),
                    (randint(0, 255), randint(0, 255), randint(0, 255)),
                    randint(-100, 100) / 10000, randint(-100, 100) / 10000
                    )
            Game.space.append(a)
    elif randint(0, 1) == 0:
        soleil = Corps(1.9885e14, 700, (0, 0), (255, 255, 0), 0, 0)
        mercure = Corps(3.3011e7, 38, (5800, 0), (127, 127, 127), 0, -0.52)
        venus = Corps(4.8675e8, 95, (10800, 0), (255, 127, 127), 0, -0.38)
        terre = Corps(5.9736e8, 100, (15000, 0), (0, 0, 255), 0, -0.32)
        mars = Corps(6.4185e7, 53, (22000, 0), (255, 50, 50), 0, -0.27)
        jupiter = Corps(1.8986e11, 300, (77800, 0), (255, 255, 230), 0, -0.143)
        saturne = Corps(5.6846e10, 260, (142670, 0), (255, 240, 240), 0, -0.105)
        uranus = Corps(8.681e9, 200, (287070, 0), (100, 100, 200), 0, -0.074)
        neptune = Corps(1.0243e10, 190, (449840, 0), (100, 100, 255), 0, -0.058)
        Game.space.append(soleil)
        Game.space.append(mercure)
        Game.space.append(venus)
        Game.space.append(terre)
        Game.space.append(mars)
        Game.space.append(jupiter)
        Game.space.append(saturne)
        Game.space.append(uranus)
        Game.space.append(neptune)

        Game.Camera.zoom = 0.047
        Game.Camera.x = 100
        Game.Camera.y = 500
        Game.dt = 25
    elif randint(0, 1) == 0:
        a = Corps(6e10, 10, (100, 500), (255, 0, 0), 0, 0)
        b = Corps(6e12, 100, (600, 500), (0, 0, 255), 0, 0)
        Game.space.append(a)
        Game.space.append(b)
    else:
        terre = Corps(6e12, 50, (100, 500), (255, 0, 0), 0, 0.1)
        mars = Corps(6e12, 50, (600, 500), (0, 0, 255), 0, 0)
        Game.space.append(terre)
        Game.space.append(mars)

    sandbox = Button((100, 100), (180, 60))
    sandbox.text = "Play Sandbox"
    sandbox.onPressed = playSandbox
    interface.append(sandbox)

    keybindButton = Button((100, 200), (180, 60))
    keybindButton.text = "Keybind"
    keybindButton.onPressed = goKeybind
    interface.append(keybindButton)

    quitButton = Button((100, 300), (180, 60))
    quitButton.text = "Quit"
    quitButton.onPressed = quitFunction
    interface.append(quitButton)
    return

def draw(screen):
    screen.fill((0, 0 ,0))

    for corps in Game.space:
        corps.draw(screen, Game.Camera)
    
    for element in interface:
        element.draw(screen)
    
    return

def update():
    for corps in Game.space:
        for otherCorps in Game.space:
            if corps == otherCorps:
                continue
            distance = updateCorps(corps, otherCorps)
            if Captors.collide(corps, otherCorps, distance):
                removedCorps = process_collide(corps, otherCorps)
                Game.space.remove(removedCorps)
        
        corps.update_position([0, 0], Game.dt)
    return