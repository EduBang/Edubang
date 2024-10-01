import pygame as pg

running = True

resolution = (1000, 1000)
screen = pg.display.set_mode(resolution)
black = (0, 0, 0)

class game:

    def draw_screen():
        screen.fill(black)
        pg.display.update()

    def quit_algo():
        pg.quit()
        quit()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False




    game.draw_screen()

game.quit_algo()
