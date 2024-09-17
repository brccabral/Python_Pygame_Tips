import random
import pygame
import sys

TILE_SIZE = 20

pygame.init()
screen = pygame.display.set_mode((500, 500), 0, 32)
pygame.display.set_caption("Particles")

mainClock = pygame.time.Clock()


def circle_surf(radius: float, color: pygame.Color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf


class Particle:
    def __init__(self, location: list[float], velocity: list[float], timer: float):
        self.location = location
        self.velocity = velocity
        self.timer = timer


particles: list[Particle] = []

while True:
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (50, 20, 120), pygame.Rect(100, 100, 200, 80))

    mx, my = pygame.mouse.get_pos()

    particles.append(
        Particle(
            [mx, my],
            [random.randint(0, 20) / 10 - 1, -5],
            random.randint(6, 11),
        )
    )

    to_remove = []
    for i, particle in enumerate(particles):
        # horizontal collision
        particle.location[0] += particle.velocity[0]

        # vertical collision
        particle.location[1] += particle.velocity[1]

        particle.timer -= 0.1  # also radius
        particle.velocity[1] += 0.15  # gravity
        pygame.draw.circle(screen, (255, 255, 255), particle.location, particle.timer)

        radius = particle.timer * 2
        # Blen a Dark Gray shape to give a glow effect (we can change the color for different glows)
        screen.blit(
            circle_surf(radius, pygame.Color(20, 20, 60)),
            (particle.location[0] - radius, particle.location[1] - radius),
            special_flags=pygame.BLEND_RGB_ADD,
        )

        if particle.timer <= 0:
            to_remove.append(i)

    # remove from a list outside main loop to avoid screen flickering
    for i in sorted(to_remove, reverse=True):
        particles.pop(i)

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
