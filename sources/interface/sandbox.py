from threading import Thread
from os import path
from math import pi, sqrt

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
    draw_cinetic_energy_vector, draw_attraction_norm, scientificNotation,
    spacePosToScreenPos, orbitalPeriod, C_EDUBANG,
    totalEnergy, kineticEnergy, momentum,
    getAttractor, barycentre, toDate,
    displayMultilineText
)
from shared.components.Captors import isColliding
from shared.components.Prediction import predict
from shared.components.Spaceship import Space_ship
from shared.components.Physics import G
from shared.components.Vectors import Vectors

dk = DataKeeper()
dk.timeScale = None
dk.active = False
dk.loadingFinished = False
dk.loadingImages = []
dk.loadingImageIndex = 0
dk.image = None
dk.stars = []
dk.perlin = PerlinNoise(768)
dk.wait = True
dk.timer = 0
dk.specialKeys = []

def stopFocusFn() -> None:
    Game.Camera.focus = None
    Events.trigger("unhovering", dk.stopFocus)
    return

dk.stopFocus = None

description = getFont("Regular", 14)

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
showBarycentre: bool = False

@Events.observe
def interface(w) -> None:
    if w != "sandbox": return
    interface.clear()
    return

@Events.observe
def keydown(event) -> None:
    if Game.window != "sandbox": return
    if dk.wait: return

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
        Game.resetSpace()
        dk.timer = 0
        f = Game.Camera.focus
        if f:
            for e in Game.space:
                if e.mass == f.mass and e.radius == f.radius and e.color == f.color:
                    Game.Camera.focus = e
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
def keyup(event) -> None:
    if Game.window != "sandbox": return
    keys = []
    
    mods = pg.key.get_mods()
    if mods & pg.KMOD_LCTRL:
        dk.specialKeys.append(0x400000e0)
    if mods & pg.KMOD_LALT:
        dk.specialKeys.append(0x400000e2)
    if event.key not in dk.specialKeys:
        keys.append(event.key)
    
    if len(keys) > 0:
        key = Game.getKeyFromCode(keys)
        if key:
            Game.keys[key] = False
        if len(dk.specialKeys) > 0:
            keys = dk.specialKeys + keys
            dk.specialKeys.clear()
        key = Game.getKeyFromCode(keys)
        if key:
            Game.keys[key] = False
    return

@Events.observe
def mousebuttondown(event) -> None:
    button = event.button
    if not dk.active: return
    if button not in [4, 5]:
        mb.active = False
    return

def loader() -> None:
    dk.wait = True
    Game.Camera.active = True
    w, h = Game.screenSize
    Game.Camera.x = w // 2
    Game.Camera.y = h // 2
    dk.active = True

    space, size = loadSpace(dk.perlin)
    img = Image.new("RGB", (size, size))
    for pos in space:
        img.putpixel(pos, (space[pos]))
    img = img.resize((5 * size, 5 * size), Image.Resampling.LANCZOS)
    dk.image = pg.image.fromstring(img.tobytes(), img.size, img.mode)
    
    dk.stars = loadStars(1500, (-3000, 3000))
    
    # ship = Space_ship.new((1000, 1000), 2000, 0, 0, 0)
    # ship.name = "Spaceship"
    # Game.space.append(ship)

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

    textShowBarycentre = Text("Afficher le barycentre", (20, 445), color=(255, 255, 255))
    interface.append(textShowBarycentre)

    showBarycentre = CheckBox((280, 441), False)
    showBarycentre.barycentre = None
    interface.append(showBarycentre)

    textShowSV = Text("Règle de mesure", (20, 555), color=(255, 255, 255))
    interface.append(textShowSV)

    showSV = CheckBox((175, 551), False)
    showSV.checked = True
    showSV.sv = None
    interface.append(showSV)

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
    dk.wait = False
    return

def load() -> None:
    for i in range(60):
        img = pg.image.load(path.join("./data/videos/loadingScreen", "%s.jpg" % i))
        img = pg.transform.scale(img, (108, 108))
        dk.loadingImages.append(img)
    dk.loadingFinished = False
    subprocess = Thread(target=loader)
    subprocess.start()
    Game.subprocess = subprocess
    return

def menu(screen) -> None:
    width, height = Game.screenSize
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
    width, height = Game.screenSize
    offset = 0

    pg.draw.rect(screen, (10, 9, 9), (width - 350, 0, 350, height))
    pg.draw.rect(screen, (0, 0, 0), (width - 340, 10, 330, 150))
    pg.draw.circle(screen, corps.color, (width - 165, 75), 20)

    if hasattr(corps, "name"):
        text = subtitle.render(corps.name, False, (255, 255, 255))
        screen.blit(text, (width - 330, 170))
        offset += 20
    
    if hasattr(corps, "description"):
        h: int = displayMultilineText(corps.description, description, (width - 330, 200), 330)
        offset += h + 30
    
    text = subtitle.render("Caractéristiques orbitaux", False, (255, 255, 255))
    screen.blit(text, (width - 330, 170 + offset))

    attractor = getattr(corps, "orbit", None) or getAttractor(corps)
    days: str = "%s jours" % round(orbitalPeriod(attractor.mass, Vectors.get_distance(corps.pos, attractor.pos)), 2) if attractor else "Inconnu"
    text = Game.font.render("Période de révolution : %s" % days, False, (255, 255, 255))
    screen.blit(text, (width - 330, 200 + offset))

    velocity: float = round(sqrt((corps.velocity[0] / C_EDUBANG) ** 2 + (corps.velocity[1] / C_EDUBANG) ** 2), 3)
    text = Game.font.render("Vitesse orbitale : %s km/s" % velocity, False, (255, 255, 255))
    screen.blit(text, (width - 330, 230 + offset))
    
    offset += 20

    text = subtitle.render("Caractéristiques physiques", False, (255, 255, 255))
    screen.blit(text, (width - 330, 260 + offset))

    text = Game.font.render("Rayon : %s km" % int(corps.radius), False, (255, 255, 255))
    screen.blit(text, (width - 330, 290 + offset))

    text = Game.font.render("Masse :", False, (255, 255, 255))
    screen.blit(text, (width - 330, 320 + offset))
    scientificNotation(corps.mass, (width - 267, 320 + offset), end="kg")

    surfaceGravity: float = round((G * corps.mass) / ((corps.radius * 1e3) ** 2), 3)
    text = Game.font.render("Gravité de surface : %s m/s²" % surfaceGravity, False, (255, 255, 255))
    screen.blit(text, (width - 330, 350 + offset))
    return

def sAfterOne(n: int) -> str:
    return "s" if n > 1 else ""

def showTime(screen) -> None:
    text: str = "Temps écoulé : 0 heure"
    if dk.timer > 0:
        date = toDate(dk.timer)
        text: str = "Temps écoulé : "
        if date[0] > 0:
            text += "%s an%s, " % (date[0], sAfterOne(date[0]))
        if date[1] > 0:
            text += "%s mois, " % date[1]
        if date[2] > 0:
            text += "%s semaine%s, " % (date[2], sAfterOne(date[2]))
        if date[3] > 0:
            text += "%s jour%s, " % (date[3], sAfterOne(date[3]))
        if date[4] > 0:
            text += "%s heure%s" % (date[4], sAfterOne(date[4]))
    
    w, h = Game.screenSize
    surface = Game.font.render(text, False, (255, 255, 255))
    screen.blit(surface, (380, h - 50))
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))
    width, height = Game.screenSize
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
        if hasattr(element, "barycentre"):
            showBarycentre = element.checked

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
        draw_attraction_norm(screen)

    if showPrediction:
        predict(Game, 200, 1)

    if showBarycentre:
        bX, bY = spacePosToScreenPos(barycentre(Game.space))
        pg.draw.line(screen, (0, 255, 0), (bX - 8, bY), (bX + 8, bY), 2)
        pg.draw.line(screen, (0, 255, 0), (bX, bY - 8), (bX, bY + 8), 2)

    showTime(screen)

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

    if dk.wait: return
    dk.timer += Game.DT * 2.195
    for corps in Game.space:
        # corps.update_position([0, 0], Game.DT)
        for otherCorps in Game.space:
            if corps == otherCorps: continue
            distance: float = updateCorps(corps, otherCorps)
            if isColliding(corps, otherCorps, distance):
                Game.space.remove(process_collide(corps, otherCorps))
    return