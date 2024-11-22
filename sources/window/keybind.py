import json

from eventListen import Events

from main import Game
from shared.utils.utils import Button, DataKeeper, KeyBind, Text

dk = DataKeeper()

interface = []

@Events.observe
def window(w) -> None:
    interface.clear()
    return

def backFunction() -> None:
    newKeybinds = {}
    with open("data/keybind.json", "w", encoding="utf-8") as f:
        for keybind in interface:
            if not hasattr(keybind, "kb"):
                continue
            newKeybinds[getattr(keybind, "kb")] = keybind.key
        f.write(json.dumps(newKeybinds))
        f.close()
    Game.keybinds = newKeybinds
    Game.resetKeys()
    Game.select("settings")
    return

def load() -> None:
    backButton = Button((100, 100), (180, 60))
    backButton.scrollable = True
    backButton.text = "Back to menu"
    backButton.onPressed = backFunction
    interface.append(backButton)

    with open("data/keybind.json", "r", encoding="utf-8") as f:
        dk.keybinds = json.load(f)
        f.close()

    for i, kb in enumerate(dk.keybinds):
        keybind = KeyBind(dk.keybinds[kb], (250, 100 * (i + 1) + 100))
        keybind.kb = kb
        keybind.scrollable = True
        text = Text(kb, (100, 100 * (i + 1) + 110), color=(255, 255, 255))
        text.scrollable = True
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