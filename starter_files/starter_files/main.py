import pygame
import constants
from character import Character
from weapon import Weapon

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Game")
font = pygame.font.Font("starter_files\starter_files/assets/fonts/AtariClassic.ttf", 32)

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

# Load heats
heart_empty = _scale(pygame.image.load(f'starter_files/starter_files/assets/images/items/heart_empty.png').convert_alpha(), constants.ITEM_SCALE)
heart_half = _scale(pygame.image.load(f'starter_files/starter_files/assets/images/items/heart_half.png').convert_alpha(), constants.ITEM_SCALE)
heart_full = _scale(pygame.image.load(f'starter_files/starter_files/assets/images/items/heart_full.png').convert_alpha(), constants.ITEM_SCALE)
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

# Create damage text
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color, ):
        super().__init__()
        self.image = font.render(str(damage), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

# Display player hearts
def draw_info():
    half = True
    for i in range(5):
        if player.health >= (i+1)* 20:
            screen.blit(heart_full, (10 + heart_full.get_width() * i, 0))
        elif player.health % 20 == 10 and half:
            screen.blit(heart_half, (10 + heart_full.get_width() * i, 0))
            half = False
        else:
            screen.blit(heart_empty, (10 + heart_full.get_width() * i, 0))
        
#Weapon
bow = Weapon(bow_image, arrow_image)


#Character
player = Character(100, 100, 80, mob_animations, 0)

#Enemy
enemy = Character(500, 300, 200, mob_animations, 1)
enemy_list = []
enemy_list.append(enemy)

# Sprite groups
arrow_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()

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
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, damage, constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()

    #draw main char
    player.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)
    bow.draw(screen)
    
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen) #This is a Group object, which has built-in draw method without having to be defined.

    draw_info()
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
