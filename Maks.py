import sys
import pygame

pygame.init()
pygame.display.set_caption("mask test")

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

img = pygame.image.load("img.png")
img.set_colorkey((0, 0, 0))
img_2 = pygame.image.load("img_2.png")
img_2.set_colorkey((0, 0, 0))
img_loc = (50, 50)

# unsetcolor = set the color of the original "alpha"
# here we are setting to transparent (default is black)
mask = pygame.mask.from_surface(img)
mask_surf = mask.to_surface(unsetcolor=(0, 0, 0, 0))
mask_2 = pygame.mask.from_surface(img_2)
mask_2_surf = mask_2.to_surface(unsetcolor=(0, 0, 0, 0))

show_masks = False

while True:
    screen.fill((0, 0, 0))

    mx, my = pygame.mouse.get_pos()

    if not show_masks:
        screen.blit(img, img_loc)
        screen.blit(img_2, (mx, my))
    else:
        screen.blit(mask_surf, img_loc)
        screen.blit(mask_2_surf, (mx, my))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                show_masks = not show_masks
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.update()
    clock.tick(60)
