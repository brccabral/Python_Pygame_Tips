import pygame
import sys
import math
import random

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption("game base")
screen = pygame.display.set_mode((500, 500), 0, 32)


class Spark:
    def __init__(self, loc: list[float], angle: float, speed: float, color: pygame.Color, scale: float = 1):
        self.loc = loc
        self.angle = angle
        self.speed = speed  # more speed, larger the spark
        self.scale = scale
        self.color = color
        self.alive = True

    def point_towards(self, angle: float, rate: float):
        rotate_direction = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sing = 1  # noqa (ignore flake8 warning)
        if abs(rotate_direction) < rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign

    def calculate_movement(self, dt: int):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]

    # gravity and friction
    def velocity_adjust(self, friction: float, force: float, terminal_velocity: float, dt: int):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])
        # if you want to get more realistic, the speed should be adjusted here

    def move(self, dt: int):
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]

        # a bunch of options to mess around with relating to angles...
        # self.point_towards(math.pi / 2, 0.02)  # adds gravity 1
        # self.velocity_adjust(0.975, 0.2, 8, dt)  # adds gravity 2
        # self.angle += 0.1  # adds rotation

        self.speed -= 0.1

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        if self.alive:
            # 4 points in a diamond shape
            points = [
                [
                    self.loc[0] + math.cos(self.angle) * self.speed * self.scale,
                    self.loc[1] + math.sin(self.angle) * self.speed * self.scale,
                ],
                [
                    self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3,
                    self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3,
                ],
                [
                    self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5,
                    self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5,
                ],
                [
                    self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3,
                    self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3,
                ],
            ]
            pygame.draw.polygon(surf, self.color, points)


sparks: list[Spark] = []

# Loop ------------------------------------------------------- #
while True:

    # Background --------------------------------------------- #
    screen.fill((0, 0, 0))

    for i, spark in sorted(enumerate(sparks), reverse=True):
        spark.move(1)
        spark.draw(screen)
        if not spark.alive:
            sparks.pop(i)

    mx, my = pygame.mouse.get_pos()
    for i in range(10):  # adds more sparks per frame
        sparks.append(
            Spark([mx, my], math.radians(random.randint(0, 360)), random.randint(3, 6), pygame.Color(255, 255, 255), 2)
        )

    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)
