from ctypes import pythonapi, c_long, py_object
from threading import Thread
from os import path

import pygame as pg
from PIL import Image
from eventListen import Events
from nsi25perlin import PerlinNoise

from main import Game #, medium
from shared.utils.utils import updateCorps, process_collide, Captors, Corps, MessageBox, Path, DataKeeper, Input, Text, CheckBox, SizeViewer, loadSpace, loadStars, draw_velocity_vector, draw_cinetic_energy_vector

dk = DataKeeper()
dk.active = False
dk.loadingFinished = False
dk.loadingImages = []
dk.loadingImageIndex = 0
dk.process = None
dk.image = None
dk.stars = []
dk.perlin = PerlinNoise(768)
interface = []
font = pg.font.SysFont("Comic Sans MS", 30)
mb = MessageBox("Return to menu ?")

def kill(thread: Thread) -> None:
    threadId = thread.ident
    if not threadId: return

    pointer = pythonapi.PyThreadState_SetAsyncExc(c_long(threadId), py_object(SystemExit))
    if pointer > 1:
        pythonapi.PyThreadState_SetAsyncExc(threadId, 0)
    return

@Events.observe
def window(w) -> None:
    interface.clear()
    isAlive = getattr(dk.process, "is_alive", False)
    if isAlive:
        kill(dk.process)
        dk.process = None
    return
    


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
    if Game.keys["resetCamera"]:
        Game.Camera.reset()
        Game.Camera.active = True
    key = event.key
    if not dk.active: return
    if key == pg.K_ESCAPE:
        if mb.active:
            mb.active = False
            dk.active = False
            dk.loadingFinished = False
            dk.image = None
            dk.stars = []
            Game.reset()
            Game.select("menu") # double échap pour quitter
        else:
            mb.active = True
    else:
        mb.active = False
        
    if key == pg.K_KP_PLUS:
        Game.Camera.zoom *= 1.05
    elif key == pg.K_KP_MINUS:
        Game.Camera.zoom /= 1.05
    return

@Events.observe
def mousebuttondown(event) -> None:
    button = event.button
    if not dk.active: return
    if button in [4, 5]:
        return
    mb.active = False
    return

def loader() -> None:
    Game.Camera.active = True
    dk.active = True

    space, size = loadSpace(dk.perlin)
    img = Image.new("RGB", (size, size))
    for pos in space:
        img.putpixel(pos, (space[pos]))
    img = img.resize((5 * size, 5 * size), Image.Resampling.LANCZOS)
    dk.image = pg.image.fromstring(img.tobytes(), img.size, img.mode)
    
    dk.stars = loadStars(1500, (-3000, 3000))

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

    # km = Corps(1, 1, (0, 0), (255, 255, 255), 0, 0)
    # km.name = "1 Kilometer"
    # Game.space.append(km)

    textDT = Text("TimeScale : ", (40, 40), color=(255, 255, 255), font=font)
    interface.append(textDT)

    inputDT = Input(str(Game.timeScale), (200, 40), (200, 40))
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

    showPath = CheckBox((300, 100), False)
    showPath.trajectoire = None
    interface.append(showPath)
    
    textShowAttractionNorm = Text("Afficher la norme d'attraction", (40, 158), color=(255, 255, 255))
    interface.append(textShowAttractionNorm)

    showAttractionNorm = CheckBox((360, 150), False)
    showAttractionNorm.attraction_norm = None
    interface.append(showAttractionNorm)

    sizeViewer = SizeViewer((10, 300))
    interface.append(sizeViewer)

    dk.loadingFinished = True
    dk.loadingImages = []
    dk.loadingImageIndex = 0
    dk.process = None

    return

def load(*args, **kwargs) -> None:
    dk.loadingFinished = False
    process = Thread(target=loader)
    process.start()
    dk.process = process
    for i in range(60):
        img = pg.image.load(path.join("./data/videos/loadingScreen", "%s.jpg" % i))
        img = pg.transform.scale(img, (108, 108))
        dk.loadingImages.append(img)
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))
    if not dk.loadingFinished: # écran de chargement, à améliorer
        # text = medium.render("Loading...", False, (255, 255, 255))
        text = Game.font.render("Loading...", False, (255, 255, 255))
        screen.blit(text, (150, 55))
        image = dk.loadingImages[dk.loadingImageIndex]
        screen.blit(image, (10, 10))
        return

    showPath: bool = False

    image = dk.image
    size = image.get_size()

    screen.blit(image, (Game.Camera.x / 10 - size[0] // 4, Game.Camera.y / 10 - size[1] // 4))

    for star in dk.stars:
        x = int(star[0] + Game.Camera.x / 7)
        y = int(star[1] + Game.Camera.y / 7)
        screen.set_at((x, y), dk.stars[star])

    for element in interface:
        if hasattr(element, "trajectoire"):
            showPath = element.checked
        if hasattr(element, "attractionnorm"):
            showAttractionNorm = element.checked

        
    for corps in Game.space:
        corps.draw(screen, Game.Camera)
        if showPath:
            Path.draw_corps_path(screen, corps.path, corps.color) #ici check machin

        # draw_velocity_vector(screen, corps)
        # draw_cinetic_energy_vector(screen, corps)

    for element in interface:
        element.draw(screen)
        if hasattr(element, "numberOnly"):
            Game.timeScale = int(element.text) if element.text not in ["-", ""] else 0

    mb.draw(screen)
    return

def update() -> None:
    if not dk.loadingFinished:
        dk.loadingImageIndex += 1
        if dk.loadingImageIndex > 59:
            dk.loadingImageIndex = 0

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