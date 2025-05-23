import pygame
import csv
import constants
from weapon import Weapon, Fireball
from world import World


# Initialize game
pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Game")
font = pygame.font.Font("starter_files\starter_files/assets/fonts/AtariClassic.ttf", 24)

#create clock for frame rate
clock = pygame.time.Clock()

#define game variables
level = 1
screen_scroll = []

#helper function to scale
def scale(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# Load weapon images
bow_image = scale(pygame.image.load(f'starter_files/starter_files/assets/images/weapons/bow.png').convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale(pygame.image.load(f'starter_files/starter_files/assets/images/weapons/arrow.png').convert_alpha(), constants.WEAPON_SCALE)
fireball_image = scale(pygame.image.load(f'starter_files/starter_files/assets/images/weapons/fireball.png').convert_alpha(), constants.WEAPON_SCALE)
#Load coins
coin_list = []
for i in range(4):
    img = scale(pygame.image.load(f'starter_files\starter_files/assets\images\items\coin_f{i}.png').convert_alpha(), constants.ITEM_SCALE)
    coin_list.append(img)
# Load potion
red_potion = scale(pygame.image.load(f'starter_files\starter_files/assets\images\items\potion_red.png').convert_alpha(), 2)
# Load items
item_list = []
item_list.append(coin_list)
item_list.append([red_potion])
# Load hearts
heart_empty = scale(pygame.image.load(f'starter_files/starter_files/assets/images/items/heart_empty.png').convert_alpha(), constants.ITEM_SCALE)
heart_half = scale(pygame.image.load(f'starter_files/starter_files/assets/images/items/heart_half.png').convert_alpha(), constants.ITEM_SCALE)
heart_full = scale(pygame.image.load(f'starter_files/starter_files/assets/images/items/heart_full.png').convert_alpha(), constants.ITEM_SCALE)
# Load character images
mob_animations = []
mob_type = ["elf", "tiny_zombie", "skeleton", "goblin", "muddy", "imp", "big_demon"]   # elf == player
animation_type = ["idle", "run"]

for mob in mob_type:
    animation_list = []
    for animation in animation_type:
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'starter_files/starter_files/assets/images/characters/{mob}/{animation}/{i}.png').convert_alpha()
            img = scale(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

# Load tiles
tile_list = []
for i in range(constants.TILE_TYPE):
    img = pygame.image.load(f'starter_files\starter_files/assets/images/tiles/{i}.png').convert_alpha()
    tile_img = pygame.transform.scale(img, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_img)
# Load world
with open(f'starter_files\starter_files\levels\level{level}_data.csv', newline='') as csvfile:
    map_level = [row for row in csv.reader(csvfile)] 

# Create world
world = World()
world.process_data(map_level, tile_list, item_list, mob_animations)

# Character
player = world.player
# Weapon
bow = Weapon(bow_image, arrow_image)
# Sprite groups
arrow_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
for item in world.item_list:
    item_group.add(item)
fireball_group = pygame.sprite.Group()

# Display player hearts
def draw_info():
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50), 1)

    half = True
    for i in range(5):
        if player.health >= (i+1)* 20:
            screen.blit(heart_full, (10 + heart_full.get_width() * i, 0))
        elif player.health % 20 == 10 and half:
            screen.blit(heart_half, (10 + heart_full.get_width() * i, 0))
            half = False
        else:
            screen.blit(heart_empty, (10 + heart_full.get_width() * i, 0))

    draw_text(font, constants.WHITE, constants.SCREEN_WIDTH / 2, 15, "LEVEL: "+ str(level))
    draw_text(font, constants.RED, constants.SCREEN_WIDTH - 200, 15 , f"Score: {player.score}")      
# Display text func
def draw_text(font, color, x, y, msg):
    img = font.render(msg, True, color)
    screen.blit(img, (x, y))
    return img.get_width()
# Create damage text
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color, ):
        super().__init__()
        self.image = font.render(str(damage), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.counter = 0

    def update(self, screen_scroll):
        # Reposition
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

#------------------------------------------------------------------
# Movement boolean
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
    screen_scroll = player.move(dx, dy, world.obstacle_tiles)
    
    # Check level
    if world.next_level(player):
        level += 1

        # Load new CSV
        with open(f'starter_files/starter_files/levels/level{level}_data.csv', newline='') as csvfile:
            map_level = [row for row in csv.reader(csvfile)]

        # Clear groups
        arrow_group.empty()
        damage_text_group.empty()
        item_group.empty()
        fireball_group.empty()
        
        # Save from prev rounds
        temp_health = player.health
        temp_score = player.score
        # Rebuild world
        world = World()
        world.process_data(map_level, tile_list, item_list, mob_animations)
        player = world.player
        player.health = temp_health
        player.score = temp_score

    # Update all
    world.update(screen_scroll)
    player.update()
    for enemy in world.enemy:
        fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll, fireball_image)
        if enemy.alive:
            enemy.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(screen_scroll, world.enemy, world.obstacle_tiles)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, damage, constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update(screen_scroll)
    if fireball:
        fireball_group.add(fireball)
    for fireball in fireball_group:
        fireball.update(screen_scroll, player)
    item_group.update(screen_scroll, player)

    #draw all
    world.draw(screen)
    player.draw(screen)
    for enemy in world.enemy:
        enemy.draw(screen)
    bow.draw(screen)
    
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen) #This is a Group object, which has built-in draw method without having to be defined.
    item_group.draw(screen)

    for fireball in fireball_group:
        fireball.draw(screen)

    # Next level
    world.next_level(player)
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
