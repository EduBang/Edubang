import pygame as pg
from math import *
from proto import proto
from eventListen import Events
from statistics import *


from components.Vectors import *
from components.Corps import *
from components.Physics import *
from components.Captors import *

pg.init()

# Initialisation
pg.display.set_caption("EduBang")
icon = pg.image.load("source/Images/icon.png")
pg.display.set_icon(icon)
running = True
resolution = (1200, 1000)
screen = pg.display.set_mode(resolution)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
dt = 1 # Pas de temps (ajustable)
events = Events()


with proto("Game") as Game:
    @Game
    def draw_screen(self):
        pg.display.update()

    @Game
    def quit_algo(self):
        pg.quit()
        quit()

#class trajectoire
with proto("Path") as Path:
    # dessiner trajectoire terre
    @Path
    def draw_corps_path(self, path, color):
        for pos in path:
            x = float((pos[0] + Camera.x / Camera.zoom) * Camera.zoom)
            y = float((pos[1] + Camera.y / Camera.zoom) * Camera.zoom)
            pg.draw.circle(screen, color, (x, y), 1000 * Camera.zoom)

with proto("CameraHandler") as CameraHandler:
    @CameraHandler
    def new(self):
        self.x = 0
        self.y = 0
        self.speed = 5
        self.zoom = 1
        self.maxZoom = 100
        self.minZoom = 0.001
        self.offset = [0, 0]
        self.focus = None
        return

Camera = CameraHandler()
listCorps = []

# simulation de la terre et mars
# terre = Corps(6e12, 50, (100, 500), red, 0, 0.1)
# mars = Corps(6e12, 50, (600, 500), blue, 0, 0)
# listCorps.append(terre)
# listCorps.append(mars)

# simulation de x corps aléatoires
# from random import randint
# x = 10
# for i in range(x):
#     a = Corps(randint(5 * 10 ** 9, 20 * 10 ** 9),
#               randint(10, 50),
#               (randint(10, 1000), randint(10, 1000)),
#               (randint(0, 255), randint(0, 255), randint(0, 255)),
#               randint(-100, 100) / 10000, randint(-100, 100) / 10000
#               )
#     listCorps.append(a)

# simulation d'un petit corps léger qui entre en collision sur un gros et lourd
# a = Corps(6e10, 10, (100, 500), red, 0, 0)
# b = Corps(6e12, 100, (600, 500), blue, 0, 0)
# listCorps.append(a)
# listCorps.append(b)

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
# listCorps.append(soleil)
# listCorps.append(mercure)
# listCorps.append(venus)
# listCorps.append(terre)
# listCorps.append(mars)
# listCorps.append(jupiter)
# listCorps.append(saturne)
# listCorps.append(uranus)
# listCorps.append(neptune)

keys = {
    pg.K_z: False,
    pg.K_q: False,
    pg.K_s: False,
    pg.K_d: False,
    pg.K_UP: False,
    pg.K_LEFT: False,
    pg.K_DOWN: False,
    pg.K_RIGHT: False
}

@events.observe
def keydown(key: int) -> None:
    if key in keys:
        keys[key] = True
    return

@events.observe
def keyup(key: int) -> None:
    if key in keys:
        keys[key] = False
    return

@events.observe
def mousewheel(x: int, y: int) -> None:
    if y == 1 and Camera.zoom < Camera.maxZoom: # scroll vers le haut: zoom
        Camera.zoom *= 1.1
    if y == -1 and Camera.zoom > Camera.minZoom: # scroll vers le bas: dézoom
        Camera.zoom /= 1.1
    return

@events.observe
def mousebuttondown(position: tuple[int, int], button: int) -> None:
    for corps in listCorps:
        x = float((corps.pos[0] + Camera.x / Camera.zoom) * Camera.zoom)
        y = float((corps.pos[1] + Camera.y / Camera.zoom) * Camera.zoom)
        sqx = (position[0] - x) ** 2
        sqy = (position[1] - y) ** 2
        if sqrt(sqx + sqy) < corps.radius * Camera.zoom:
            Camera.focus = corps
            break
    else:
        Camera.focus = None
    return


# Fonction permettant de mélanger les couleurs de 2 corps selon la surface
def mergeColor(a, b) -> tuple[int, int, int]:
    # C'est un calcul de moyenne pondérée
    surfaceA = pi * a.radius ** 2
    surfaceB = pi * b.radius ** 2
    red = (surfaceA * a.color[0] + surfaceB * b.color[0]) / (surfaceA + surfaceB)
    green = (surfaceA * a.color[1] + surfaceB * b.color[1]) / (surfaceA + surfaceB)
    blue = (surfaceA * a.color[2] + surfaceB * b.color[2]) / (surfaceA + surfaceB)
    return (red, green, blue)


def process_collide(corps1, corps2):
    cinetic_energy_corps1 = Physics.get_cinetic_energy(corps1.mass, Physics.get_velocity(corps1.path[-2], corps1.path[-1], dt))
    cinetic_energy_corps2 = Physics.get_cinetic_energy(corps2.mass, Physics.get_velocity(corps2.path[-2], corps2.path[-1], dt))
    unit_vector_mouv_corps1 = Vectors.get_unit_vector_mouv(corps1.path[-2], corps1.path[-1])
    unit_vector_mouv_corps2 = Vectors.get_unit_vector_mouv(corps2.path[-2], corps2.path[-1])
    
    cinetic_energy_vector_corps1 = cinetic_energy_corps1 * unit_vector_mouv_corps1[0], cinetic_energy_corps1 * unit_vector_mouv_corps1[1]
    cinetic_energy_vector_corps2 = cinetic_energy_corps2 * unit_vector_mouv_corps2[0], cinetic_energy_corps2 * unit_vector_mouv_corps2[1]
    
    sum_vector_cinetic_energy_corps1 = (cinetic_energy_vector_corps1[0] / corps1.mass, cinetic_energy_vector_corps1[1] / corps1.mass)
    sum_vector_cinetic_energy_corps2 = (cinetic_energy_vector_corps2[0] / corps2.mass, cinetic_energy_vector_corps2[1] / corps2.mass)

    mass = corps1.mass + corps2.mass
    radius = sqrt(((pi * corps1.radius ** 2) + (pi * corps2.radius ** 2)) / pi)
    color = mergeColor(corps1,corps2)
    vInitialX = (corps1.mass * sum_vector_cinetic_energy_corps1[0] + corps2.mass * sum_vector_cinetic_energy_corps2[0]) / mass
    vInitialY = (corps1.mass * sum_vector_cinetic_energy_corps1[1] + corps2.mass * sum_vector_cinetic_energy_corps2[1]) / mass

    corps = corps1
    hasChanged = False
    if corps2.radius > corps1.radius:
        corps = corps2
        hasChanged = True
    corps.mass = mass
    corps.radius = radius
    corps.color = color
    corps.velocity = [vInitialX, vInitialY]
    corps.path = []
    if Camera.focus in [corps1, corps2]:
        Camera.focus = corps
    return corps1 if hasChanged else corps2

collision_occurred = False
fusion = None

# Fonction permettant de mettre à jour la postion entre 2 corps.
def updateCorps(a, b) -> float:
    distance = Vectors.get_distance(a, b)
    attraction = Physics.get_attraction(a.mass, b.mass, distance)
    unitVectorA = Vectors.get_unit_vector(a.pos, b.pos)
    unitVectorB = Vectors.get_unit_vector(b.pos, a.pos)
    accA = [unitVectorA[0] * attraction / a.mass, unitVectorA[1] * attraction / a.mass]
    accB = [unitVectorB[0] * attraction / b.mass, unitVectorB[1] * attraction / b.mass]

    a.update_position(accA, dt)
    b.update_position(accB, dt)
    return distance

# Boucle principale
clock = pg.time.Clock()
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            events.trigger("keydown", event.key)
        if event.type == pg.KEYUP:
            events.trigger("keyup", event.key)
        if event.type == pg.MOUSEWHEEL:
            events.trigger("mousewheel", event.x, event.y)
        if event.type == pg.MOUSEBUTTONDOWN:
            events.trigger("mousebuttondown", event.pos, event.button)
    
    if keys[pg.K_z] or keys[pg.K_UP]: # faire monter la caméra
        Camera.y += Camera.speed
    if keys[pg.K_q] or keys[pg.K_LEFT]: # faire aller la caméra à gauche
        Camera.x += Camera.speed
    if keys[pg.K_s] or keys[pg.K_DOWN]: # faire descendre la caméra
        Camera.y -= Camera.speed
    if keys[pg.K_d] or keys[pg.K_RIGHT]: # faire aller la caméra à droite
        Camera.x -= Camera.speed

    if Camera.focus is not None:
        midScreenX = screen.get_width() // 2
        midScreenY = screen.get_height() // 2
        Camera.x = -Camera.focus.pos[0] + midScreenX
        Camera.y = -Camera.focus.pos[1] + midScreenY

    screen.fill(black)

    for corps in listCorps:
        for otherCorps in listCorps:
            if corps == otherCorps: # si le corps est égale à l'autre corps
                continue # on l'oublie

            distance = updateCorps(corps, otherCorps)
            # Vérification de la collision
            if Captors.collide(corps, otherCorps, distance):
                removedCorps = process_collide(corps, otherCorps)
                listCorps.remove(removedCorps)
        
        corps.update_position([0, 0], dt)
        corps.draw(screen, Camera)
    
    # Mettre à jour l'écran
    Game.draw_screen()
    clock.tick(60)  # Limite à 60 FPS

Game.quit_algo()