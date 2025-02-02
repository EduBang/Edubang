# Projet : EduBang
# Auteurs : Anaël Chevillard, Sacha Fréguin, Néji Lim

from os import listdir, path

from eventListen import Events

from main import Game, l, p
from shared.utils.utils import Button, DataKeeper, Language, Button

dk = DataKeeper()
dk.back = None

interface: list = []

@Events.observe
def window(w: str) -> None:
    if w != "language": return
    interface.clear()
    return

@Events.observe
def lang(lang: str) -> None:
    dk.back.text = l("back")
    return

def backFunction() -> None:
    Game.select("settings")
    return

def load() -> None:
    backButton = Button((100, 200), (180, 60))
    backButton.text = l("back")
    backButton.onPressed = backFunction
    dk.back = backButton
    interface.append(backButton)

    languages = [path.join(p("data/language"), f) for f in listdir(p("data/language")) if path.isfile(path.join(p("data/language"), f))]
    for i, language in enumerate(languages):
        lang = Language(language, (400, 70 * i + 100))
        interface.append(lang)
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
