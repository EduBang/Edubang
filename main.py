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
        high_triangle = length_vector / 8
        side_triangle = high_triangle / 2
        point_1 = (end_pos[0] - high_triangle, end_pos[1] - side_triangle)
        point_2 = (end_pos[0] + high_triangle, end_pos[1] - side_triangle)
        
        pg.draw.line(screen, (0,0,255), end_pos  ,(end_pos[0] - end_pos[0] / 8, end_pos[1] - end_pos[1] / 8),width)

        
        
        pg.draw.line(screen, (0,255,0), start_pos, end_pos, width)
    
        
        pg.draw.line(screen, (0,255,0), end_pos, point_1)
        pg.draw.line(screen, (0,255,0), end_pos, point_2)
        
        
        

while running:
    
    for event in pg.event.get():
        
        pg.draw.circle(screen, (255,0,0), (w / 2, h / 2), 30, 0)
        game.vector((10, 10), (200, 200), 1)
        
        if event.type == pg.QUIT:
            running = False
            
        
            
        

    game.draw_screen()
    
    

game.quit_algo()
