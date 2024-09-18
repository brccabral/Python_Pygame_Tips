import sys
import pygame

pygame.init()
pygame.display.set_caption("mask test")

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

while True:
    screen.fill((0, 0, 0))

    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.update()
    clock.tick(60)
