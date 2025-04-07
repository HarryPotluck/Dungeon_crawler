import pygame
import constants
from character import Character

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Game")

#create clock for frame rate
clock = pygame.time.Clock()

#helper function to scale
def _scale(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))


animation_list = []
for i in range(4):
    img = pygame.image.load(f'starter_files/starter_files/assets/images/characters/elf/idle/{i}.png').convert_alpha()
    img = _scale(img, constants.SCALE)
    animation_list.append(img)

#Character
player = Character(100, 100, animation_list)

moving_left = False
moving_right = False
moving_up = False
moving_down = False
run = True

while run:
    #Control frame rate
    clock.tick(constants.FPS)

    # Fill bg
    screen.fill(constants.BG)

    #coor
    dx = 0
    dy = 0

    if moving_left:
        dx = -constants.SPEED
    if moving_right:
        dx = constants.SPEED
    if moving_up:
        dy = -constants.SPEED
    if moving_down:
        dy = constants.SPEED
        
    player.move(dx, dy)
    player._update()
    #draw main char
    player.draw(screen, dx)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            print(f"Key pressed: {event.key}")
            if event.key in (pygame.K_a, pygame.K_LEFT):
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    pygame.display.update()
pygame.quit()
