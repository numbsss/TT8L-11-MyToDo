import pygame,sys
pygame.init() 
from pygame.locals import* 
import random
import math
import time
screen = pygame.display.set_mode((798,600))

pygame.mixer.init()

pygame.display.set_caption('car game')

IntroFont = pygame.font.Font("freesansbold.ttf", 38)
def introImg(x,y):
    intro = pygame.image.load("car game\intro.png")
    
    screen.blit(intro,(x,y))
def play(x,y):
    playtext = IntroFont.render("PLAY",True,(255,0,0))
    screen.blit (playtext,(x,y))

def introscreen():
    run = True
    pygame.mixer.music.load('car game/startingMusic.mp3')
    pygame.mixer.music.play()
    while run :
        screen.fill((0,0,0))
        introImg(0,0)
        play(100,450)

        x,y = pygame.mouse.get_pos()

        button1 = pygame.Rect(60,440,175,50)

        pygame.draw.rect(screen, (255,255,255), button1,6)

        if button1.collidepoint(x,y):

            pygame.draw.rect(screen, (155,0,0), button1,6)

            if click:
                countdown() 
                
        click = False
        for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
         if event.type == pygame.MOUSEBUTTONDOWN:
             if event.button == 1:
                 click = True
        pygame.display.update()

def countdown():
    font2 = pygame.font.Font('freesansbold.ttf', 85)
    countdownBacground = pygame.image.load('car game/bg.png')
    three = font2.render('3',True, (187,30,16))
    two =   font2.render('2',True, (255,255,0))
    one =   font2.render('1',True, (51,165,50))
    go =    font2.render('GO!!!',True, (0,255,0))

    screen.blit(countdownBacground, (0,0))
    pygame.display.update()

    screen.blit(three,(350,250))
    pygame.display.update()
    time.sleep(1)

    screen.blit(countdownBacground, (0,0))
    pygame.display.update()
    time.sleep(1)

    screen.blit(two,(350,250))
    pygame.display.update()
    time.sleep(1)

    screen.blit(countdownBacground, (0,0))
    pygame.display.update()
    time.sleep(1)

    screen.blit(one,(350,250))
    pygame.display.update()
    time.sleep(1)

    screen.blit(countdownBacground, (0,0))
    pygame.display.update()
    time.sleep(1)

    screen.blit(go,(300,250))
    pygame.display.update()
    time.sleep(1)
    pygame.display.update()

