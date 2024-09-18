import sys
import pygame

pygame.init()
pygame.display.set_caption("mask test")

screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

img = pygame.image.load("img.png")
img.set_colorkey((0, 0, 0))
# img.set_colorkey((255, 127, 39))  # the "alpha" is the orange
img_2 = pygame.image.load("img_2.png")
img_2.set_colorkey((0, 0, 0))
# img_2.set_colorkey((255, 127, 39))
img_loc = (50, 50)

# unsetcolor = set the color of the original "colorkey"
# here we are setting to transparent (default is black)
# setcolor = set the Mask main color (default is white)
mask = pygame.mask.from_surface(img)
# mask_surf = mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(0, 0, 100, 255))
mask_surf = mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255))
mask_2 = pygame.mask.from_surface(img_2)
# mask_2_surf = mask_2.to_surface(unsetcolor=(0, 0, 100, 100), setcolor=(100, 0, 0, 100))
mask_2_surf = mask_2.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255))

show_masks = False

# every = skips some points, may be used to improve performance
outline = [(p[0] + img_loc[0], p[1] + img_loc[1]) for p in mask.outline(every=1)]

while True:
    screen.fill((24, 24, 24))

    mx, my = pygame.mouse.get_pos()

    if not show_masks:
        screen.blit(img, img_loc)
        screen.blit(img_2, (mx, my))
    else:
        screen.blit(mask_surf, img_loc)
        screen.blit(mask_2_surf, (mx, my))
        pygame.draw.lines(screen, (255, 0, 255), False, outline, 3)

        overlap_mask = mask.overlap_mask(mask_2, (mx - img_loc[0], my - img_loc[1]))
        screen.blit(overlap_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 0, 0, 255)), img_loc)

        # overlap_centroid - is not the middle, but the average of overlaping points (mass center)
        overlap_centroid = overlap_mask.centroid()
        pygame.draw.circle(
            screen, (0, 200, 255), (overlap_centroid[0] + img_loc[0], overlap_centroid[1] + img_loc[1]), 10, 3
        )
        pygame.draw.circle(
            screen, (0, 200, 255), (overlap_centroid[0] + img_loc[0], overlap_centroid[1] + img_loc[1]), 3, 3
        )

        # area is faster than count
        print(f"count {overlap_mask.count()}")
        print(f"area {mask.overlap_area(mask_2, (mx - img_loc[0], my - img_loc[1]))}")
        # to detect if there is a overlap, getting just the first point is even faster
        print(f"First point {mask.overlap(mask, (mx - img_loc[0], my - img_loc[1]))}")

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
