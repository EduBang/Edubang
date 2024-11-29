from ctypes import pythonapi, c_long, py_object
from threading import Thread
from os import path
from math import pi

import pygame as pg
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from eventListen import Events
from nsi25perlin import PerlinNoise

from main import Game, getFont
from shared.utils.utils import updateCorps, process_collide, Captors, Corps, MessageBox, Path, DataKeeper, Input, Text, CheckBox, SizeViewer, loadSpace, loadStars, draw_velocity_vector, draw_cinetic_energy_vector
from shared.components.Prediction import Prediction

prediction = Prediction(Game.space)
dk = DataKeeper()
dk.pause = False
dk.timeScale = None
dk.active = False
dk.loadingFinished = False
dk.loadingImages = []
dk.loadingImageIndex = 0
dk.process = None
dk.image = None
dk.stars = []
dk.perlin = PerlinNoise(768)
interface = []
mb = MessageBox("Retourner au menu ?")
subtitle = getFont("Bold")
brand = Image.open("data/images/brand.png")
brand = brand.resize((175, 41), Image.Resampling.BICUBIC)
brand = pg.image.fromstring(brand.tobytes(), brand.size, brand.mode)
icon = Image.open("data/images/icon.png")
icon = icon.resize((398, 402), Image.Resampling.BICUBIC)
icon = ImageOps.expand(icon, border=20, fill=(0, 0, 0, 0))
icon = icon.filter(ImageFilter.GaussianBlur(10))
enhancer = ImageEnhance.Brightness(icon)
icon = enhancer.enhance(.075)
icon = pg.image.fromstring(icon.tobytes(), icon.size, icon.mode)

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
    if Game.window != "sandbox": return
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
    if Game.keys["pause"]:
        dk.pause = not dk.pause
        if dk.pause:
            dk.timeScale = Game.timeScale
            for element in interface:
                if hasattr(element, "numberOnly"):
                    element.text = "0"
        else:
            for element in interface:
                if hasattr(element, "numberOnly"):
                    element.text = str(dk.timeScale)
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
    Game.Camera.x = 1000
    Game.Camera.y = 500
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

    # km = Corps(10, 1, (0, 0), (255, 255, 255), 0, 0)
    # km.name = "1 Kilometer"
    # Game.space.append(km)
    # km10 = Corps(100, 10, (100, 100), (255, 255, 255), 0, 0)
    # km10.name = "10 Kilometer"
    # Game.space.append(km10)

    textDT = Text("Échelle du temps : ", (20, 145), color=(255, 255, 255))
    interface.append(textDT)

    inputDT = Input(str(Game.timeScale), (180, 145), (100, 40))
    def inputDTdraw():
        color = (0, 0, 255) if inputDT.focus else (255, 255, 255)
        surface = Game.font.render(inputDT.text, False, color)
        dim = Game.font.size(inputDT.text)
        x = inputDT.position[0]
        y = inputDT.position[1] + inputDT.size[1] // 2 - dim[1] // 2 - 10
        Game.screen.blit(surface, (x, y))
        text = Game.font.render("jour/s", False, color)
        Game.screen.blit(text, (x + dim[0] + 4, y))
    inputDT.draw = inputDTdraw
    inputDT.numberOnly = True
    interface.append(inputDT)

    textShowName = Text("Afficher le nom des astres", (20, 245), color=(255, 255, 255))
    interface.append(textShowName)

    showNames = CheckBox((245, 241), True)
    showNames.sn = None
    interface.append(showNames)

    textShowPath = Text("Afficher les trajectoires", (20, 295), color=(255, 255, 255))
    interface.append(textShowPath)

    showPath = CheckBox((225, 291), False)
    showPath.trajectoire = None
    interface.append(showPath)
    
    textShowAttractionNorm = Text("Afficher la norme d'attraction", (20, 345), color=(255, 255, 255))
    interface.append(textShowAttractionNorm)

    showAttractionNorm = CheckBox((280, 341), False)
    showAttractionNorm.attraction_norm = None
    interface.append(showAttractionNorm)

    textShowSV = Text("Règle de mesure", (20, 455), color=(255, 255, 255))
    interface.append(textShowSV)

    showSV = CheckBox((175, 451), False)
    showSV.checked = True
    showSV.sv = None
    interface.append(showSV)

    w, h = Game.screen.get_size()

    sizeViewer = SizeViewer((w - 200, h - 50))
    sizeViewer.measure = None
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

def menu(screen) -> None:
    width, height = screen.get_size()
    pg.draw.rect(screen, (10, 9, 9), (0, 0, 350, height))

    screen.blit(brand, (20, 20))
    screen.blit(icon, (-150, height - 320))

    text = subtitle.render("Paramètres de simulation", False, (255, 255, 255))
    screen.blit(text, (20, 100))
    pg.draw.line(screen, (102, 102, 102), (20, 130), (100, 130))

    text = subtitle.render("Paramètres d'affichage", False, (255, 255, 255))
    screen.blit(text, (20, 200))
    pg.draw.line(screen, (102, 102, 102), (20, 230), (100, 230))

    text = subtitle.render("Outils", False, (255, 255, 255))
    screen.blit(text, (20, 400))
    pg.draw.line(screen, (102, 102, 102), (20, 430), (100, 430))

def draw(screen) -> None:
    screen.fill((0, 0, 0))
    if not dk.loadingFinished:
        width, height = screen.get_size()
        text = Game.font.render("Chargement...", False, (255, 255, 255))
        tW, tH = Game.font.size("Chargement...")
        screen.blit(text, (width // 2 - tW + 70, height // 2 - tH // 2))
        image = dk.loadingImages[dk.loadingImageIndex]
        screen.blit(image, (width // 2 - 108 // 2 - tW, height // 2 - 108 // 2))
        return

    showPath: bool = False
    showAttractionNorm: bool = False
    showSV: bool = False
    showNames: bool = True

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
        if hasattr(element, "sv"):
            showSV = element.checked
        if hasattr(element, "sn"):
            showNames = element.checked

        
    for corps in Game.space:
        corps.draw(screen, Game.Camera)
        if showNames:
            if hasattr(corps, "name") and pi * (corps.radius * Game.Camera.zoom) ** 2 < 10:
                camera = Game.Camera
                x = float((corps.pos[0] + camera.x / camera.zoom) * camera.zoom)
                y = float((corps.pos[1] + camera.y / camera.zoom) * camera.zoom)
                pg.draw.line(screen, (255, 255, 255), (x + 4, y - 4), (x + 16, y - 16), 1)
                surface = Game.font.render(corps.name, False, (255, 255, 255))
                screen.blit(surface, (x + 18, y - 30))
        if showPath:
            Path.draw_corps_path(screen, corps.path, corps.color) #ici check machin

        # draw_velocity_vector(screen, corps)
        # draw_cinetic_energy_vector(screen, corps)
    
    # prediction.predict(1)

    menu(screen)

    for element in interface:
        if hasattr(element, "measure") and not showSV: continue
        element.draw()
        if hasattr(element, "numberOnly"):
            Game.timeScale = int(element.text) if element.text not in ["-", ""] else 0

    if dk.pause:
        width, height = screen.get_size()
        text = Game.font.render("Simulation en pause", False, (255, 255, 255))
        tW, tH = Game.font.size("Simulation en pause")
        screen.blit(text, (width // 2 - tW // 2, height // 2 - tH // 2 - 200))

    mb.draw()
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