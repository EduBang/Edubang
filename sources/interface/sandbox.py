# Projet : EduBang
# Auteurs : Anaël Pernot-Chevillard, Sacha Fréguin, Néji Lim

from threading import Thread
from math import pi, sqrt

import pygame as pg
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from eventListen import Events
from nsi25perlin import PerlinNoise

from main import Game, getFont, brand, l, p
from shared.utils.utils import (
    C_EDUBANG, updateCorps, process_collide,
    MessageBox, Path, DataKeeper,
    Input, Text, CheckBox,
    Button, SizeViewer, loadSpaceIterated,
    loadStars, draw_velocity_vector,
    draw_cinetic_energy_vector, draw_attraction_norm, scientificNotation,
    spacePosToScreenPos, orbitalPeriod, C_EDUBANG,
    getAttractor, barycentre, toDate,
    displayMultilineText, setHelpMessage, displayRotatedImage,
    unit
)
from shared.components.Captors import isColliding
from shared.components.Prediction import predict
from shared.components.Physics import G
from shared.components.Vectors import Vectors

dk = DataKeeper()
dk.timeScale = None
dk.active = False
dk.loadingFinished = False
dk.loadingBar = 0
dk.loadingImage = pg.image.load(p("data/images/icons/orbitWhite.png"))
dk.orientation = 0
dk.image = None
dk.stars = []
dk.perlin = PerlinNoise(768)
dk.wait = True
dk.timer = 0
dk.specialKeys = []
dk.hideHUD = False
dk.escape = False
dk.screenShot = None
dk.pauseMenu = []
dk.help = False

def stopFocusFn() -> None:
    Game.Camera.focus = None
    Events.trigger("unhovering", dk.stopFocus)
    return

dk.stopFocus = None

description = getFont("Regular", 14)

interface: list = []

loadingText: str = l("loading")

subtitle = getFont("Bold")
icon = Image.open(p("data/images/icon.png"))
icon = icon.resize((398, 402), Image.Resampling.BICUBIC)
icon = ImageOps.expand(icon, border=20, fill=(0, 0, 0, 0))
icon = icon.filter(ImageFilter.GaussianBlur(10))
enhancer = ImageEnhance.Brightness(icon)
icon = enhancer.enhance(.075)
icon = pg.image.fromstring(icon.tobytes(), icon.size, icon.mode)

pauseIcon = pg.transform.scale(pg.image.load(p("data/images/brand.png")), (234, 54.9))
continueIcon = pg.transform.scale(pg.image.load(p("data/images/icons/continue.png")), (45, 45))
orbitIcon = pg.transform.scale(pg.image.load(p("data/images/icons/orbitBlack.png")), (45, 45))
settingsIcon = pg.transform.scale(pg.image.load(p("data/images/icons/settingsBlack.png")), (45, 45))
crossIcon = pg.transform.scale(pg.image.load(p("data/images/icons/cross.png")), (45, 45))

showPath: bool = False
showAttractionNorm: bool = False
showSV: bool = False
showNames: bool = True
showPrediction: bool = False
showBarycentre: bool = False

def setPauseButtonState(state: bool) -> None:
    for element in dk.pauseMenu:
        element.active = state
        if not state: Events.trigger("unhovering", element)
    return

def continueFn() -> None:
    dk.escape = False
    dk.screenShot = None
    dk.wait = False
    setPauseButtonState(False)
    return

def editFn() -> None:
    dk.escape = False
    dk.active = False
    dk.loadingFinished = False
    dk.image = None
    dk.stars = []
    dk.pauseMenu.clear()
    Game.resetSpace()
    Game.select("editor")
    return

def settingsFn() -> None:
    dk.escape = False
    dk.pauseMenu.clear()
    Game.select("settings")
    Events.trigger("SB2S")
    return

def quitFn() -> None:
    dk.escape = False
    dk.active = False
    dk.loadingFinished = False
    dk.image = None
    dk.stars = []
    dk.pauseMenu.clear()
    Game.space.clear()
    Game.select("menu")

@Events.observe
def window(w) -> None:
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
        keys.append(0x400000E0)
    if mods & pg.KMOD_LALT:
        keys.append(0x400000E2)
    keys.append(event.key)

    key = Game.getKeyFromCode(keys)

    if key:
        Game.keys[key] = True
    if Game.keys["help"]:
        dk.help = not dk.help
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
        x, y = spacePosToScreenPos(barycentre(Game.space))
        w, h = Game.screenSize
        Game.Camera.x = x + w / 2
        Game.Camera.y = y + h / 2
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
    if Game.keys["hideHUD"]:
        dk.hideHUD = not dk.hideHUD
        Events.trigger("hideHUD", dk.hideHUD)
    if Game.Camera.focus:
        if Game.keys["next"]:
            index = Game.space.index(Game.Camera.focus)
            if index + 1 == len(Game.space):
                Game.Camera.focus = Game.space[0]
                Game.Camera.zoom = 51 / Game.Camera.focus.radius
            else:
                Game.Camera.focus = Game.space[index + 1]
                Game.Camera.zoom = 51 / Game.Camera.focus.radius
        if Game.keys["previous"]:
            index = Game.space.index(Game.Camera.focus)
            if index - 1 < 1:
                Game.Camera.focus = Game.space[-1]
                Game.Camera.zoom = 51 / Game.Camera.focus.radius
            else:
                Game.Camera.focus = Game.space[index - 1]
                Game.Camera.zoom = 51 / Game.Camera.focus.radius
    key = event.key
    if not dk.active: return
    if key == pg.K_ESCAPE:
        if Game.Camera.focus:
            Game.Camera.focus = None
        else:
            if dk.hideHUD:  
                dk.hideHUD = False
                Events.trigger("hideHUD", dk.hideHUD)
            else:
                if not dk.escape:
                    dk.escape = True
                    sub = Game.screen.subsurface(pg.Rect(0, 0, *Game.screenSize))
                    img = pg.image.tobytes(sub, "RGB")
                    image = Image.frombytes("RGB", Game.screenSize, img)
                    image = image.filter(ImageFilter.GaussianBlur(10))
                    dk.screenShot = pg.image.fromstring(image.tobytes(), image.size, image.mode)
                    dk.wait = True
                    setPauseButtonState(True)
        
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
        dk.specialKeys.append(0x400000E0)
    if mods & pg.KMOD_LALT:
        dk.specialKeys.append(0x400000E2)
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

def loader() -> None:
    dk.wait = True
    Game.Camera.active = True
    x, y = spacePosToScreenPos(barycentre(Game.space))
    w, h = Game.screenSize
    Game.Camera.x = x + w / 2
    Game.Camera.y = y + h / 2
    dk.active = True

    if not dk.image:
        for i in loadSpaceIterated(dk.perlin):
            if isinstance(i, int):
                dk.loadingBar = 396 * i / 768
                continue
            space, size = i
            img = Image.new("RGB", (size, size))
            for pos in space:
                img.putpixel(pos, (space[pos]))
            img = img.resize((5 * size, 5 * size), Image.Resampling.LANCZOS)
            dk.image = pg.image.fromstring(img.tobytes(), img.size, img.mode)
        dk.stars = loadStars(1500, (-3000, 3000))

    textDT = Text("%s : " % l("timeScale"), (20, 145), color=(255, 255, 255))
    interface.append(textDT)

    inputDT = Input(str(Game.timeScale), (180, 145), (100, 40))
    def inputDTdraw():
        color = (0, 0, 255) if inputDT.focus else (255, 255, 255)
        surface = Game.font.render(inputDT.text, False, color)
        dim = Game.font.size(inputDT.text)
        x = inputDT.position[0]
        y = inputDT.position[1] + inputDT.size[1] // 2 - dim[1] // 2 - 10
        Game.screen.blit(surface, (x, y))
        u, e = l("timeScaleUnit").split(" ")
        unit(u, e, (x + dim[0] + 4, y), color=color)

    inputDT.draw = inputDTdraw
    inputDT.numberOnly = True
    inputDT.resetOnClick = True
    interface.append(inputDT)

    textWarning1 = Text(l("dtWarning1"), (20, 178), color = (255, 255, 255))
    interface.append(textWarning1)

    textWarning2 = Text(l("dtWarning2"), (20, 198), color = (255, 255, 255))
    interface.append(textWarning2)


    textShowName = Text(l("planetName"), (20, 285), color=(255, 255, 255))
    interface.append(textShowName)

    showNames = CheckBox((280, 285), True)
    showNames.sn = None
    interface.append(showNames)

    textShowPath = Text(l("planetTrajectory"), (20, 335), color=(255, 255, 255))
    interface.append(textShowPath)

    showPath = CheckBox((280, 335), False)
    showPath.trajectoire = None
    interface.append(showPath)
    
    textShowAttractionNorm = Text(l("planetAttraction"), (20, 385), color=(255, 255, 255))
    interface.append(textShowAttractionNorm)

    
    showAttractionNorm = CheckBox((280, 385), False)
    showAttractionNorm.attraction_norm = None
    interface.append(showAttractionNorm)

    textShowPrediction = Text(l("planetPrediction"), (20, 435), color=(255, 255, 255))
    interface.append(textShowPrediction)

    showPrediction = CheckBox((280, 435), False)
    showPrediction.prediction = None
    interface.append(showPrediction)

    textShowBarycentre = Text(l("planetBarycenter"), (20, 485), color=(255, 255, 255))
    interface.append(textShowBarycentre)

    showBarycentre = CheckBox((280, 485), False)
    showBarycentre.barycentre = None
    interface.append(showBarycentre)

    textShowSV = Text(l("rules"), (20, 585), color=(255, 255, 255))
    interface.append(textShowSV)

    showSV = CheckBox((280, 585), False)
    showSV.checked = True
    showSV.sv = None
    interface.append(showSV)

    sizeViewer = SizeViewer((w - 200, h - 50))
    sizeViewer.measure = None
    interface.append(sizeViewer)

    stopFocus = Button((w - 340, h - 60), (330, 50))
    stopFocus.text = l("disableFocus")
    stopFocus.onPressed = stopFocusFn
    stopFocus.active = False
    interface.append(stopFocus)
    dk.stopFocus = stopFocus

    continueButton = Button((0, 0), (400, 50))
    continueButton.text = l("continue")
    continueButton.onPressed = continueFn
    continueButton.icon = continueIcon
    continueButton.active = False
    interface.append(continueButton)
    dk.pauseMenu.append(continueButton)

    editButton = Button((0, 0), (400, 50))
    editButton.text = l("edit")
    editButton.onPressed = editFn
    editButton.icon = orbitIcon
    editButton.active = False
    interface.append(editButton)
    dk.pauseMenu.append(editButton)

    settingsButton = Button((0, 0), (400, 50))
    settingsButton.text = l("settings")
    settingsButton.onPressed = settingsFn
    settingsButton.icon = settingsIcon
    settingsButton.active = False
    interface.append(settingsButton)
    dk.pauseMenu.append(settingsButton)

    quitButton = Button((0, 0), (400, 50))
    quitButton.text = l("quit")
    quitButton.onPressed = quitFn
    quitButton.icon = crossIcon
    quitButton.active = False
    interface.append(quitButton)
    dk.pauseMenu.append(quitButton)

    dk.loadingFinished = True
    dk.wait = False
    return

def load() -> None:
    dk.loadingFinished = False
    subprocess = Thread(target=loader)
    subprocess.start()
    Game.subprocess = subprocess
    return

def menu(screen) -> None:
    _, height = Game.screenSize
    pg.draw.rect(screen, (10, 9, 9), (0, 0, 350, height))

    screen.blit(brand, (20, 20))
    screen.blit(icon, (-150, height - 320))

    text = subtitle.render(l("parameterSimulation"), False, (255, 255, 255))
    screen.blit(text, (20, 100))
    pg.draw.line(screen, (102, 102, 102), (20, 130), (200, 130))

    text = subtitle.render(l("renderingParameter"), False, (255, 255, 255))
    screen.blit(text, (20, 240))
    pg.draw.line(screen, (102, 102, 102), (20, 270), (200, 270))

    text = subtitle.render(l("tools"), False, (255, 255, 255))
    screen.blit(text, (20, 540))
    pg.draw.line(screen, (102, 102, 102), (20, 570), (200, 570))

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
    
    text = subtitle.render(l("orbitalCharacteristics"), False, (255, 255, 255))
    screen.blit(text, (width - 330, 170 + offset))
    pg.draw.line(screen, (102, 102, 102), (width - 330, 200 + offset), (width - 150, 200 + offset))

    attractor = getattr(corps, "orbit", None) or getAttractor(corps)
    days: str = "%s %s" % (round(orbitalPeriod(attractor.mass, Vectors.get_distance(corps.pos, attractor.pos)), 2) if attractor else l("revolutionPeriodUnknown"), l("revolutionPeriodUnit"))
    text = Game.font.render("%s : %s" % (l("revolutionPeriod"), days), False, (255, 255, 255))
    screen.blit(text, (width - 330, 210 + offset))

    velocity: float = round(sqrt((corps.velocity[0] / C_EDUBANG) ** 2 + (corps.velocity[1] / C_EDUBANG) ** 2), 3)
    text = Game.font.render("%s : %s" % (l("orbitalVelocity"), velocity), False, (255, 255, 255))
    w, h = Game.font.size("%s : %s" % (l("orbitalVelocity"), velocity))
    screen.blit(text, (width - 330, 240 + offset))
    u, e = l("orbitalVelocityUnit").split(" ")
    unit(u, e, (width - 325 + w, 240 + offset))
    
    offset += 20

    text = subtitle.render(l("physicalCharacteristics"), False, (255, 255, 255))
    screen.blit(text, (width - 330, 300 + offset))
    pg.draw.line(screen, (102, 102, 102), (width - 330, 330 + offset), (width - 150, 330 + offset))

    text = Game.font.render("%s : %s %s" % (l("radius"), int(corps.radius), l("radiusUnit")), False, (255, 255, 255))
    screen.blit(text, (width - 330, 340 + offset))

    text = Game.font.render("%s :" % l("mass"), False, (255, 255, 255))
    i, _ = Game.font.size("%s :" % l("mass"))
    screen.blit(text, (width - 330, 370 + offset))
    scientificNotation(corps.mass, (width - 330 + i + 5, 370 + offset), end=l("massUnit"))

    surfaceGravity: float = round((G * corps.mass) / ((corps.radius * 1e3) ** 2), 3)
    text = Game.font.render("%s : %s" % (l("surfaceGravity"), surfaceGravity), False, (255, 255, 255))
    w, h = Game.font.size("%s : %s" % (l("surfaceGravity"), surfaceGravity))
    screen.blit(text, (width - 330, 400 + offset))
    u, e = l("surfaceGravityUnit").split(" ")
    unit(u, e, (width - 325 + w, 400 + offset))
    return

def sAfterOne(n: int, ident: str) -> str:
    return l("%ss" % ident) if n > 1 else l(ident)

def showTime(screen) -> None:
    text: str = "%s : 0 %s" % (l("timeElapsed"), l("hour"))
    if dk.timer > 0:
        date = toDate(dk.timer)
        text: str = "%s : " % l("timeElapsed")
        if date[0] > 0:
            text += "%s %s, " % (date[0], sAfterOne(date[0], "year"))
        if date[1] > 0:
            text += "%s %s, " % (date[1], l("month"))
        if date[2] > 0:
            text += "%s %s, " % (date[2], sAfterOne(date[2], "week"))
        if date[3] > 0:
            text += "%s %s, " % (date[3], sAfterOne(date[3], "day"))
        if date[4] > 0:
            text += "%s %s" % (date[4], sAfterOne(date[4], "hour"))
    
    _, h = Game.screenSize
    surface = Game.font.render(text, False, (255, 255, 255))
    screen.blit(surface, (380, h - 50))
    return

def drawEscapeMenu() -> None:
    if not dk.escape: return
    Game.screen.blit(dk.screenShot, (0, 0))
    Game.screen.blit(pauseIcon, (Game.screenSize[0] // 2 - 117, Game.screenSize[1] // 2 - 175))
    for element in dk.pauseMenu:
        element.position = [Game.screenSize[0] // 2 - 200, Game.screenSize[1] // 2 - 75 + dk.pauseMenu.index(element) * 70]
        element.draw()
    return

def showHelp() -> None:
    if not dk.help: return
    surface = pg.Surface((Game.screenSize), pg.SRCALPHA)
    surface.fill((0, 0, 0, 128))

    w, h = Game.screenSize

    setHelpMessage(surface, (20, 145), (300, 25), 4, (400, 50), (200, 100), l("help1"))
    setHelpMessage(surface, (20, 245), (300, 225), 4, (400, 200), (200, 100), l("help2"))
    setHelpMessage(surface, (20, 555), (300, 25), 4, (400, 350), (200, 100), l("help3"))
    setHelpMessage(surface, (380, h - 50), (350, 25), 1, (400, h - 225), (200, 100), l("help4"))

    if Game.Camera.focus:
        setHelpMessage(surface, (w - 330, 170), (300, 50), 2, (w - 630, 50), (200, 100), l("help5"))
        setHelpMessage(surface, (w - 330, 280), (300, 55), 2, (w - 630, 200), (200, 100), l("help6"))
        setHelpMessage(surface, (w - 330, 430), (300, 85), 2, (w - 630, 350), (200, 100), l("help7"))
        setHelpMessage(surface, (w - 340, h - 60), (330, 50), 2, (w - 630, h - 225), (200, 100), l("help8"))

    Game.screen.blit(surface, (0, 0))
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))
    width, height = Game.screenSize
    if not dk.loadingFinished:
        text = Game.font.render(loadingText, False, (255, 255, 255))
        tW, tH = Game.font.size(loadingText)
        screen.blit(text, (width / 2 - tW + 70, height / 2 - tH / 2))
        displayRotatedImage(screen, dk.loadingImage, (width / 2 - tW, height / 2), dk.orientation)
        pg.draw.rect(screen, (255, 255, 255), (width / 2 - 200, height / 2 + 150, 400, 20), 1)
        pg.draw.rect(screen, (255, 255, 255), (width / 2 - 198, height / 2 + 152, dk.loadingBar, 16))
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
        


    if showAttractionNorm:
        draw_attraction_norm(screen)

    if showPrediction:
        predict(Game, 40, 5)

    if showBarycentre:
        bX, bY = spacePosToScreenPos(barycentre(Game.space))
        pg.draw.line(screen, (0, 255, 0), (bX - 8, bY), (bX + 8, bY), 2)
        pg.draw.line(screen, (0, 255, 0), (bX, bY - 8), (bX, bY + 8), 2)

    if not dk.hideHUD:
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
            text = Game.font.render(l("pause"), False, (255, 255, 255))
            tW, tH = Game.font.size(l("pause"))
            screen.blit(text, (width // 2 - tW // 2, height // 2 - tH // 2 - 200))

        showHelp()
        drawEscapeMenu()
    return

def update() -> None:
    if not dk.loadingFinished:
        dk.orientation += 1
        if dk.orientation > 359:
            dk.orientation = 0

    if dk.wait: return
    dk.timer += Game.DT * 2.195
    for corps in Game.space:
        corps.update_position([0, 0], Game.DT)
        for otherCorps in Game.space:
            if corps == otherCorps: continue
            distance: float = updateCorps(corps, otherCorps)
            if isColliding(corps, otherCorps, distance):
                Game.space.remove(process_collide(corps, otherCorps))
    return
