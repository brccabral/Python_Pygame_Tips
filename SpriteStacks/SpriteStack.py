import sys
import os
import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500), 0, 32)
display = pygame.Surface((100, 100))

images = [pygame.image.load("car/" + img) for img in os.listdir("car")]

clock = pygame.time.Clock()

while True:
    display.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(60)
