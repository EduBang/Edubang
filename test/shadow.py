# Projet : EduBang
# Auteurs : Anaël Chevillard, Sacha Fréguin, Néji Lim

import pygame as pg
from PIL import Image, ImageDraw
from math import *
# Initialisation de Pygame
# Initialisation de Pygame
pg.init()




def mirror_image(image, flip_x=True, flip_y=False):
    """
    Applique un effet miroir sur une image.

    :param image: Surface pygame à inverser
    :param flip_x: Miroir horizontal si True
    :param flip_y: Miroir vertical si True
    :return: Nouvelle image avec l'effet miroir appliqué
    """
    return pg.transform.flip(image, flip_x, flip_y)

# Définir les dimensions de la fenêtre
largeur, hauteur = 1000, 1000
screen = pg.display.set_mode((largeur, hauteur))
surface_opp = pg.Surface((400,400), pg.SRCALPHA)
# Définir les dimensions de l'image
largeur_image, hauteur_image = 400, 400
image = Image.new("RGBA", (largeur_image, hauteur_image), (255, 255, 255, 0))

# Placer des pixels sur l'image
center_point = (200, 200)  # Ajuster le centre du cercle
opacite = 0
opp = 0
draw = ImageDraw.Draw(image)
for x in range(largeur_image // 2 + 65):
    for y in range(hauteur_image):

        draw.point((x + 135, y), fill=(0, 0, 0, int(opp)))
        opp += 0.01

for x in range(largeur_image // 2 - 65):
    for y in range(hauteur_image):
        draw.point((x, y), fill=(0, 0, 0, 0))

for x in range(largeur_image):
    for y in range(hauteur_image):
        if sqrt((center_point[0] - x) ** 2 + (center_point[1] - y) ** 2) > 200:
            draw.point((x, y), fill=(0, 0, 0, 0))



       
image.show()
image.save("data/images/test.png")

# Dessiner un cercle sur l'image


# Convertir l'image PIL en surface Pygame
mode = image.mode
size = image.size
data = image.tobytes()
image_pg = pg.image.fromstring(data, size, mode)


# Définir la couleur de fond
couleur_fond = (255, 255, 255)  # Blanc
# Boucle de jeu
en_cours = True
while en_cours:
    for evenement in pg.event.get():
        if evenement.type == pg.QUIT:
            en_cours = False
        elif evenement.type == pg.KEYDOWN:
            if evenement.key == pg.K_a:
                opacite = max(0, opacite - 10)  # Diminuer l'opacité
            elif evenement.key == pg.K_e:
                opacite = min(255, opacite + 10)  # Augmenter l'opacité

    # Redessiner la surface_opp avec la nouvelle opacité
    surface_opp.fill((0, 0, 0, 0))  # Effacer la surface
    pg.draw.circle(surface_opp, (0, 0, 0, opacite), (200, 200), 200)

    # Afficher l'image sur la fenêtre
    screen.fill(couleur_fond)
    screen.blit(image_pg, (400, 400))
    screen.blit(surface_opp, (400, 400))
    pg.display.flip()

pg.quit()