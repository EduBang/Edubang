# Projet : EduBang
# Auteurs : Anaël Chevillard, Sacha Fréguin, Néji Lim

from math import pi, sqrt

from proto import proto
import pygame as pg

def lorentzFactor(v: float | int) -> float:
    """
    Calcule de facteur de Lorentz

    Arguments:
        v (float | int): La vitesse de l'objet
    
    Retourne:
        float: Le facteur de Lorentz
    """
    return 1 / sqrt(1 - (v ** 2 / 0x13F4D4EACDD7564))

with proto("Corps") as Corps:
    @Corps
    def new(self, mass: int | float, radius: int, pos: tuple[int, int], color: tuple[int, int, int], v_initial: tuple[float, float]) -> None:
        """
        L'initiateur du corps
        
        Arguments:
            mass (int | float): La masse de l'astre en kg
            radius (int): Le rayon de l'astre en km
            pos (tuple[int, int]): La position de l'astre dans l'espace
            color (tuple[int, int, int]): La couleur de l'astre
            v_initial (tuple[int, int]): La vitesse initiale de l'astre

        Retourne:
            None
        """
        self.mass = mass # kilogramme
        self.radius = radius # kilomètre
        self.pos = pos
        self.color = color
        self.velocity = list(v_initial)  # Vitesse initiale
        self.path = []
        return
    
    @Corps
    def draw(self, screen, camera) -> None:
        """
        Fonction qui dessine l'astre
        
        Arguments:
            screen (pg.Surface): L'écran PyGame
            camera (Camera): La caméra
            
        Retourne:
            None
        """
        x: float = (self.pos[0] * camera.zoom) + camera.x
        y: float = (self.pos[1] * camera.zoom) + camera.y
        if pi * (self.radius * camera.zoom) ** 2 < 10: # Si le corps est trop petit sur l'écran, alors il va l'afficher avec une croix
            pg.draw.line(screen, (255, 255, 255), (x - 8, y), (x + 8, y), 2)
            pg.draw.line(screen, (255, 255, 255), (x, y - 8), (x, y + 8), 2)
        else:
            if -1e2 < x < 1e4 and -1e2 < y < 1e4:
                pg.draw.circle(screen, self.color, (x, y), self.radius * camera.zoom)
        return
    
    @Corps
    def update_position(self, acc: tuple[float, float], dt: float) -> None:
        """
        Fonction qui met é jour la position de l'astre selon l'accélération et du temps
        
        Arguments:
            acc (tuple[float, float]): L'accélération
            dt (float): Le temps
        
        Retourne:
            None
        """
        # Mise à jour de la vitesse (conserve l'inertie)
        gamma: float = lorentzFactor(sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2))

        # selon prgm, acc en km/s
        self.velocity[0] += acc[0] * dt / gamma
        self.velocity[1] += acc[1] * dt / gamma

        # Mise à jour de la position en fonction de la nouvelle vitesse (avec inertie)
        self.pos = (
            self.pos[0] + self.velocity[0] * dt,
            self.pos[1] + self.velocity[1] * dt
        )

        self.path.append(self.pos) # Laisser ce code ira consommer environ 4Mo de RAM par seconde pour 10 corps.
        if len(self.path) > 499: # On limite alors la liste du chemin à 500. C'est ajustable.
            self.path.pop(0)
        return
