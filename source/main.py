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
pi = 3.1416
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
            pg.draw.circle(screen,  color, (float(pos[0]), float(pos[1])), 2)

terre = Corps(6e12, 50, (100, 500), red, 0, 0.1)
mars = Corps(6e12, 50, (600, 500), blue, 0, 0)


def couleur_moyenne(corps1, corps2):
    new_color = ((corps1.color[0] + corps2.color[0]) / 2, (corps1.color[1] + corps2.color[1]) / 2, (corps1.color[2] + corps2.color[2]) / 2)
    return new_color
    


def process_collide(corps1, corps2):
    cinetic_energy_corps1 = Physics.get_cinetic_energy(corps1.mass, Physics.get_velocity(corps1.path[-2], corps1.path[-1], dt))
    cinetic_energy_corps2 = Physics.get_cinetic_energy(corps2.mass, Physics.get_velocity(corps2.path[-2], corps2.path[-1], dt))
    unit_vector_mouv_corps1 = Vectors.get_unit_vector_mouv(corps1.path[-2], corps1.path[-1])
    unit_vector_mouv_corps2 = Vectors.get_unit_vector_mouv(corps2.path[-2], corps2.path[-1])
    
    cinetic_energy_vector_corps1 = cinetic_energy_corps1 * unit_vector_mouv_corps1[0], cinetic_energy_corps1 * unit_vector_mouv_corps1[1]
    cinetic_energy_vector_corps2 = cinetic_energy_corps2 * unit_vector_mouv_corps2[0], cinetic_energy_corps2 * unit_vector_mouv_corps2[1]
    
    sum_vector_cinetic_energy_corps1 = cinetic_energy_vector_corps1[0] / corps1.mass, cinetic_energy_vector_corps1[1] / corps1.mass
    sum_vector_cinetic_energy_corps2 = cinetic_energy_vector_corps2[0] / corps2.mass, cinetic_energy_vector_corps2[1] / corps2.mass
    
    
    fusion = Corps(corps1.mass + corps2.mass, sqrt(((pi * terre.radius ** 2) + (pi * mars.radius ** 2)) / pi),
                   ((terre.pos[0] + mars.pos[0]) / 2,(terre.pos[1] + mars.pos[1]) / 2), couleur_moyenne(terre,mars),
                   sum_vector_cinetic_energy_corps1[0] + sum_vector_cinetic_energy_corps2[0], sum_vector_cinetic_energy_corps1[1] + sum_vector_cinetic_energy_corps2[1])
    return fusion

collision_occurred = False
fusion = None

# Boucle principale
clock = pg.time.Clock()
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill(black)
    
    if not collision_occurred:
        # Calcul des forces et de l'accélération
        distance = Vectors.get_distance(terre, mars)
        
        attraction_terre = Physics.get_attraction(terre.mass, mars.mass, distance)
        attraction_mars = Physics.get_attraction(mars.mass, terre.mass, distance)
        
        unit_vector_terre = Vectors.get_unit_vector(terre.pos, mars.pos)
        unit_vector_mars = Vectors.get_unit_vector(mars.pos, terre.pos)
        
        # Calcul des accélérations pour la Terre et Mars
        acc_terre = [unit_vector_terre[0] * attraction_terre / terre.mass, unit_vector_terre[1] * attraction_terre / terre.mass]
        acc_mars = [unit_vector_mars[0] * attraction_mars / mars.mass, unit_vector_mars[1] * attraction_mars / mars.mass]

        # Mise à jour des positions
        mars.update_position(acc_mars, dt)
        terre.update_position(acc_terre, dt)
        
        # Vérification de la collision
        if Captors.collide(terre, mars, distance):
            print("Collision détectée")
            fusion = process_collide(terre, mars)
            collision_occurred = True  # Marquer que la collision a eu lieu
            
    # Dessiner les corps ou la fusion en fonction de l'état de collision
    if collision_occurred:
        fusion.draw(screen)
        Path.draw_corps_path(fusion.path, fusion.color)
        acc_fusion = [0, 0]  # Exemple sans force externe; ajouter des forces si nécessaire
        fusion.update_position(acc_fusion, dt)
    else:
        mars.draw(screen)
        terre.draw(screen)
        Path.draw_corps_path(terre.path, terre.color)
        Path.draw_corps_path(mars.path, mars.color)
    
    # Mettre à jour l'écran
    Game.draw_screen()
    clock.tick(60)  # Limite à 60 FPS

Game.quit_algo()