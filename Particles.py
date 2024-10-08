import random
import pygame
import sys

TILE_SIZE = 20

pygame.init()
screen = pygame.display.set_mode((500, 500), 0, 32)
pygame.display.set_caption("Particles")

mainClock = pygame.time.Clock()


class Particle:
    def __init__(self, location: list[float], velocity: list[float], timer: float):
        self.location = location
        self.velocity = velocity
        self.timer = timer


particles: list[Particle] = []

tile_map: dict[str, tuple[int, int, tuple[int, int, int]]] = {}
for i in range(10):
    tile_map[str(i + 4) + ";14"] = (i + 4, 14, (255, 0, 0))

tile_map["15;10"] = (15, 10, (0, 0, 255))
tile_map["15;11"] = (15, 11, (0, 0, 255))
tile_map["15;12"] = (15, 12, (0, 0, 255))
tile_map["15;13"] = (15, 13, (0, 0, 255))

tile_map["11;11"] = (11, 11, (0, 255, 255))
tile_map["11;12"] = (11, 12, (0, 255, 255))

clicking = False

while True:
    screen.fill((0, 0, 0))

    mx, my = pygame.mouse.get_pos()

    if clicking:
        for i in range(30):
            particles.append(
                Particle(
                    [mx, my],
                    [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5],
                    random.randint(4, 6),
                )
            )

    to_remove: list[int] = []
    for i, particle in enumerate(particles):
        # horizontal collision
        particle.location[0] += particle.velocity[0]
        loc_str = str(int(particle.location[0] / TILE_SIZE)) + ";" + str(int(particle.location[1] / TILE_SIZE))
        if loc_str in tile_map:
            particle.velocity[0] = -0.7 * particle.velocity[0]
            particle.velocity[1] *= 0.95
            particle.location[0] += particle.velocity[0] * 2

        # vertical collision
        particle.location[1] += particle.velocity[1]
        loc_str = str(int(particle.location[0] / TILE_SIZE)) + ";" + str(int(particle.location[1] / TILE_SIZE))
        if loc_str in tile_map:
            particle.velocity[1] = -0.7 * particle.velocity[1]
            particle.velocity[0] *= 0.95
            particle.location[1] += particle.velocity[1] * 2

        particle.timer -= 0.035  # also radius
        particle.velocity[1] += 0.15  # gravity
        pygame.draw.circle(screen, (255, 255, 255), particle.location, particle.timer)
        if particle.timer <= 0:
            to_remove.append(i)

    # remove from a list outside main loop to avoid screen flickering
    for i in sorted(to_remove, reverse=True):
        particles.pop(i)

    for k, tile in tile_map.items():
        pygame.draw.rect(screen, tile[2], pygame.Rect(tile[0] * TILE_SIZE, tile[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

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
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False

    pygame.display.update()
    mainClock.tick(60)
