import pygame 
from pygame.locals import *
import random 

pygame.init()

#create the window 
width = 500
height = 500
screen_size = (width,height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# colours
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# game settings
gameover =  False 
speed = 2
score = 0

#markers size
marker_width = 10
marker_height = 50

# road and edge markers
road = (100, 0, 300, height)
left_edge_marker = (95, 0, marker_width, height)
rigth_edge_marker = (395, 0, marker_width, height)

# game loop 
clock = pygame.time.Clock()
fps = 120
running = True
while running:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False 
            
    # draw the grass
    screen.fill(green)

    # draw the road 
    pygame.draw.rect(screen, gray,road)

    pygame.display.update()

pygame.quit()