import random
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((500, 500), 0, 32)
pygame.display.set_caption("Particles")

mainClock = pygame.time.Clock()

# [loc, velocity, timer] - timer is also radius
particles = []

while True:
    screen.fill((0, 0, 0))

    particles.append([[250, 250], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])

    for particle in particles:
        # [loc, velocity, timer] - timer is also radius
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1  # also radius
        pygame.draw.circle(screen, (255, 255, 255), particle[0], particle[2])
        if particle[2] <= 0:
            particles.remove(particle)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.update()
    mainClock.tick(60)
