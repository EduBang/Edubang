from json import load as loadJson
from os import listdir, path

from eventListen import Events

from main import Game
from shared.utils.utils import DataKeeper, System, Button

dk = DataKeeper()
interface: list = []

@Events.observe
def window(w) -> None:
    if w != "discover": return
    interface.clear()
    return

def backFunction() -> None:
    Game.select("menu")
    return

def load() -> None:
    backButton = Button((100, 200), (180, 60))
    backButton.text = "Retour"
    backButton.onPressed = backFunction
    interface.append(backButton)

    systemsFile = [path.join("data/systems", f) for f in listdir("data/systems") if path.isfile(path.join("data/systems", f))]
    for i, systemFile in enumerate(systemsFile):
        s = {}
        with open(systemFile, "r", encoding="utf-8") as f:
            s = loadJson(f)
            f.close()
        system = System(s, i)
        interface.append(system)
    return

def draw(screen) -> None:
    screen.fill((0, 0 ,0))

    surface = Game.title.render("Découvrir", False, (255, 255, 255))
    screen.blit(surface, (100, 100))

    for element in interface:
        element.draw()

    return

def update() -> None:
    return