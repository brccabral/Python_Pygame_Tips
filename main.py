from math import ceil
import os
import random
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_RIGHT, K_LEFT, K_UP, K_w, K_e

# pre_init the mixer to avoid delay when we play sound effects (jump.play())
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# allow more sounds to play at once, if not, sounds will be cutoff or not play
pygame.mixer.set_num_channels(64)

pygame.display.set_caption("My Pygame Window")

WINDOW_SIZE = (600, 400)
TILE_SIZE = 16
CHUNK_SIZE = 8  # visible tiles is a 8x8 grid

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))

VISIBLE_TILES_Y = ceil(display.get_height() / (CHUNK_SIZE * TILE_SIZE)) + 1
VISIBLE_TILES_X = ceil(display.get_width() / (CHUNK_SIZE * TILE_SIZE)) + 1

clock = pygame.time.Clock()

grass_image = pygame.image.load("grass.png").convert()
dirt_image = pygame.image.load("dirt.png").convert()
plant_image = pygame.image.load("plant.png").convert()
plant_image.set_colorkey((255, 255, 255))

tile_index = {1: grass_image, 2: dirt_image, 3: plant_image}


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

global animation_frames
animation_frames: dict[str, pygame.Surface] = {}


# generate the visible tiles on the fly
def generate_chunk(x: int, y: int):
    chunk_data: list[tuple[list[int], int]] = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # nothing
            if target_y > 10:
                tile_type = 2  # dirt
            elif target_y == 10:
                tile_type = 1  # grass
            elif target_y == 9:
                if random.randint(1, 5) == 1:
                    tile_type = 3  # plant
            if tile_type != 0:
                chunk_data.append(([target_x, target_y], tile_type))
    return chunk_data


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

jump_sound = pygame.mixer.Sound("sounds/jump.wav")
grass_sounds = [pygame.mixer.Sound("sounds/grass_0.wav"), pygame.mixer.Sound("sounds/grass_1.wav")]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load("sounds/music.wav")
pygame.mixer.music.play(-1)

player_action = "idle"
player_frame = 0
player_flip = False

# the map is generated as needed
game_map: dict[str, list[tuple[list[int], int]]] = {}

grass_sound_timer = 0

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

    # only play grass sound if timer is 0 and player is moving on the ground
    if grass_sound_timer > 0:
        grass_sound_timer -= 1

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

    # draw tiles
    tile_rects = []  # collision tiles
    for y in range(VISIBLE_TILES_Y):
        for x in range(VISIBLE_TILES_X):
            target_x = x - 1 + round(scroll[0] / (CHUNK_SIZE * TILE_SIZE))
            target_y = y - 1 + round(scroll[1] / (CHUNK_SIZE * TILE_SIZE))
            target_chunk = str(target_x) + ";" + str(target_y)
            # the map is generated as needed
            if target_chunk not in game_map:
                game_map[target_chunk] = generate_chunk(target_x, target_y)
            # only draw the tiles in current chunk
            for tile_pos, tile_type in game_map[target_chunk]:
                display.blit(
                    tile_index[tile_type], (tile_pos[0] * TILE_SIZE - scroll[0], tile_pos[1] * TILE_SIZE - scroll[1])
                )
                if tile_type in [1, 2]:
                    tile_rects.append(
                        pygame.Rect(tile_pos[0] * TILE_SIZE, tile_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
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
        # only play grass sound if timer is 0 and player is moving on the ground
        if player_movement[0] != 0:
            if grass_sound_timer == 0:
                grass_sound_timer = 30
                random.choice(grass_sounds).play()
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
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_e:
                pygame.mixer.music.play(-1)
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:  # 5 frames to vertical_momentum gets to 1 (0.2 * 5)
                    jump_sound.play()
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    # d = pygame.font.Font().render(f"{len(game_map)=}", False, "black")
    # display.blit(d, (20, 20))
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE))
    pygame.display.update()
    clock.tick(60)
