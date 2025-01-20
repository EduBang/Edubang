from json import dumps
from json import load as loadJson
from os import listdir, path

from eventListen import Events

from main import Game, getFont
from shared.utils.utils import Button, DataKeeper, KeyBind, Text, Button, SCROLL_SPEED, l

dk = DataKeeper()   
dk.offsetY = 0
dk.intScroll = (float("-inf"), float("+inf")) # On s'inspire de la notation mathématique des intervalles : ]-∞;+∞[

interface: list = []

@Events.observe
def window(w) -> None:
    if w != "keybind": return
    interface.clear()
    dk.offsetY = 0
    dk.intScroll = (float("-inf"), float("+inf")) 
    return

@Events.observe
def mousewheel(event) -> None:
    if Game.window != "keybind": return
    if dk.offsetY + SCROLL_SPEED <= dk.intScroll[1] and event.y > 0 or dk.offsetY - SCROLL_SPEED >= dk.intScroll[0] and event.y < 0:
        Events.trigger("positionChanged", event.y * SCROLL_SPEED)
        dk.offsetY += event.y * SCROLL_SPEED
    return

def positionChanged(self, y) -> None:
    self.position[1] += y
    return

def backFunction() -> None:
    newKeybinds: dict = {}
    for keybind in interface:
        kb = getattr(keybind, "kb", None)
        if not kb: continue

        nkb = {
            "name": kb[1]["name"],
            "code": keybind.keys,
            "key": keybind.keyname
        }

        with open(keybind.file, "r", encoding="utf-8") as rf:
            content = loadJson(rf)
            rf.close()
        content.update({kb[0]: nkb})
        with open(keybind.file, "w", encoding="utf-8") as wf:
            wf.write(dumps(content))
            wf.close()
        
        newKeybinds[kb[0]] = nkb

    Game.keybinds = newKeybinds
    Game.resetKeys()
    Game.select("settings")
    return

def resetKeybinds() -> None:
    Game.resetKeybinds()
    i: int = 0
    keybinds: list = list(Game.keybinds)
    for element in interface:
        if element.size == (180, 60): continue

        if hasattr(element, "kb"):
            keybind = keybinds[i]
            k = Game.keybinds[keybind]
            element.keys = k["code"]
            element.keyname = k["key"]
            element.kb = (keybind, k)
            i += 1
        
    return

def load() -> None:
    backButton = Button((100, 200), (180, 60))
    backButton.text = l("back")
    backButton.onPressed = backFunction
    interface.append(backButton)

    resetButton = Button((100, 300), (180, 60))
    resetButton.text = l("reset")
    resetButton.onPressed = resetKeybinds
    interface.append(resetButton)

    h: int = 100
    keybindsFiles = [path.join("data/settings", f) for f in listdir("data/settings") if path.isfile(path.join("data/settings", f))]
    for keybindFile in keybindsFiles:
        keybinds = {}
        with open(keybindFile, "r", encoding="utf-8") as f:
            keybinds = loadJson(f)
            f.close()
        title = Text(keybindFile[14:-5], (500, h), color=(255, 255, 255))
        title.font = getFont("Bold", 24)
        Events.setEvent(title, "positionChanged", positionChanged)
        interface.append(title)
        h += 70
        for k in keybinds:
            keybind = keybinds[k]
            kb = KeyBind(keybind["code"], keybind["key"], (700, h))
            kb.kb = (k, keybind)
            kb.file = keybindFile
            Events.setEvent(kb, "positionChanged", positionChanged)
            text = Text(keybind["name"], (400, h + 10), color=(255, 255, 255))
            Events.setEvent(text, "positionChanged", positionChanged)
            interface.append(text)
            interface.append(kb)
            h += 70
        h += 50

    dk.intScroll = (-h + Game.screenSize[1], 0)
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))
    surface = Game.title.render(l("title"), False, (255, 255, 255))
    screen.blit(surface, (100, 100))

    for element in interface:
        element.draw()
    return

def update() -> None:
    return