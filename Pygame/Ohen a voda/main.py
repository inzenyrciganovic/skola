import pygame
from settings import *

pygame.init.screen()
screen = pygame.display.set_mode(SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.set_caption("hgisudhgiusd")
clock = pygame.tick.Clock()
running = True
while running:
    for event in pygame.event.get():
        