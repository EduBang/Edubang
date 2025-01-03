from json import dumps
from json import load as loadJson
from os import listdir, path

from eventListen import Events

from main import Game, getFont
from shared.utils.utils import Button, DataKeeper, KeyBind, Text

dk = DataKeeper()

interface: list = []

@Events.observe
def window(w) -> None:
    if w != "keybind": return
    interface.clear()
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

def load() -> None:
    backButton = Button((100, 200), (180, 60))
    backButton.text = "Retour"
    backButton.onPressed = backFunction
    interface.append(backButton)

    h: int = 100
    keybindsFiles = [path.join("data/settings", f) for f in listdir("data/settings") if path.isfile(path.join("data/settings", f))]
    for i, keybindFile in enumerate(keybindsFiles):
        keybinds = {}
        with open(keybindFile, "r", encoding="utf-8") as f:
            keybinds = loadJson(f)
            f.close()
        title = Text(keybindFile.split("\\")[1][:-5], (500, h), color=(255, 255, 255))
        title.font = getFont("Bold", 24)
        title.scrollable = True
        interface.append(title)
        h += 70
        for j, k in enumerate(keybinds):
            keybind = keybinds[k]
            kb = KeyBind(keybind["code"], keybind["key"], (700, h))
            kb.kb = (k, keybind)
            kb.file = keybindFile
            kb.scrollable = True
            text = Text(keybind["name"], (400, h + 10), color=(255, 255, 255))
            text.scrollable = True
            interface.append(kb)
            interface.append(text)
            h += 70
        h += 50
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))
    surface = Game.title.render("Contrôles", False, (255, 255, 255))
    screen.blit(surface, (100, 100))

    for element in interface:
        element.draw()
    return

def update() -> None:
    return