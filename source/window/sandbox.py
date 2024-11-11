import pygame as pg

from main import Game
from shared.utils.utils import updateCorps, process_collide, Captors, Corps, MessageBox, Path, DataKeeper, Input, Text, CheckBox

from eventListen import Events

dk = DataKeeper()
dk.active = False
interface = []
font = pg.font.SysFont("Comic Sans MS", 30)
mb = MessageBox("Return to menu ?")

@Events.observe
def window(w):
    for i in interface:
        interface.remove(i)

@Events.observe
def keydown(event) -> None:
    key = Game.getKeyFromCode(event.key)
    if key:
        Game.keys[key] = True
    if Game.keys["increaseTime"]:
        for i in interface:
            if not hasattr(i, "numberOnly"): continue
            txt = i.text
            i.text = str(int(txt if txt != "" else "0") + 1)
    if Game.keys["decreaseTime"]:
        for i in interface:
            if not hasattr(i, "numberOnly"): continue
            txt = i.text
            i.text = str(int(txt if txt != "" else "0") - 1)
    key = event.key
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
def mousebuttondown(event) -> None:
    button = event.button
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

    textDT = Text("DT : ", (40, 40), color=(255, 255, 255), font=font)
    interface.append(textDT)

    inputDT = Input(str(Game.dt), (100, 40), (200, 40))
    def inputDTdraw(screen):
        color = (0, 0, 255) if inputDT.focus else (255, 255, 255)
        surface = inputDT.font.render(inputDT.text, False, color)
        dim = inputDT.font.size(inputDT.text)
        x = inputDT.position[0] + 5
        y = inputDT.position[1] + inputDT.size[1] // 2 - dim[1] // 2
        screen.blit(surface, (x, y))
    inputDT.draw = inputDTdraw
    inputDT.font = font
    inputDT.numberOnly = True
    interface.append(inputDT)

    textShowPath = Text("Afficher les trajectoires", (40, 108), color=(255, 255, 255))
    interface.append(textShowPath)

    showPath = CheckBox((220, 100), False)
    showPath.trajectoire = None
    interface.append(showPath)

    return

def draw(screen):
    screen.fill((0, 0, 0))

    showPath: bool = False

    for element in interface:
        if not hasattr(element, "trajectoire",): continue
        showPath = element.checked
        

    for corps in Game.space:
        corps.draw(screen, Game.Camera)
        if showPath:
            Path.draw_corps_path(screen, corps.path, corps.color)

    for element in interface:
        element.draw(screen)
        if hasattr(element, "numberOnly"):
            Game.dt = int(element.text) if element.text not in ["-", ""] else 0

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