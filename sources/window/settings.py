import json

from eventListen import Events
import pygame as pg

from main import Game
from shared.utils.utils import Button, DataKeeper, SlideBar, Text

dk = DataKeeper()

interface = []

def goKeybind() -> None:
    Game.reset()
    Game.select("keybind")
    return

@Events.observe
def window(w) -> None:
    interface.clear()
    return

def backFunction() -> None:
    settings = {}
    with open("data/settings.json", "w", encoding="utf-8") as f:
        for element in interface:
            if not hasattr(element, "setting"):
                continue
            settings[getattr(element, "setting")] = int(element.value)
        f.write(json.dumps(settings))
        f.close()
    Game.settings = settings
    pg.mixer.music.set_volume(settings["volume"] / 100)
    Game.resetKeys()
    Game.select("menu")
    return

def load() -> None:
    backButton = Button((100, 100), (180, 60))
    backButton.scrollable = True
    backButton.text = "Retour"
    backButton.onPressed = backFunction
    interface.append(backButton)

    keybindButton = Button((100, 200), (180, 60))
    keybindButton.text = "Contrôles"
    keybindButton.onPressed = goKeybind
    interface.append(keybindButton)

    with open("data/settings.json", "r", encoding="utf-8") as f:
        dk.settings = json.load(f)
        f.close()

    for i, setting in enumerate(dk.settings):
        sb = SlideBar((250, 200 * (i + 1) + 125))
        sb.setting = setting
        sb.value = int(dk.settings[setting])
        sb.scrollable = True
        text = Text(setting, (100, 200 * (i + 1) + 110), color=(255, 255, 255))
        text.scrollable = True
        interface.append(sb)
        interface.append(text)
    return

def draw(screen) -> None:
    screen.fill((0, 0 ,0))
    for element in interface:
        element.draw()
    return

def update() -> None:
    for element in interface:
        setting = getattr(element, 'setting', None)
        if not setting: continue
        if setting == "volume":
            pg.mixer.music.set_volume(element.value / 100)
    return