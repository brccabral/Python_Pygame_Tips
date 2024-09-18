import sys
import os
import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500), 0, 32)
display = pygame.Surface((100, 100))

images = [pygame.image.load("car/" + img) for img in os.listdir("car")]

clock = pygame.time.Clock()


# for performance, it is better to calculate all rotations on game load
# and cache them (in dictionary).
# 90 different angles are good for pixelart games
def render_stack(
    surf: pygame.Surface,
    images: list[pygame.Surface],
    pos: tuple[float, float],
    rotation: float,
    spread: int = 1,
):
    for i, img in enumerate(images):
        rotated_img = pygame.transform.rotate(img, rotation)
        surf.blit(
            rotated_img, (pos[0] - rotated_img.get_width() // 2, pos[1] - rotated_img.get_height() // 2 - i * spread)
        )


# frame serves as rotation
frame = 0

while True:
    display.fill((0, 0, 0))

    frame += 1
    # spred=1 is better, with 2 we already see gaps
    render_stack(display, images, (50, 100), frame, spread=15)

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
