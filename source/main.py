import pygame as pg
from math import *

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

class Game:

    def draw_screen():
        pg.display.update()


    def quit_algo():
        pg.quit()
        quit()

#class trajectoire
class Path:
    # dessiner trajectoire terre
    def draw_corps_path(path, color):
        for pos in path:
            pg.draw.circle(screen,  color, (float(pos[0]), float(pos[1])), 2)



class Vectors:#jsp

    def get_unit_vector(pos1, pos2):
        dif_x = pos2[0] - pos1[0]
        dif_y = pos2[1] - pos1[1]
        distance = sqrt(dif_x ** 2 + dif_y ** 2)
        
        if distance == 0:
            return (0, 0)
        
        x_v_unit = dif_x / distance
        y_v_unit = dif_y / distance
        return (x_v_unit, y_v_unit)


class Corps:
    def __init__(self, m, radius, pos, color, v_initial_x, v_initial_y):#c'est pas bon
        self.mass = m
        self.radius = radius
        self.pos = pos
        self.color = color
        self.velocity = [v_initial_x, v_initial_y]  # Vitesse initiale
        self.path = []


    def draw(self):#c'est bon
        pg.draw.circle(screen, self.color, (float(self.pos[0]), float(self.pos[1])), self.radius)

    def update_position(self, acc, dt):
        self.path.append(self.pos)
        # Mise à jour de la vitesse (conserve l'inertie)
        self.velocity[0] += acc[0] * dt
        self.velocity[1] += acc[1] * dt
        
        # Mise à jour de la position en fonction de la nouvelle vitesse (avec inertie)
        self.pos = (self.pos[0] + self.velocity[0] * dt, 
                    self.pos[1] + self.velocity[1] * dt)
      

class Physics:
    
    def get_distance(corps1, corps2):
        return sqrt(((corps1.pos[0] - corps2.pos[0]) ** 2) + ((corps1.pos[1] - corps2.pos[1]) ** 2))

    def get_attraction(mass1, mass2, d, radius):
        G = 6.67e-11
        

        if d == 0:
            return 0

            
        else :
            return G * ((mass1 * mass2) / (d ** 2))
        
    #def colision(corps1, corps2)


    

# Initialisation des planètes
terre = Corps(6e12, 50, (100, 500), red, 0.4, -0.4)
mars = Corps(6e12, 50, (600, 500), blue, -0.4,0.4)

# Boucle principale
clock = pg.time.Clock()
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill(black)
    
    # Calcul des forces et de l'accélération
    distance = Physics.get_distance(terre, mars)#c'est bon
    
    
    attraction_terre = Physics.get_attraction(terre.mass, mars.mass, distance, terre.radius)
    attraction_mars = Physics.get_attraction(mars.mass, terre.mass, distance, mars.radius)
    
    unit_vector_terre = Vectors.get_unit_vector(terre.pos, mars.pos)
    unit_vector_mars = Vectors.get_unit_vector(mars.pos, terre.pos)
    
    # Calcul des accélérations pour la Terre (inversement proportionnel à la masse)
    acc_terre = [unit_vector_terre[0] * attraction_terre / terre.mass, unit_vector_terre[1] * attraction_terre / terre.mass]
    acc_mars = [unit_vector_mars[0] * attraction_mars / mars.mass, unit_vector_mars[1] * attraction_mars / mars.mass]

    # Mise à jour des positions avec conservation de l'inertie
    dt = 15 # Pas de temps (ajustable)
    mars.update_position(acc_mars, dt)
    terre.update_position(acc_terre, dt)
    

    
    
    # Dessiner les corps
    mars.draw()
    terre.draw()
    Path.draw_corps_path(terre.path, terre.color)
    Path.draw_corps_path(mars.path, mars.color)
    
    # Mettre à jour l'écran
    Game.draw_screen()

    
    
    clock.tick(60)  # Limite à 60 FPS

Game.quit_algo()
