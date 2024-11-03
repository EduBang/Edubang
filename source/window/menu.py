from random import randint

from main import Game
from utils import updateCorps, process_collide, Captors, Button, Corps

def buttonOnPressed():
    Game.select("sandbox")

btn = Button((100, 100), (180, 60))
btn.text = "Play Sandbox"
btn.onPressed = buttonOnPressed


x = 10
for i in range(x):
    a = Corps(randint(5 * 10 ** 9, 20 * 10 ** 9),
            randint(10, 50),
            (randint(10, 1000), randint(10, 1000)),
            (randint(0, 255), randint(0, 255), randint(0, 255)),
            randint(-100, 100) / 10000, randint(-100, 100) / 10000
            )
    Game.space.append(a)

def load(*args, **kwargs):
    return

def draw(screen):
    screen.fill((0, 0 ,0))

    for corps in Game.space:
        for otherCorps in Game.space:
            if corps == otherCorps: # si le corps est égale à l'autre corps
                continue # on l'oublie

            distance = updateCorps(corps, otherCorps)
            # Vérification de la collision
            if Captors.collide(corps, otherCorps, distance):
                removedCorps = process_collide(corps, otherCorps)
                Game.space.remove(removedCorps)
        
        corps.update_position([0, 0], Game.dt)
        corps.draw(screen, Game.Camera)
        # Path.draw_corps_path(corps.path, corps.color)
    
    btn.draw(screen)
    
    return