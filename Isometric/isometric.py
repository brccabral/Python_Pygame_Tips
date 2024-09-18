import pygame
import sys
import time

pygame.init()
pygame.display.set_caption("game base")
screen = pygame.display.set_mode((900, 900), 0, 32)
display = pygame.Surface((300, 300))

grass_img = pygame.image.load("grass.png").convert()
grass_img.set_colorkey((0, 0, 0))

f = open("map.txt")
map_data = [[int(c) for c in row] for row in f.read().split("\n")]
f.close()

while True:
    display.fill((0, 0, 0))

    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile:
                pygame.draw.rect(display, (255, 255, 255), pygame.Rect(x * 10, y * 10, 10, 10), 1)

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
    time.sleep(1)
