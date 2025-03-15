# Projet : EduBang
# Auteurs : Anaël Pernot-Chevillard, Sacha Fréguin, Néji Lim

from json import load as loadJson
from json.decoder import JSONDecodeError
from os import listdir, path
try:
    from tkinter import Tk, filedialog
except ModuleNotFoundError as e:
    print("> Impossible d'importer le module tkinter : %s" % e)
    Tk = filedialog = None

from eventListen import Events

from main import Game, l, p
from shared.utils.utils import DataKeeper, System, Button

dk = DataKeeper()
dk.tmessage = None
interface: list = []

@Events.observe
def window(w) -> None:
    if w != "discover": return
    interface.clear()
    return

def addSystem() -> None:
    root = Tk()
    root.withdraw()
    file: str = filedialog.askopenfilename(filetypes=[("EduBang System", "*.ebs"), ("All files", "*.*")])
    if not file: return
    system = None
    try:
        s = {}
        with open(file, "r", encoding="utf-8") as f:
            s = loadJson(f)
            f.close()
        system = System(s, len(interface) - 2)
        system.draw()
    except Exception as e:
        if isinstance(e, UnicodeDecodeError):
            dk.tmessage = [10, l("err1")]
        elif isinstance(e, JSONDecodeError):
            dk.tmessage = [10, l("err2")]
            system.destroy()
        else:
            dk.tmessage = [10, l("err3")]
            system.destroy()
    if getattr(system, "system", None):
        interface.append(system)
    root.destroy()
    return

def backFunction() -> None:
    Game.select("menu")
    return

def load() -> None:
    backButton = Button((100, 200), (180, 60))
    backButton.text = l("back")
    backButton.onPressed = backFunction
    interface.append(backButton)

    if Tk and filedialog:
        addSystemButton = Button((100, 300), (180, 60))
        addSystemButton.text = l("addSystem")
        addSystemButton.onPressed = addSystem
        interface.append(addSystemButton)

    systemsFile = [path.join(p("data/systems"), f) for f in listdir(p("data/systems")) if path.isfile(path.join(p("data/systems"), f))]
    for i, systemFile in enumerate(systemsFile):
        s = {}
        with open(systemFile, "r", encoding="utf-8") as f:
            s = loadJson(f)
            f.close()
        system = System(s, i)
        interface.append(system)
    return

def draw(screen) -> None:
    screen.fill((0, 0, 0))

    surface = Game.title.render(l("title"), False, (255, 255, 255))
    screen.blit(surface, (100, 100))

    for element in interface:
        element.draw()

    if dk.tmessage:
        dk.tmessage[0] -= (Game.deltaTime * 2.195)
        width, height = Game.screenSize
        text: str = dk.tmessage[1]
        surface = Game.italic.render(text, False, (255, 0, 0))
        surface.set_alpha(int(255 * dk.tmessage[0] / 5))
        tW, tH = Game.italic.size(text)
        screen.blit(surface, (width // 2 - tW // 2, height // 2 - tH // 2 + 300))
        if dk.tmessage[0] <= 0:
            dk.tmessage = None

    return

def update() -> None:
    return
