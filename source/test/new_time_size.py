import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Échelle de temps avec Pygame")

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Facteur de vitesse (time scale)
time_scale = 1.0

# Position et vitesse initiale d'un objet
x_position = 100
y_position = HEIGHT // 2
speed = 200  # Vitesse en pixels par seconde

# Boucle principale du jeu
clock = pygame.time.Clock()
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Ajustement de l'échelle de temps avec les touches haut et bas
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                time_scale += 0.1  # Augmenter l'échelle de temps
            elif event.key == pygame.K_DOWN:
                time_scale = max(0.1, time_scale - 0.1)  # Diminuer l'échelle de temps

    # Calcul du temps écoulé (delta time) ajusté avec l'échelle de temps
    delta_time = clock.tick(60) / 1000.0  # Temps en secondes entre chaque image
    delta_time *= time_scale  # Appliquer l'échelle de temps

    # Mise à jour de la position de l'objet
    x_position += speed * delta_time
    if x_position > WIDTH:  # Remettre l'objet au début s'il sort de l'écran
        x_position = 0

    # Effacer l'écran et dessiner l'objet
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (int(x_position), y_position), 20)

    # Afficher l'échelle de temps actuelle
    font = pygame.font.Font(None, 36)
    text = font.render(f'Échelle de temps : {time_scale:.1f}', True, (0, 0, 0))
    screen.blit(text, (10, 10))

    # Rafraîchir l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
