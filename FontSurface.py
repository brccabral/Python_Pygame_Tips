import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

pygame.init()

mainClock = pygame.time.Clock()

pygame.display.set_caption("Font Surface")
screen = pygame.display.set_mode((500, 500), 0, 32)


# Funcs/Classes ---------------------------------------------- #
def clip(surf: pygame.Surface, x: int, y: int, x_size: int, y_size: int):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


class Font:
    def __init__(self, path: str):
        self.spacing = 1
        # fmt: off
        # order as presented in image
        self.character_order = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                                'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                                'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                                't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', '\'', '!', '?',
                                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=',
                                '\\', '[', ']', '*', '"', '<', '>', ';']
        # fmt: on
        font_img = pygame.image.load(path).convert()
        current_char_width = 0
        self.characters: dict[str, pygame.Surface] = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            # from the image we see that each char is separated by gray bars
            # so, if we see gray value, it is the end of the char
            if c.r == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                char_img.set_colorkey((0, 0, 0))
                self.characters[self.character_order[character_count]] = char_img
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters["A"].get_width()

    def render(self, surf: pygame.Surface, text: str, loc: tuple[int, int]):
        x_ofset = 0
        for char in text:
            if char != " ":
                surf.blit(self.characters[char], (loc[0] + x_ofset, loc[1]))
                x_ofset += self.characters[char].get_width() + self.spacing
            else:
                x_ofset += self.space_width + self.spacing


small_font = Font("small_font.png")

# Loop ------------------------------------------------------- #
while True:

    # Background --------------------------------------------- #
    screen.fill((0, 255, 0))

    small_font.render(screen, "Hello, World!", (20, 20))

    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)
