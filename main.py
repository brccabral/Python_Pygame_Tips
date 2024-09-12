import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_RIGHT, K_LEFT, K_UP

pygame.init()

pygame.display.set_caption("My Pygame Window")

WINDOW_SIZE = (600, 400)
TILE_SIZE = 16

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))

clock = pygame.time.Clock()

player_image = pygame.image.load("player.png").convert()
player_image.set_colorkey((255, 255, 255))

grass_image = pygame.image.load("grass.png").convert()
dirt_image = pygame.image.load("dirt.png").convert()


def collision_test(rect: pygame.Rect, tiles: list[pygame.Rect]):
    hit_list: list[pygame.Rect] = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect: pygame.Rect, movement: list[float], tiles: list[pygame.Rect]):
    collision_types = {"top": False, "bottom": False, "right": False, "left": False}

    # horizontal collision
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True

    # vertical collision
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True

    return rect, collision_types


moving_right = False
moving_left = False

# vertical_momentum increases 0.2 each frame, it takes 5 frames to move 1 tile
vertical_momentum = 0
# use air_timer to check if player is colliding at bottom (on the ground)
# if less than 6 frames, the player is considered on ground and can jump
air_timer = 0


def load_map(path):
    with open(path + ".txt", "r") as f:
        data = f.read()
    data = data.split("\n")
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = load_map("map")


player_rect = pygame.Rect(
    50,
    50,
    player_image.get_width(),
    player_image.get_height(),
)

while True:
    display.fill((146, 244, 255))

    tile_rects = []
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == "1":
                display.blit(dirt_image, (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == "2":
                display.blit(grass_image, (x * TILE_SIZE, y * TILE_SIZE))
            # create rects for collisions
            if tile != "0":
                tile_rects.append(
                    pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

    player_movement = [0.0, 0.0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum

    # gravity
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if collisions["bottom"]:
        vertical_momentum = 0
        air_timer = 0
    else:
        air_timer += 1
    if collisions["top"]:
        vertical_momentum = 0

    display.blit(player_image, player_rect.topleft)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:  # 5 frames to vertical_momentum gets to 1 (0.2 * 5)
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE))
    pygame.display.update()
    clock.tick(60)
