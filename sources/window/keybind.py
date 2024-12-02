import json
from os import listdir, path

from eventListen import Events

from main import Game, getFont
from shared.utils.utils import Button, DataKeeper, KeyBind, Text

dk = DataKeeper()

interface = []

@Events.observe
def window(w) -> None:
    interface.clear()
    return

def backFunction() -> None:
    newKeybinds = {}
    for keybind in interface:
        kb = getattr(keybind, "kb", None)
        if not kb: continue

        nkb = {
            "name": kb[1]["name"],
            "code": keybind.key,
            "key": keybind.keyname
        }

        with open(keybind.file, "r", encoding="utf-8") as rf:
            content = json.load(rf)
            rf.close()
        content.update({kb[0]: nkb})
        with open(keybind.file, "w", encoding="utf-8") as wf:
            wf.write(json.dumps(content))
            wf.close()
        
        newKeybinds[kb[0]] = nkb


    Game.keybinds = newKeybinds
    Game.resetKeys()
    Game.select("settings")
    return

def load() -> None:
    backButton = Button((600, 100), (180, 60))
    backButton.text = "Retour"
    backButton.onPressed = backFunction
    interface.append(backButton)

    keybindsFiles = [path.join("data/settings", f) for f in listdir("data/settings") if path.isfile(path.join("data/settings", f))]
    for i, keybindFile in enumerate(keybindsFiles):
        keybinds = {}
        with open(keybindFile, "r", encoding="utf-8") as f:
            keybinds = json.load(f)
            f.close()
        title = Text(keybindFile.split("\\")[1][:-5], (200, 100 * ((i * 8) + 1)), color=(255, 255, 255))
        title.font = getFont("Black", 24)
        title.scrollable = True
        interface.append(title)
        for j, k in enumerate(keybinds):
            keybind = keybinds[k]
            kb = KeyBind(keybind["code"], keybind["key"], (400, 100 * (j + (i * 8) + 1) + 60))
            kb.kb = (k, keybind)
            kb.file = keybindFile
            kb.scrollable = True
            text = Text(keybind["name"], (100, 100 * (j + (i * 8) + 1) + 70), color=(255, 255, 255))
            text.scrollable = True
            interface.append(kb)
            interface.append(text)
    return

def draw(screen) -> None:
    screen.fill((0, 0 ,0))
    for element in interface:
        element.draw()
    return

def update() -> None:
    return