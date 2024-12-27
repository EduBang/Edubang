from ctypes import pythonapi, c_long, py_object
from threading import Thread
from os import path
from math import pi

import pygame as pg
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from eventListen import Events
from nsi25perlin import PerlinNoise

from main import Game, getFont
from shared.utils.utils import (
    C_EDUBANG, updateCorps, process_collide,
    MessageBox, Path, DataKeeper,
    Input, Text, CheckBox,
    Button, SizeViewer, loadSpace,
    loadStars, draw_velocity_vector,
    draw_cinetic_energy_vector, draw_attraction_norm2, scientificNotation,
    spacePosToScreenPos, orbitalPeriod, C_EDUBANG,
    getAttractor
)
from shared.components.Corps import Corps
from shared.components.Captors import Captors
from shared.components.Prediction import Prediction
from shared.components.Spaceship import Space_ship
from shared.components.Physics import G
from shared.components.Vectors import Vectors
from shared.components.Relative import totalEnergy, kineticEnergy, momentum

dk = DataKeeper()
dk.timeScale = None
dk.active = False
dk.loadingFinished = False
dk.loadingImages = []
dk.loadingImageIndex = 0
dk.process = None
dk.image = None
dk.stars = []
dk.perlin = PerlinNoise(768)

def stopFocusFn() -> None:
    Game.Camera.focus = None
    Events.trigger("unhovering", dk.stopFocus)
    return

dk.stopFocus = None

interface: list = []

mb = MessageBox("Retourner au menu ? (Échap)")

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

showPath: bool = False
showAttractionNorm: bool = False
showSV: bool = False
showNames: bool = True
showPrediction: bool = False

def kill(thread: Thread) -> None:
    threadId = thread.ident
    if not threadId: return
    pointer = pythonapi.PyThreadState_SetAsyncExc(c_long(threadId), py_object(SystemExit))
    if pointer > 1:
        pythonapi.PyThreadState_SetAsyncExc(threadId, 0)
    return

@Events.observe
def window(w) -> None:
    if w != "sandbox": return
    interface.clear()
    isAlive = getattr(dk.process, "is_alive", False)
    if isAlive:
        kill(dk.process)
        dk.process = None
    return

@Events.observe
def keydown(event) -> None:
    if Game.window != "sandbox": return
    keys = []
    
    mods = pg.key.get_mods()
    if mods & pg.KMOD_LCTRL:
        keys.append(0x400000e0)
    if mods & pg.KMOD_LALT:
        keys.append(0x400000e2)
    keys.append(event.key)

    key = Game.getKeyFromCode(keys)

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
        Game.Camera.x = 1000
        Game.Camera.y = 500
        Game.Camera.active = True
    if Game.keys["pause"]:
        Game.pause = not Game.pause
    if Game.keys["resetSimulation"]:
        for a, d in zip(Game.space, [
                                    (0, 0),
                                    (57_909_050, -47.362),
                                    (108_209_500, -35.02571),
                                    (149_597_887.5, -29.783),
                                    # (149_597_887.5 + 384_399, -29.783 - 0.95),
                                    (227_944_000, -24.080),
                                    (778_340_000, -13.0585),
                                    # (778_340_000.5 + 421_800, -13.0585 - 11.5),
                                    # (778_340_000.5 - 671_100, -13.0585 + 10),
                                    # (778_340_000.5 + 1_070_400, -13.0585 - 8),
                                    # (778_340_000.5 - 1_882_700, -13.0585 + 6),
                                    (1_426_700_000, -9.6407),
                                    # (1_426_700_000.5 + 1_221_870, -9.6407 - 4.2),
                                    (2_870_700_000, -6.796732),
                                    (4_498_400_000, -5.43248),
                                    # (4_498_400_000 + 354_759, -5.43248 - 3.3)
                                    ]
                        ):
            a.pos = (d[0], 0)
            a.velocity = [0, d[1] * C_EDUBANG]
    key = event.key
    if not dk.active: return
    if key == pg.K_ESCAPE:
        if Game.Camera.focus:
            Game.Camera.focus = None
        else:
            if mb.active:
                mb.active = False
                dk.active = False
                dk.loadingFinished = False
                dk.image = None
                dk.stars = []
                Game.reset()
                Game.select("menu")
            else:
                mb.active = True
    else:
        mb.active = False
        
    if key == pg.K_KP_PLUS and Game.Camera.zoom < Game.Camera.maxZoom:
        Game.Camera.zoom *= 1.05
    elif key == pg.K_KP_MINUS and Game.Camera.zoom > Game.Camera.minZoom:
        Game.Camera.zoom /= 1.05

    return

@Events.observe
def keydown(event) -> None:
    keys = []
    
    mods = pg.key.get_mods()
    if mods & pg.KMOD_LCTRL:
        keys.append(0x400000e0)
    if mods & pg.KMOD_LALT:
        keys.append(0x400000e2)
    keys.append(event.key)

    key = Game.getKeyFromCode(keys)
    if key:
        Game.keys[key] = True
    return

@Events.observe
def mousebuttondown(event) -> None:
    button = event.button
    if not dk.active: return
    if button not in [4, 5]:
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

    soleil = Corps(1.9885e30, 696342, (0, 0), (255, 255, 0), (0, 0))
    soleil.name = "Soleil"
    mercure = Corps(3.3011e23, 2439.7, (57_909_050, 0), (127, 127, 127), (0, -47.362 * C_EDUBANG))
    mercure.name = "Mercure"
    venus = Corps(4.8675e24, 6051.8, (108_209_500, 0), (255, 127, 127), (0, -35.02571 * C_EDUBANG))
    venus.name = "Vénus"
    terre = Corps(5.9736e24, 6371.008, (149_597_887.5 , 0), (0, 0, 255), (0, -29.783 * C_EDUBANG))
    terre.name = "Terre"

    lune = Corps(7.3477e22, 1736, (149_597_887.5 + 384_399 , 0), (200, 200, 200), (0, (-29.783 - 1.022) * C_EDUBANG))
    lune.name = "Lune"
    lune.orbit = terre

    mars = Corps(6.4185e23, 3389.5, (227_944_000, 0), (255, 50, 50), (0, -24.080 * C_EDUBANG))
    mars.name = "Mars"

    jupiter = Corps(1.8986e27, 69911, (778_340_000, 0), (252, 201, 129), (0, -13.0585 * C_EDUBANG))
    jupiter.name = "Jupiter"

    io = Corps(8.93e22, 1821.6, (778_340_000.5 + 421_800, 0), (240, 232, 84), (0, (-13.0585 - 11.5) * C_EDUBANG)) # 17.334
    io.name = "IO"
    io.orbit = jupiter

    europe = Corps(4.8e22, 1560.8, (778_340_000.5 - 671_100, 0), (237, 228, 157), (0, (-13.0585 + 10) * C_EDUBANG)) # 13.74
    europe.name = "Europe"
    europe.orbit = jupiter

    ganymede = Corps(1.4819e23, 2631.2, (778_340_000.5 + 1_070_400, 0), (186, 168, 138), (0, (-13.0585 - 8) * C_EDUBANG)) # 10.88
    ganymede.name = "Ganymède"
    ganymede.orbit = jupiter

    callisto = Corps(1.075938e23, 2410.15, (778_340_000.5 - 1_882_700, 0), (64, 63, 57), (0, (-13.0585 + 6) * C_EDUBANG)) # 8.2
    callisto.name = "Callisto"
    callisto.orbit = jupiter

    saturne = Corps(5.6846e26, 58232, (1_426_700_000, 0), (230, 177, 124), (0, -9.6407 * C_EDUBANG))
    saturne.name = "Saturne"

    titan = Corps(1.3452e23, 2575.5, (1_426_700_000.5 + 1_221_870, 0), (204, 157, 82), (0, (-9.6407 - 4.2) * C_EDUBANG)) # 5.57
    titan.name = "Titan"
    titan.orbit = saturne

    uranus = Corps(8.681e25, 25362, (2_870_700_000, 0), (100, 100, 200), (0, -6.796732 * C_EDUBANG))
    uranus.name = "Uranus"
    neptune = Corps(1.0243e26, 24622, (4_498_400_000, 0), (100, 100, 255), (0, -5.43248 * C_EDUBANG))
    neptune.name = "Neptune"

    triton = Corps(2.140e22, 1353.4, (4_498_400_000 + 354_759, 0), (161, 237, 240), (0, (-5.43248 - 3.3) * C_EDUBANG)) # 4.39
    triton.name = "Triton"
    triton.orbit = neptune
    
    # ship = Space_ship.new((1000, 1000), 2000, 0, 0, 0)
    # ship.name = "Spaceship"
    
    # Game.space.append(ship)
    Game.space.append(soleil)
    Game.space.append(mercure)
    Game.space.append(venus)
    Game.space.append(terre)

    # Game.space.append(lune)

    Game.space.append(mars)
    Game.space.append(jupiter)

    # Game.space.append(io)
    # Game.space.append(europe)
    # Game.space.append(ganymede)
    # Game.space.append(callisto)

    Game.space.append(saturne)

    # Game.space.append(titan)

    Game.space.append(uranus)
    Game.space.append(neptune)

    # Game.space.append(triton)

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
    inputDT.resetOnClick = True
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

    textShowPrediction = Text("Afficher les prédictions", (20, 395), color=(255, 255, 255))
    interface.append(textShowPrediction)

    showPrediction = CheckBox((280, 391), False)
    showPrediction.prediction = None
    interface.append(showPrediction)

    textShowSV = Text("Règle de mesure", (20, 555), color=(255, 255, 255))
    interface.append(textShowSV)

    showSV = CheckBox((175, 551), False)
    showSV.checked = True
    showSV.sv = None
    interface.append(showSV)

    w, h = Game.screen.get_size()

    sizeViewer = SizeViewer((w - 200, h - 50))
    sizeViewer.measure = None
    interface.append(sizeViewer)

    stopFocus = Button((w - 340, h - 60), (330, 50))
    stopFocus.text = "Désactiver le suivi"
    stopFocus.onPressed = stopFocusFn
    stopFocus.active = False
    interface.append(stopFocus)
    dk.stopFocus = stopFocus

    dk.loadingFinished = True
    dk.loadingImages = []
    dk.loadingImageIndex = 0

    return

def load(*args, **kwargs) -> None:
    for i in range(60):
        img = pg.image.load(path.join("./data/videos/loadingScreen", "%s.jpg" % i))
        img = pg.transform.scale(img, (108, 108))
        dk.loadingImages.append(img)
    dk.loadingFinished = False
    process = Thread(target=loader)
    process.start()
    dk.process = process
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
    screen.blit(text, (20, 500))
    pg.draw.line(screen, (102, 102, 102), (20, 530), (100, 530))

def stats(corps) -> None:
    screen = Game.screen
    width, height = screen.get_size()

    pg.draw.rect(screen, (10, 9, 9), (width - 350, 0, 350, height))
    pg.draw.rect(screen, (0, 0, 0), (width - 340, 10, 330, 150))
    pg.draw.circle(screen, corps.color, (width - 165, 75), 20)
    if hasattr(corps, "name"):
        text = Game.font.render(corps.name, False, (255, 255, 255))
        screen.blit(text, (width - 330, 170))
    text = subtitle.render("Caractéristiques orbitaux", False, (255, 255, 255))
    screen.blit(text, (width - 330, 210))

    attractor = getattr(corps, "orbit", None) or getAttractor(corps)
    days: float = round(orbitalPeriod(attractor.mass, Vectors.get_distance(corps.pos, attractor.pos)), 2)
    text = Game.font.render("Période de révolution : %s jours" % days, False, (255, 255, 255))
    screen.blit(text, (width - 330, 240))

    velocity: float = round(((corps.velocity[0] / C_EDUBANG) ** 2 + (corps.velocity[1] / C_EDUBANG) ** 2) ** .5, 3)
    text = Game.font.render("Vitesse orbitale : %s km/s" % velocity, False, (255, 255, 255))
    screen.blit(text, (width - 330, 270))

    # moment: float = momentum(corps.mass, velocity)
    # text = Game.font.render("Momentum :", False, (255, 255, 255))
    # screen.blit(text, (width - 330, 300))
    # scientificNotation(moment, (width - 227, 300), end="kg")

    # kinetic: float = kineticEnergy(corps.mass, velocity)
    # text = Game.font.render("Énergie cinétique :", False, (255, 255, 255))
    # screen.blit(text, (width - 330, 330))
    # scientificNotation(kinetic, (width - 187, 330), end="N")

    # total: float = totalEnergy(corps.mass, velocity)
    # text = Game.font.render("Énergie totale :", False, (255, 255, 255))
    # screen.blit(text, (width - 330, 360))
    # scientificNotation(total, (width - 210, 360), end="N")

    text = subtitle.render("Caractéristiques physiques", False, (255, 255, 255))
    screen.blit(text, (width - 330, 500))

    text = Game.font.render("Rayon : %s km" % int(corps.radius), False, (255, 255, 255))
    screen.blit(text, (width - 330, 530))

    text = Game.font.render("Masse :", False, (255, 255, 255))
    screen.blit(text, (width - 330, 560))
    scientificNotation(corps.mass, (width - 267, 560), end="kg")

    surfaceGravity: float = round((G * corps.mass) / ((corps.radius * 1e3) ** 2), 3)
    text = Game.font.render("Gravité de surface : %s m/s²" % surfaceGravity, False, (255, 255, 255))
    screen.blit(text, (width - 330, 590))
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))
    width, height = screen.get_size()
    if not dk.loadingFinished:
        text = Game.font.render("Chargement...", False, (255, 255, 255))
        tW, tH = Game.font.size("Chargement...")
        screen.blit(text, (width // 2 - tW + 70, height // 2 - tH // 2))
        image = dk.loadingImages[dk.loadingImageIndex]
        screen.blit(image, (width // 2 - 108 // 2 - tW, height // 2 - 108 // 2))
        return

    image = dk.image
    size = image.get_size()

    screen.blit(image, (Game.Camera.x / 10 - size[0] // 4, Game.Camera.y / 10 - size[1] // 4))

    if Game.Camera.zoom < 0.3:
        for star in dk.stars:
            x = int(star[0] + Game.Camera.x / 7)
            y = int(star[1] + Game.Camera.y / 7)
            screen.set_at((x, y), (255, 255, 255))

    for element in interface:
        if hasattr(element, "trajectoire"):
            showPath = element.checked
        if hasattr(element, "attraction_norm"):
            showAttractionNorm = element.checked
        if hasattr(element, "sv"):
            showSV = element.checked
        if hasattr(element, "sn"):
            showNames = element.checked
        if hasattr(element, "prediction"):
            showPrediction = element.checked

    if Game.Camera.focus:
        dk.stopFocus.active = True
        dk.stopFocus.position = [width - 340, height - 60]
        midScreenX = width // 2
        midScreenY = height // 2
        Game.Camera.x = midScreenX - Game.Camera.focus.pos[0] * Game.Camera.zoom
        Game.Camera.y = midScreenY - Game.Camera.focus.pos[1] * Game.Camera.zoom
    else:
        if hasattr(dk.stopFocus, "active"):
            dk.stopFocus.active = False

    for corps in Game.space:
        corps.draw(screen, Game.Camera)
        if showNames:
            if hasattr(corps, "name") and pi * (corps.radius * Game.Camera.zoom) ** 2 < 10:
                x, y = spacePosToScreenPos(corps.pos)
                pg.draw.line(screen, (255, 255, 255), (x + 4, y - 4), (x + 16, y - 16), 1)
                surface = Game.font.render(corps.name, False, (255, 255, 255))
                screen.blit(surface, (x + 18, y - 30))
        if showPath:
            Path.draw_corps_path(screen, corps.path, corps.color)
        

        # draw_velocity_vector(screen, corps)
        # draw_cinetic_energy_vector(screen, corps)

    if showAttractionNorm:
        draw_attraction_norm2(screen)

    if showPrediction:
        Prediction.predict(Game, 20)

    menu(screen)

    if Game.Camera.focus:
        stats(Game.Camera.focus)

    for element in interface:
        if hasattr(element, "measure") and not showSV: continue
        if Game.Camera.focus and hasattr(element, "measure") and element.position[0] > width - 500:
            element.position[0] = width - 500
        element.draw()
        if hasattr(element, "numberOnly"):
            Game.timeScale = int(element.text) if element.text not in ["-", ""] else 0
            element.active = not Game.pause
            if element.focus and Game.pause:
                element.focus = False

    if Game.pause:
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
        corps.update_position([0, 0], Game.DT)
        for otherCorps in Game.space:
            if corps == otherCorps: continue
            distance: float = updateCorps(corps, otherCorps)
            if Captors.collide(corps, otherCorps, distance):
                Game.space.remove(process_collide(corps, otherCorps))
    return