import pygame
import constants
from character import Character
from weapon import Weapon

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

# Load weapon images
bow_image = _scale(pygame.image.load(f'starter_files/starter_files/assets/images/weapons/bow.png').convert_alpha(), constants.WEAPON_SCALE)
arrow_image = _scale(pygame.image.load(f'starter_files/starter_files/assets/images/weapons/arrow.png').convert_alpha(), constants.WEAPON_SCALE)

# Load character images
mob_animations = []
mob_type = ["elf", "big_demon", "goblin", "imp", "muddy", "skeleton", "tiny_zombie"]
animation_type = ["idle", "run"]

for mob in mob_type:
    animation_list = []
    for animation in animation_type:
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'starter_files/starter_files/assets/images/characters/{mob}/{animation}/{i}.png').convert_alpha()
            img = _scale(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

#Weapon
bow = Weapon(bow_image, arrow_image)
arrow_group = pygame.sprite.Group()

#Character
player = Character(100, 100, mob_animations, 0)

#Enemy
enemy = Character(40, 100, mob_animations, 3)
enemy_list = []
enemy_list.append(enemy)

moving_left = False
moving_right = False
moving_up = False
moving_down = False

# Game loop
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
    
    # Move player
    player.move(dx, dy)

    #Update player
    player.update()
    for enemy in enemy_list:
        enemy.update()
    arrow = bow.update(player)
    if arrow:
        print("arrow created")
        arrow_group.add(arrow)
    for arrow in arrow_group:
        print("arrow updated")
        arrow.update()

    #draw main char
    player.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)
    bow.draw(screen)
    
    for arrow in arrow_group:
        arrow.draw(screen)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                moving_left = True
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                moving_right = True
            if event.key in (pygame.K_w, pygame.K_UP):
                moving_up = True
            if event.key in (pygame.K_s, pygame.K_DOWN):
                moving_down = True

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_LEFT):
                moving_left = False
            if event.key in (pygame.K_d, pygame.K_RIGHT):
                moving_right = False
            if event.key in (pygame.K_w, pygame.K_UP):
                moving_up = False
            if event.key in (pygame.K_s, pygame.K_DOWN):
                moving_down = False

    pygame.display.update()

pygame.quit()
