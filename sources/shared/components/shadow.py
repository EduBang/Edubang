import pygame as pg
from PIL import Image, ImageDraw
from math import *
# Initialisation de Pygame
# Initialisation de Pygame
pg.init()

# Définir les dimensions de la fenêtre
largeur, hauteur = 1000, 1000
fenetre = pg.display.set_mode((largeur, hauteur))

# Définir les dimensions de l'image
largeur_image, hauteur_image = 400, 400
image = Image.new("RGBA", (largeur_image, hauteur_image), (255, 255, 255, 0))

# Placer des pixels sur l'image
center_point = (200, 200)  # Ajuster le centre du cercle
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



       
# image.show()
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

    # Afficher l'image sur la fenêtre
    fenetre.fill(couleur_fond)
    fenetre.blit(image_pg, (400, 400))
    pg.display.flip()

pg.quit()