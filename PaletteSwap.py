import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("game base")
screen = pygame.display.set_mode((800, 500), 0, 32)

tree_img = pygame.image.load("tree.png").convert()
tree_img.set_colorkey((0, 0, 0))


# be careful with performance in a game loop
def palette_swap(surf: pygame.Surface, olc_c: pygame.Color, new_c: pygame.Color):
    img_copy = pygame.Surface(surf.get_size())
    img_copy.fill(new_c)
    surf.set_colorkey(olc_c)
    img_copy.blit(surf, (0, 0))
    return img_copy


swap_img = tree_img.copy()
swap_img = palette_swap(swap_img, pygame.Color(11, 70, 97), pygame.Color(17, 11, 96))
swap_img = palette_swap(swap_img, pygame.Color(15, 106, 99), pygame.Color(83, 32, 145))
swap_img = palette_swap(swap_img, pygame.Color(35, 152, 77), pygame.Color(167, 65, 131))
swap_img = palette_swap(swap_img, pygame.Color(154, 209, 59), pygame.Color(205, 124, 97))
swap_img.set_colorkey((0, 0, 0))  # need to reset set_colorkey as `palette_swap()` creates a new black Surface

# Loop ------------------------------------------------------- #
while True:

    # Background --------------------------------------------- #
    screen.fill((255, 255, 255))

    screen.blit(pygame.transform.scale(tree_img, (tree_img.get_width() * 3, tree_img.get_height() * 3)), (50, 50))
    screen.blit(pygame.transform.scale(swap_img, (swap_img.get_width() * 3, swap_img.get_height() * 3)), (400, 50))

    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)
