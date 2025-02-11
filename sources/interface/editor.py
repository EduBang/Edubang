# Projet : EduBang
# Auteurs : Anaël Chevillard, Sacha Fréguin, Néji Lim

from json import dumps
from json import load as loadJson
from os import listdir, path
from math import pi, sqrt
from datetime import datetime

import pygame as pg
from eventListen import Events

from main import Game, getFont, brand, l, p
from shared.components.Corps import Corps
from shared.components.Prediction import predict
from shared.utils.utils import DataKeeper, Button, spacePosToScreenPos, getSize, screenPosToSpacePos, Input, barycentre, drawArrow, MessageBox, Enums, Card

dk = DataKeeper()
dk.body = None
dk.mouseselection = None
dk.selected = []
dk.specialKeys = []
dk.saving = False
dk.saveTarget = []
dk.saveCanva = {}
dk.standBy = False
dk.tsave = None
dk.target = None
dk.arrows = {}
dk.bodies = []
dk.hideHUD = False
dk.mb = None
dk.hover = None
dk.shift = False
dk.selectRect = []
dk.moveSelected = False
dk.relativePos = {}

semibold = getFont("SemiBold", 16)
subtitle = getFont("Bold")
unitFont = getFont("Regular", 12)

interface: list = []

def pause() -> None:
    dk.standBy = True
    Game.Camera.active = False
    return

def resume() -> None:
    dk.standBy = False
    Game.Camera.active = True

def minimum(startPos, endPos) -> tuple:
    x1, y1 = startPos
    x2, y2 = endPos
    return (min(x1, x2), min(y1, y2))

def maximum(startPos, endPos) -> tuple:
    x1, y1 = startPos
    x2, y2 = endPos
    return (max(x1, x2), max(y1, y2))

def getSelectRect() -> tuple[float, float, float, float]:
    """
    Calcule les coordonnées ainsi que les dimensions du rectangle de sélection

    Arguments:
        None

    Retourne:
        tuple[float, float, float, float]: Les coordonnées et les dimensions du rectangle de sélection
    """
    c = dk.selected[0]
    pos: tuple[float, float] = spacePosToScreenPos(c.pos)
    x1 = pos[0] - c.radius * Game.Camera.zoom
    y1 = pos[1] - c.radius * Game.Camera.zoom
    x2 = pos[0] + c.radius * Game.Camera.zoom
    y2 = pos[1] + c.radius * Game.Camera.zoom
    for selected in dk.selected:
        x, y = spacePosToScreenPos(selected.pos)
        pg.draw.circle(Game.screen, (255, 255, 255), (x, y), selected.radius * Game.Camera.zoom, 1)
        dx1, dy1 = x - selected.radius * Game.Camera.zoom, y - selected.radius * Game.Camera.zoom
        dx2, dy2 = x + selected.radius * Game.Camera.zoom, y + selected.radius * Game.Camera.zoom
        if dx1 < x1:
            x1 = dx1
        if dy1 < y1:
            y1 = dy1
        if dx2 > x2:
            x2 = dx2
        if dy2 > y2:
            y2 = dy2
    return [x1, y1, x2 - x1, y2 - y1]

def resetSaveCanva() -> None:
    saveButton, inputName, inputDescription = [dk.saveCanva[i] for i in ("save", "name", "description")]
    dk.saving = False
    dk.saveTarget.clear()
    saveButton.active = False
    inputName.active = False
    inputName.visible = False
    inputName.text = ""
    inputDescription.active = False
    inputDescription.visible = False
    inputDescription.text = ""
    dk.standBy = False
    Game.Camera.active = True
    return

def doSave() -> None:
    name: str = dk.saveCanva["name"].text
    if not name:
        message = l("err1")
        if len(dk.saveTarget) == 1:
            message = l("err2")
        dk.tsave = [5, message, (255, 0, 0)]
        
        return
    description: str = dk.saveCanva["description"].text
    fileName: str = name.replace(" ", "_").lower()

    if len(dk.saveTarget) == 1:
        body: dict = {
            "mass": dk.saveTarget[0].mass,
            "radius": dk.saveTarget[0].radius,
            "color": dk.saveTarget[0].color,
            "meta": {
                "name": name,
                "description": description,
            }
        }
        with open(p("data/bodies/%s.json" % fileName), "w+", encoding="utf-8") as f:
            f.write(dumps(body, indent=4))
            f.close()
        body["file"] = p("data/bodies/%s.json" % fileName)
        c = Card(body, (0, 0))
        dk.bodies.append(c)
    else:
        with open(p("data/systems/%s.ebs" % fileName), "w+", encoding="utf-8") as f:
            space: list = []
            for corps in dk.saveTarget:
                meta = {}
                if hasattr(corps, "name"):
                    meta["name"] = corps.name
                if hasattr(corps, "description"):
                    meta["description"] = corps.description
                space.append({
                    "mass": corps.mass,
                    "radius": corps.radius,
                    "position": corps.pos,
                    "color": corps.color,
                    "velocity": corps.velocity,
                    "meta": meta
                })
            data: dict = {}
            data["title"] = name
            data["description"] = description
            data["meta"] = {
                "user": Game.user,
                "lastModified": int(datetime.now().timestamp())
            }
            data["space"] = space

            f.write(dumps(data, indent=4))
            f.close()
    resetSaveCanva()
    dk.tsave = [5, "%s %s" % (name, l("saved")), (0, 255, 0)]
    return

@Events.observe
def keydown(event) -> None:
    if Game.window != "editor": return
    key = event.key

    if not dk.hideHUD:
        if key == pg.K_ESCAPE:
            if dk.saving: resetSaveCanva()
            elif dk.body: dk.body = None
            elif Game.Camera.focus: Game.Camera.focus = None
            else:
                if dk.mb.active:
                    dk.mb.active = False
                    dk.active = False
                    dk.loadingFinished = False
                    dk.image = None
                    dk.stars = []
                    dk.bodies = []
                    dk.mb = None
                    Game.reset()
                    Game.select("menu")
                else:
                    dk.mb.active = True

        if dk.standBy: return
        
        if key == pg.K_KP_PLUS and Game.Camera.zoom < Game.Camera.maxZoom:
            Game.Camera.zoom *= 1.05
        elif key == pg.K_KP_MINUS and Game.Camera.zoom > Game.Camera.minZoom:
            Game.Camera.zoom /= 1.05
        
        dk.shift = key == pg.K_LSHIFT

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

    if Game.keys["hideHUD"]:
        dk.hideHUD = not dk.hideHUD
        Events.trigger("hideHUD", dk.hideHUD)
    
    if dk.hideHUD: return
    if Game.keys["delete"]:
        for corps in dk.selected:
            Game.space.remove(corps)
        dk.selected.clear()
    if Game.keys["selectAll"]:
        dk.selected = Game.space.copy()
    if Game.keys["save"] and len(dk.selected) > 0:
        dk.saving = True
        dk.saveTarget = dk.selected.copy()
        Game.keys[key] = False
    return

@Events.observe
def keyup(event) -> None:
    if Game.window != "editor": return
    if dk.standBy: return
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
    
    key = event.key
    dk.shift = key == pg.K_LSHIFT
    return

@Events.observe
def inventory(body) -> None:
    dk.body = body
    Game.Camera.zoom = 51 / body["radius"]
    return

@Events.observe
def mousebuttondown(event) -> None:
    if Game.window != "editor": return
    if dk.hideHUD: return
    button = event.button
    pos = event.pos
    if button != 1: return
    body = dk.body
    if body:
        pos = event.pos
        corps = Corps(body["mass"], body["radius"], screenPosToSpacePos(pos), body["color"], (0, 0))
        for meta in body["meta"]:
            setattr(corps, meta, body["meta"][meta])
        Game.space.append(corps)
        dk.body = None
    else:
        for arrow in dk.arrows:
            x, y = dk.arrows[arrow]
            sqx, sqy = (pos[0] - x) ** 2, (pos[1] - y) ** 2
            if sqrt(sqx + sqy) < 10:
                dk.target = arrow
                break
        else:
            if not dk.selectRect: return
            if dk.selectRect[0] < pos[0] < dk.selectRect[0] + dk.selectRect[2] and dk.selectRect[1] < pos[1] < dk.selectRect[1] + dk.selectRect[3]:
                dk.moveSelected = True
                for corps in dk.selected:
                    rPos = screenPosToSpacePos(pos)
                    dk.relativePos[corps] = (corps.pos[0] - rPos[0], corps.pos[1] - rPos[1])
            else:
                Game.Camera.focus = None 
                dk.selected.clear()
                dk.relativePos.clear()
                dk.mouseselection = screenPosToSpacePos(pos)
    return

@Events.observe
def mousebuttonup(event) -> None:
    if Game.window != "editor": return
    if dk.hideHUD: return
    button = event.button
    pos = event.pos
    if button != 1: return
    if dk.moveSelected:
        dk.moveSelected = False
    if dk.mouseselection:
        dk.mouseselection = None
    if dk.target:
        targetPos = spacePosToScreenPos(dk.target.pos)
        x = (pos[0] - targetPos[0]) / Game.Camera.zoom
        y = (pos[1] - targetPos[1]) / Game.Camera.zoom
        dk.target.velocity = [x, y]
        dk.target = None
    for corps in Game.space:
        x, y = spacePosToScreenPos(corps.pos)
        sqx, sqy = (pos[0] - x) ** 2, (pos[1] - y) ** 2
        if pi * (corps.radius * Game.Camera.zoom) ** 2 < 10:
            if sqrt(sqx + sqy) < 10:
                Game.Camera.focus = corps
                break
        if sqrt(sqx + sqy) < corps.radius * Game.Camera.zoom:
            Game.Camera.focus = corps
            break
    if dk.hover:
        if dk.hover in dk.selected: return
        if not dk.shift:
            dk.selected.clear()
        dk.selected.append(dk.hover)
    return

def drawGrid() -> None:
    w, distance, unit = getSize()
    screen = Game.screen
    width, height = Game.screenSize
    k: int = int(width // w)
    for i in range(-5 * k, 5 * k):
        color: tuple[int, int, int] = (100, 100, 100) if i != 0 else (255, 255, 255)
        s: float = i * w / Game.Camera.zoom
        pg.draw.line(screen, color, spacePosToScreenPos((s, -Game.Camera.y / Game.Camera.zoom)), spacePosToScreenPos((s, (height - Game.Camera.y) / Game.Camera.zoom)), 1)
        pg.draw.line(screen, color, spacePosToScreenPos((-Game.Camera.x / Game.Camera.zoom, s)), spacePosToScreenPos(((width - Game.Camera.x) / Game.Camera.zoom, s)), 1)
        text: str = "%s %s" % (abs(distance * i), unit)
        surface = unitFont.render(text, False, (255, 255, 255))
        screen.blit(surface, spacePosToScreenPos((s, 0)))
        screen.blit(surface, spacePosToScreenPos((0, s)))
    return

def drawMouseSelection() -> None:
    if dk.mouseselection:
        startPos = spacePosToScreenPos(dk.mouseselection)
        endPos = pg.mouse.get_pos()
        pos = minimum(startPos, endPos)
        w, h = abs(endPos[0] - startPos[0]), abs(endPos[1] - startPos[1])
        surface = pg.Surface((w, h))
        surface.set_alpha(100)
        surface.fill((54, 156, 235))
        Game.screen.blit(surface, pos)
    return

def drawSelected() -> None:
    if dk.hover and dk.hover in Game.space:
        x, y = spacePosToScreenPos(dk.hover.pos)
        pg.draw.circle(Game.screen, (255, 255, 255), (x, y), dk.hover.radius * Game.Camera.zoom, 1)
    if len(dk.selected) < 1: return
    dk.selectRect = getSelectRect()
    pg.draw.rect(Game.screen, (255, 255, 255), dk.selectRect, 1)

    bX, bY = spacePosToScreenPos(barycentre(dk.selected))
    pg.draw.line(Game.screen, (0, 255, 0), (bX - 8, bY), (bX + 8, bY), 2)
    pg.draw.line(Game.screen, (0, 255, 0), (bX, bY - 8), (bX, bY + 8), 2)
    return

def drawSaving(width, height) -> None:
    if not dk.saving: return
    x, y = (width - 900) // 2, (height - 450) // 2
    pg.draw.rect(Game.screen, (10, 9, 9), (x, y, 900, 450))
    pg.draw.rect(Game.screen, (255, 255, 255), (x, y, 900, 450), 1)

    saveButton, inputName, inputDescription = [dk.saveCanva[i] for i in ("save", "name", "description")]
    inputName.position = (x + 10, y + 10)
    inputDescription.position = (x + 10, y + 80)
    saveButton.position = (x + 10, y + 380)
    if not saveButton.active:
        saveButton.active = True
        inputName.active = True
        inputName.visible = True
        inputDescription.active = True
        inputDescription.visible = True
    return

def drawVelocityArrow() -> None:
    if not dk.target: return
    targetPos = spacePosToScreenPos(dk.target.pos)
    mousePos = pg.mouse.get_pos()
    drawArrow(targetPos, mousePos)
    targetPos = spacePosToScreenPos(dk.target.pos)
    x = (mousePos[0] - targetPos[0]) / Game.Camera.zoom
    y = (mousePos[1] - targetPos[1]) / Game.Camera.zoom
    dk.target.velocity = [x, y]
    return

def drawInventory(h: int) -> None:
    pg.draw.rect(Game.screen, Enums.Background, (0, 0, 300, h))

    Game.screen.blit(brand, (20, 20))

    text = subtitle.render(l("preset"), False, (255, 255, 255))
    Game.screen.blit(text, (20, 100))
    pg.draw.line(Game.screen, (102, 102, 102), (20, 130), (100, 130))

    temp = dk.bodies.copy()
    i = 0
    while len(temp) > 0:
        for j in range(3):
            if len(temp) < 1: break
            card = temp.pop(0)
            card.position = (20 + 90 * j, 160 + 110 * i)
            card.draw()
        i += 1

    return

def load() -> None:
    Game.timeScale = 1
    Game.Camera.active = True
    Game.Camera.zoom = 1
    w, h = Game.screenSize
    Game.Camera.x = w // 2
    Game.Camera.y = h // 2

    bodyFiles = [path.join(p("data/bodies"), f) for f in listdir(p("data/bodies")) if path.isfile(path.join(p("data/bodies"), f))]
    for i, bodyFile in enumerate(bodyFiles):
        body = {}
        with open(bodyFile, "r", encoding="utf-8") as f:
            body = loadJson(f)
            body["file"] = bodyFile
            c = Card(body, (0, 0))
            f.close()
        dk.bodies.append(c)

    saveButton = Button((0, 0), (180, 60))
    saveButton.text = l("save")
    saveButton.font = semibold
    saveButton.onPressed = doSave
    saveButton.active = False
    interface.append(saveButton)
    dk.saveCanva["save"] = saveButton

    inputName = Input("", (0, 0), (180, 60))
    inputName.name = None
    inputName.placeholder = l("name")
    inputName.active = False
    inputName.visible = False
    inputName.onPressed = pause
    inputName.afterInput = resume
    interface.append(inputName)
    dk.saveCanva["name"] = inputName

    inputDescription = Input("", (0, 0), (180, 60))
    inputDescription.description = None
    inputDescription.placeholder = l("description")
    inputDescription.active = False
    inputDescription.visible = False
    inputDescription.onPressed = pause
    inputDescription.afterInput = resume
    interface.append(inputDescription)
    dk.saveCanva["description"] = inputDescription

    dk.mb = MessageBox(l("returnToMenu"))

    return

def stats(corps, width, height) -> None:
    screen = Game.screen
    pg.draw.rect(screen, (10, 9, 9), (width - 350, 0, 350, height))
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))
    width, height = Game.screenSize

    drawGrid()

    for corps in Game.space:
        corps.draw(screen, Game.Camera)
        pos = spacePosToScreenPos(corps.pos)
        x = pos[0] + corps.velocity[0] * Game.Camera.zoom
        y = pos[1] + corps.velocity[1] * Game.Camera.zoom
        drawArrow(pos, (x, y))
        dk.arrows[corps] = (x, y)

    predict(Game, 250, 1)

    if not dk.hideHUD:
        drawSelected()
        drawMouseSelection()
        drawVelocityArrow()

        if dk.body:
            pos = pg.mouse.get_pos()
            radius: float | int = dk.body["radius"]
            pg.draw.circle(screen, (255, 255, 255), pos, radius * Game.Camera.zoom, 1)

        if Game.Camera.focus:
            stats(Game.Camera.focus, width, height)

        drawSaving(width, height)

        drawInventory(height)

        for element in interface:
            element.draw()

        if dk.tsave:
            dk.tsave[0] -= (Game.deltaTime * 2.195)
            width, height = Game.screenSize
            text: str = dk.tsave[1]
            surface = Game.italic.render(text, False, dk.tsave[2])
            surface.set_alpha(int(255 * dk.tsave[0] / 5))
            tW, tH = Game.italic.size(text)
            screen.blit(surface, (width // 2 - tW // 2, height // 2 - tH // 2 + 300))
            if dk.tsave[0] <= 0:
                dk.tsave = None

        dk.mb.draw()
    return

def update() -> None:
    if dk.mouseselection:
        pos = screenPosToSpacePos(pg.mouse.get_pos())
        mini = minimum(dk.mouseselection, pos)
        maxi = maximum(dk.mouseselection, pos)
        for corps in Game.space:
            if mini[0] < corps.pos[0] < maxi[0] and mini[1] < corps.pos[1] < maxi[1]:
                if corps not in dk.selected:
                    dk.selected.append(corps)
            else:
                if corps in dk.selected:
                    dk.selected.remove(corps)
    pos = pg.mouse.get_pos()
    if dk.moveSelected:
        spos = screenPosToSpacePos(pos)
        for corps in dk.selected:
            corps.pos = (dk.relativePos[corps][0] + spos[0], dk.relativePos[corps][1] + spos[1])

    for corps in Game.space:
        x, y = spacePosToScreenPos(corps.pos)
        sqx, sqy = (pos[0] - x) ** 2, (pos[1] - y) ** 2
        if sqrt(sqx + sqy) < corps.radius * Game.Camera.zoom:
            dk.hover = corps
            break
    else:
        dk.hover = None
    return
