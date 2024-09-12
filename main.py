import os
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

# camera
# true_scroll uses floats to follow player, but is converted to scroll with `int`
# when drawing on screen to avoing overlapping pixels
true_scroll = [0.0, 0.0]


def load_map(path):
    with open(path + ".txt", "r") as f:
        data = f.read()
    data = data.split("\n")
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


global animation_frames
animation_frames: dict[str, pygame.Surface] = {}


def load_animation(path: str, frame_durations: list[int]):
    """
    creates a list with the names of the frames\n
    if `frame_durations` = [3,4]\n
    `['idle_0', 'idle_0', 'idle_0', 'idle_1', 'idle_1', 'idle_1', 'idle_1']`\n
    and fills the global `animation_frames` with the actual Surface\n
    `{'idle_0': Surface0, 'idle_1': Surface1}`\n
    """
    global animation_frames

    _, animation_name = os.path.split(path)
    animation_frame_data: list[str] = []
    for n, frame in enumerate(frame_durations):
        animation_frame_id = animation_name + "_" + str(n)
        img_loc = os.path.join(path, animation_frame_id + ".png")
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255, 255, 255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
    return animation_frame_data


def change_action(action_var: str, frame: int, new_value: str):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


animation_database: dict[str, list[str]] = {}

animation_database["run"] = load_animation("player_animations/run", [7, 7])
animation_database["idle"] = load_animation("player_animations/idle", [7, 7, 40])

player_action = "idle"
player_frame = 0
player_flip = False

game_map = load_map("map")


player_rect = pygame.Rect(50, 50, 5, 13)

# [depth, Rect]
# depth makes object closer to move faster giving a parallax effect
background_objects = [
    [0.25, [120, 10, 70, 400]],
    [0.25, [280, 30, 40, 400]],
    [0.5, [30, 40, 40, 400]],
    [0.5, [130, 90, 100, 400]],
    [0.5, [300, 80, 120, 400]],
]

while True:
    display.fill((146, 244, 255))

    # camera follows player, 20 is the smoothing factor
    true_scroll[0] += (player_rect.x - true_scroll[0] - display.get_width() // 2 - player_rect.width // 2) / 20
    true_scroll[1] += (player_rect.y - true_scroll[1] - display.get_height() // 2 - player_rect.height // 2) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # horizon background
    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))

    for back_depth, back_rect in background_objects:
        obj_rect = pygame.Rect(
            back_rect[0] - scroll[0] * back_depth,
            back_rect[1] - scroll[1] * back_depth,
            back_rect[2],
            back_rect[3],
        )
        if back_depth == 0.5:
            pygame.draw.rect(display, (14, 222, 150), obj_rect)
        else:
            pygame.draw.rect(display, (9, 91, 85), obj_rect)

    tile_rects = []
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == "1":
                display.blit(dirt_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            elif tile == "2":
                display.blit(grass_image, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            # create rects for collisions
            if tile != "0":
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

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

    # animation
    if player_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, "run")
        player_flip = False
    elif player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, "idle")
    elif player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, "run")
        player_flip = True
    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_image = animation_frames[player_img_id]
    display.blit(
        pygame.transform.flip(player_image, player_flip, False), (player_rect.x - scroll[0], player_rect.y - scroll[1])
    )

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
