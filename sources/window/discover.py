from json import load as loadJson

from main import Game

def load() -> None:
    return

def draw(screen) -> None:
    screen.fill((0, 0 ,0))

    surface = Game.title.render("Découvrir", False, (255, 255, 255))
    screen.blit(surface, (100, 100))
    
    return

def update() -> None:
    return