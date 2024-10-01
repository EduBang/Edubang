import pygame as pg

running = True

resolution = (0, 0)
screen = pg.display.set_mode(resolution, pg.FULLSCREEN)
w,h = pg.display.get_window_size()
black = (0, 0, 0)

class game:

    def draw_screen():
        pg.display.update()

    def quit_algo():
        pg.quit()
        quit()
        
    def vector(start_pos, end_pos, width = 5):
        
        pg.draw.line(screen, (0,255,0), start_pos, end_pos, width)
        pg.draw.polygon(screen, (0,255,0), ((end_pos)) )
        

while running:
    
    for event in pg.event.get():
        
        pg.draw.circle(screen, (255,0,0), (w / 2, h / 2), 30, 0)
        game.vector((10, 10), (20, 20), 1)
        
        if event.type == pg.QUIT:
            running = False
            
        
            
        

    game.draw_screen()
    
    

game.quit_algo()
