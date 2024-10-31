import pygame as pg
from math import *
from proto import proto
from statistics import *


from components.Vectors import *
from components.Corps import *
from components.Physics import *
from components.Captors import *

pg.init()

# Initialisation
pg.display.set_caption('EduBang')
icon = pg.image.load('source/Images/icon.png')
pg.display.set_icon(icon)
running = True
resolution = (1200, 1000)
screen = pg.display.set_mode(resolution)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
dt = 1 # Pas de temps (ajustable)


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
            pg.draw.circle(screen, color, (float(pos[0]), float(pos[1])), 1)

listCorps = []

# simulation de la terre et mars
terre = Corps(6e12, 50, (100, 500), red, 0, 0.1)
mars = Corps(6e12, 50, (600, 500), blue, 0, 0)
listCorps.append(terre)
listCorps.append(mars)

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
        corps.draw(screen)
        # Path.draw_corps_path(corps.path, corps.color)
    
    # Mettre à jour l'écran
    Game.draw_screen()
    clock.tick(60)  # Limite à 60 FPS

Game.quit_algo()