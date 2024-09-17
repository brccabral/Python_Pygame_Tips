# YOU MUST PROVIDE YOUR OWN pic.png
import sys
import pygame

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption("game base")
screen = pygame.display.set_mode((500, 500), 0, 32)

img = pygame.image.load("player.png").convert()

offset = [0, 0]

# Loop ------------------------------------------------------- #
while True:

    # Background --------------------------------------------- #
    screen.fill((0, 0, 0))

    mx, my = pygame.mouse.get_pos()

    rot = 0
    loc = [mx, my]
    screen.blit(pygame.transform.rotate(img, rot), (loc[0] + offset[0], loc[1] + offset[1]))

    # Buttons ------------------------------------------------ #
    right_clicking = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)
