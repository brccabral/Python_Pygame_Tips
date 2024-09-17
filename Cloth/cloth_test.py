import pygame
import sys

import cloth

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption("cloth?")
screen = pygame.display.set_mode((500, 500), 0, 32)

rag_data = cloth.load_rags("rags")

my_cloth = cloth.ClothObj(rag_data["vine"])

render_mode = 0

# Loop ------------------------------------------------------- #
while True:

    # Background --------------------------------------------- #
    screen.fill((0, 0, 0))

    # Cloth -------------------------------------------------- #
    mx, my = pygame.mouse.get_pos()

    # move
    my_cloth.move_grounded([mx, my])

    # process
    my_cloth.update()
    my_cloth.update_sticks()

    # render
    if render_mode:
        my_cloth.render_polygon(screen, (255, 255, 255))
    else:
        my_cloth.render_sticks(screen)

    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_r:
                if render_mode:
                    render_mode = 0
                else:
                    render_mode = 1

    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)
