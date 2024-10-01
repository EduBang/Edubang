import pygame as pg
import math

running = True

resolution = (1000, 800)
screen = pg.display.set_mode(resolution)
w,h = pg.display.get_window_size()
black = (0, 0, 0)

pg.display.set_caption('EduBang')
icon = pg.image.load('icon.png')
pg.display.set_icon(icon)

class game:

    def draw_screen():
        pg.display.update()

    def quit_algo():
        pg.quit()
        quit()
        
    def vector(start_pos, end_pos, width = 5):
        length_vector = math.sqrt(((end_pos[0] - start_pos[0]) ** 2 ) + ((end_pos[1] - start_pos[1]) ** 2))

        
        pg.draw.line(screen, (0,255,0), start_pos, end_pos, width)
    
    
        

while running:
    
    for event in pg.event.get():
        
        pg.draw.circle(screen, (255,0,0), (w / 2, h / 2), 30, 0)
        game.vector((200, 200), (200, 150), 1)
        
        if event.type == pg.QUIT:
            running = False
            
        
            
        

    game.draw_screen()
    
    

game.quit_algo()
