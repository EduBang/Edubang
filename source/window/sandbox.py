import pygame as pg

from main import Game
from shared.utils.utils import updateCorps, process_collide, Captors, Corps, MessageBox, Path, DataKeeper

from eventListen import Events

dk = DataKeeper()

dk.active = False
mb = MessageBox("Return to menu ?")

@Events.observe
def keydown(key: int) -> None:
    if not dk.active: return
    if key == pg.K_ESCAPE:
        if mb.active:
            mb.active = False
            dk.active = False
            Game.reset()
            Game.select("menu") # double échap pour quitter
        else:
            mb.active = True
    else:
        mb.active = False

@Events.observe
def mousebuttondown(position: tuple[int, int], button: int) -> None:
    if not dk.active: return
    if button in [4, 5]:
        return
    mb.active = False

def load(*args, **kwargs):
    Game.Camera.active = True
    dk.active = True

    soleil = Corps(1.9885e14, 700, (0, 0), (255, 255, 0), 0, 0)
    soleil.name = "Soleil"
    mercure = Corps(3.3011e7, 38, (5800, 0), (127, 127, 127), 0, -0.52)
    mercure.name = "Mercure"
    venus = Corps(4.8675e8, 95, (10800, 0), (255, 127, 127), 0, -0.38)
    venus.name = "Vénus"
    terre = Corps(5.9736e8, 100, (15000, 0), (0, 0, 255), 0, -0.32)
    terre.name = "Terre"
    mars = Corps(6.4185e7, 53, (22000, 0), (255, 50, 50), 0, -0.27)
    mars.name = "Mars"
    jupiter = Corps(1.8986e11, 300, (77800, 0), (255, 255, 230), 0, -0.143)
    jupiter.name = "Jupiter"
    saturne = Corps(5.6846e10, 260, (142670, 0), (255, 240, 240), 0, -0.105)
    saturne.name = "Saturne"
    uranus = Corps(8.681e9, 200, (287070, 0), (100, 100, 200), 0, -0.074)
    uranus.name = "Uranus"
    neptune = Corps(1.0243e10, 190, (449840, 0), (100, 100, 255), 0, -0.058)
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

    return

font = pg.font.SysFont("Comic Sans MS", 30)

def draw(screen):
    screen.fill((0, 0 ,0))

    for corps in Game.space:
        corps.draw(screen, Game.Camera)
        Path.draw_corps_path(screen, corps.path, corps.color)

    surface = font.render("DT : %s" % str(Game.dt), False, (255, 255, 255))
    screen.blit(surface, (40, 40))

    mb.draw(screen)
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