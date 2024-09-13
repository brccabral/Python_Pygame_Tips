import random
import pygame
import sys

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

while True:
    screen.fill((0, 0, 0))

    mouse_pos = pygame.mouse.get_pos()
    particles.append(Particle([mouse_pos[0], mouse_pos[1]], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)))

    for particle in particles:
        particle.location[0] += particle.velocity[0]
        particle.location[1] += particle.velocity[1]
        particle.timer -= 0.1  # also radius
        pygame.draw.circle(screen, (255, 255, 255), particle.location, particle.timer)
        particle.velocity[1] += 0.1  # gravity
        if particle.timer <= 0:
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
