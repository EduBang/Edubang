from json import dumps
from json import load as loadJson

from eventListen import Events
import pygame as pg

from main import Game
from shared.utils.utils import Button, DataKeeper, SlideBar, Text, l

dk = DataKeeper()

interface: list = []

def saveSettings() -> None:
    settings = {}
    with open("data/settings.json", "w", encoding="utf-8") as f:
        for element in interface:
            if not hasattr(element, "setting"):
                continue
            settings[getattr(element, "setting")] = int(element.value)
        f.write(dumps(settings))
        f.close()
    Game.settings = settings
    pg.mixer.music.set_volume(settings["volume"] / 100)
    Game.resetKeys()
    return

def goKeybind() -> None:
    saveSettings()
    Game.reset()
    Game.select("keybind")
    return

def goLanguage() -> None:
    saveSettings()
    Game.reset()
    Game.select("language")
    return

@Events.observe
def window(w) -> None:
    if w != "settings": return
    interface.clear()
    return

def backFunction() -> None:
    saveSettings()
    Game.select("menu")
    return

def load() -> None:
    backButton = Button((100, 200), (180, 60))
    backButton.text = l("back")
    backButton.onPressed = backFunction
    interface.append(backButton)

    keybindButton = Button((100, 300), (180, 60))
    keybindButton.text = l("keybind")
    keybindButton.onPressed = goKeybind
    interface.append(keybindButton)

    languageButton = Button((100, 400), (180, 60))
    languageButton.text = l("language")
    languageButton.onPressed = goLanguage
    interface.append(languageButton)

    with open("data/settings.json", "r", encoding="utf-8") as f:
        dk.settings = loadJson(f)
        f.close()

    for i, setting in enumerate(dk.settings):
        sb = SlideBar((500, 100 * (i + 1) + 120))
        sb.setting = setting
        sb.value = int(dk.settings[setting])
        text = Text(setting, (400, 100 * (i + 1) + 110), color=(255, 255, 255))
        interface.append(sb)
        interface.append(text)
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))
    surface = Game.title.render(l("title"), False, (255, 255, 255))
    screen.blit(surface, (100, 100))

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
