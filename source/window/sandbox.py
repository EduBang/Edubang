from main import Game
from utils import updateCorps, process_collide, Captors, Corps

# simulation d'un petit corps léger qui entre en collision sur un gros et lourd
# a = Corps(6e10, 10, (100, 500), red, 0, 0)
# b = Corps(6e12, 100, (600, 500), blue, 0, 0)
# space.append(a)
# space.append(b)

# simulation du système solaire
# soleil = Corps(1.9885e14, 700, (0, 0), (255, 255, 0), 0, 0)
# mercure = Corps(3.3011e7, 38, (5800, 0), (127, 127, 127), 0, -0.52)
# venus = Corps(4.8675e8, 95, (10800, 0), (255, 127, 127), 0, -0.38)
# terre = Corps(5.9736e8, 100, (15000, 0), (0, 0, 255), 0, -0.32)
# mars = Corps(6.4185e7, 53, (22000, 0), (255, 50, 50), 0, -0.27)
# jupiter = Corps(1.8986e11, 300, (77800, 0), (255, 255, 230), 0, -0.143)
# saturne = Corps(5.6846e10, 260, (142670, 0), (255, 240, 240), 0, -0.105)
# uranus = Corps(8.681e9, 200, (287070, 0), (100, 100, 200), 0, -0.074)
# neptune = Corps(1.0243e10, 190, (449840, 0), (100, 100, 255), 0, -0.058)
# space.append(soleil)
# space.append(mercure)
# space.append(venus)
# space.append(terre)
# space.append(mars)
# space.append(jupiter)
# space.append(saturne)
# space.append(uranus)
# space.append(neptune)

def load(*args, **kwargs):
    Game.Camera.active = True
    # simulation de la terre et mars
    terre = Corps(6e12, 50, (100, 500), (255, 0, 0), 0, 0.1)
    mars = Corps(6e12, 50, (600, 500), (0, 0, 255), 0, 0)
    Game.space.append(terre)
    Game.space.append(mars)
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
    return