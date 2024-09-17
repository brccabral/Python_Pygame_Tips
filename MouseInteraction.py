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

clicking = False
right_clicking = False
middle_click = False

# Loop ------------------------------------------------------- #
while True:

    # Background --------------------------------------------- #
    screen.fill((0, 0, 0))

    mx, my = pygame.mouse.get_pos()

    rot = 0
    loc = [mx, my]
    if clicking:
        rot -= 90
    if right_clicking:
        rot += 180
    if middle_click:
        rot += 90
    screen.blit(pygame.transform.rotate(img, rot), (loc[0] + offset[0], loc[1] + offset[1]))

    # Buttons ------------------------------------------------ #
    right_clicking = False  # right click is check for each frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True
            if event.button == 3:
                right_clicking = True
            if event.button == 2:
                middle_click = not middle_click  # middle_click works as a toggle
            if event.button == 4:  # scroll up
                offset[1] -= 10
            if event.button == 5:  # scroll down
                offset[1] += 10
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False

    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)
