import json

from main import Game
from shared.utils.utils import Button, DataKeeper, KeyBind, Text

from eventListen import Events

dk = DataKeeper()

interface = []

@Events.observe
def window(w):
    for i in interface:
        interface.remove(i)

def backFunction():
    newKeybinds = {}
    with open("source/data/keybind.json", "w", encoding="utf-8") as f:
        for keybind in interface:
            if not hasattr(keybind, "kb"):
                continue
            newKeybinds[getattr(keybind, "kb")] = keybind.key
        f.write(json.dumps(newKeybinds))
        f.close()
    Game.keybinds = newKeybinds
    Game.resetKeys()
    Game.select("menu")

def load() -> None:
    backButton = Button((100, 100), (180, 60))
    backButton.text = "Back to menu"
    backButton.onPressed = backFunction
    interface.append(backButton)

    with open("source/data/keybind.json", "r", encoding="utf-8") as f:
        dk.keybinds = json.load(f)
        f.close()

    for i, kb in enumerate(dk.keybinds):
        keybind = KeyBind(dk.keybinds[kb], (250, 100 * (i + 1) + 100))
        keybind.kb = kb
        text = Text(kb, (100, 100 * (i + 1) + 110), color=(255, 255, 255))
        interface.append(keybind)
        interface.append(text)
    return

def draw(screen) -> None:
    screen.fill((0, 0 ,0))
    for element in interface:
        element.draw(screen)
    return

def update() -> None:
    return