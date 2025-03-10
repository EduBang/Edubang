# Projet : EduBang
# Auteurs : Anaël Chevillard, Sacha Fréguin, Néji Lim

from json import dumps
from json import load as loadJson

from eventListen import Events
import pygame as pg

from main import Game, l, p
from shared.utils.utils import Button, DataKeeper, SlideBar, Text

dk = DataKeeper()
dk.sb2s = False

interface: list = []

def saveSettings() -> None:
    settings = {}
    with open(p("data/settings.json"), "w", encoding="utf-8") as f:
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
    Game.select("keybind")
    return

def goLanguage() -> None:
    saveSettings()
    Game.select("language")
    return

@Events.observe
def window(w) -> None:
    if w != "settings": return
    interface.clear()
    return

@Events.observe
def SB2S() -> None:
    dk.sb2s = True
    return

def backFunction() -> None:
    saveSettings()
    page = "menu"
    if dk.sb2s:
        dk.sb2s = False
        page = "sandbox"
    Game.select(page)
    return

def load() -> None:
    backButton = Button((100, 200), (180, 60))
    backButton.text = l("back")
    backButton.onReleased = backFunction
    interface.append(backButton)

    keybindButton = Button((100, 300), (180, 60))
    keybindButton.text = l("keybind")
    keybindButton.onReleased = goKeybind
    interface.append(keybindButton)

    languageButton = Button((100, 400), (180, 60))
    languageButton.text = l("language")
    languageButton.onReleased = goLanguage
    interface.append(languageButton)

    with open(p("data/settings.json"), "r", encoding="utf-8") as f:
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
