import pygame
import sys
import time
import random

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

    # for larger projects need to consider draw order, filter what to draw or not
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile:
                # 10 and 5 are related not just the TILE_SIZE, but also the image for the tile
                # the top corner to the right corner on the image

                # pygame.draw.rect(display, (255, 255, 255), pygame.Rect(x * 10, y * 10, 10, 10), 1)

                # the `- y * 10` and `+ x * 5` are to offset the image position in the isometric perception (rotation)
                # 150 and 100 are offsets for the rotation
                display.blit(grass_img, (150 + x * 10 - y * 10, 100 + x * 5 + y * 5))
                # `-14` is a "z" offset
                if random.randint(0, 1):
                    display.blit(grass_img, (150 + x * 10 - y * 10, 100 + x * 5 + y * 5 - 14))

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
