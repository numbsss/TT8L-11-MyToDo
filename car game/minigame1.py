import pygame 
from pygame.locals import *
import random

from pygame.sprite import Group 

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
right_edge_marker = (395, 0, marker_width, height)

# x coordinates of lanes 
left_lane =  150
centre_lane = 250
right_lane =  350
lanes = [left_lane, centre_lane, right_lane]

# for animating movement of the lane markers 
lane_marker_move_y = 0

class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        #scale the image down so it fits in the lane 
        image_scale  = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect ()
        self.rect.center = [x, y]  # Fixed typo here, it should be "center", not "centre"

class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('car.png')  # Corrected file path here
        super().__init__(image, x, y)
        
player_x = 250
player_y = 400

player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

clock = pygame.time.Clock()
fps = 120
running = True
while running:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False 

        # move the player's car using the left/right arrow key
        if event.type == KEYDOWN:

            if event.key == K_LEFT and player.rect.centre[0] > left_lane:
                player.rect.x == 100
            elif event.key == K_RIGHT and player.rect.centre[0] < right_lane:
                player.rect.x == 100 
            
    # draw the grass
    screen.fill(green)

    # draw the road 
    pygame.draw.rect(screen, gray,road)

    # draw the edge markers 
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # draw the lane markers 
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
        pygame.draw.rect(screen, white, (left_lane + 45, lane_marker_move_y, marker_width, marker_height))  # Removed unnecessary 'y +'
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (centre_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    player_group.draw(screen)

    pygame.display.update()

pygame.quit()