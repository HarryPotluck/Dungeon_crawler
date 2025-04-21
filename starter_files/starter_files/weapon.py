import pygame
import constants
import math
import random
class Weapon():
    def __init__(self, image, arrow_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.arrow_image = arrow_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player):
        arrow = None
        shot_cooldown = 300

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)

        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # Get mouse click
        if pygame.mouse.get_pressed()[0] and self.fired == False and pygame.time.get_ticks() - self.last_shot >= shot_cooldown:
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False
        
        return arrow

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, ((self.rect.centerx - self.image.get_width()/2), (self.rect.centery - self.image.get_height()/2)))
        
class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        super().__init__()
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        #calculate speed based on angle
        self.dx = math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.ARROW_SPEED)  # pygame y coor increases down
    
    def update(self, screen_scroll, enemy_list, obstacle_tiles):
        # Reposition
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        
        # Initialize Damage
        damage = 0
        damage_pos = None

        #reposition based on speed
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Check if arrow is off_screen
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.top > constants.SCREEN_HEIGHT or self.rect.bottom < 0:
            self.kill()
        
        # Check if arrow hit wall
        for obstacle in obstacle_tiles:
            if self.rect.colliderect(obstacle[1]):
                self.kill()

        # Check collision between arrows and monsters
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5, 5)
                enemy.health -= damage
                damage_pos = enemy.rect
                enemy.hit = True
                self.kill()
                break
        
        return damage, damage_pos

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - self.image.get_width()/2), (self.rect.centery - self.image.get_height()/2)))

class Fireball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y):
        super().__init__()
        self.original_image = image
        
        #calculate speed based on angle
        x_dist = target_x - x
        y_dist = -(target_y - y)
        angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.original_image, angle - 90 + random.randint(-5, 5))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.dx = math.cos(math.radians(angle)) * constants.FIREBALL_SPEED
        self.dy = -(math.sin(math.radians(angle)) * constants.FIREBALL_SPEED)  # pygame y coor increases down
    
    def update(self, screen_scroll, player):
        # Reposition
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        
        #reposition based on speed
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Check if arrow is off_screen
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.top > constants.SCREEN_HEIGHT or self.rect.bottom < 0:
            self.kill()
        
        # Check collision between fireball and player
        if self.rect.colliderect(player.rect):
            self.kill()
            if player.hit == False:
                player.hit = True
                player.health -= 10 if player.alive else 0
                player.last_hit = pygame.time.get_ticks()
        

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - self.image.get_width()/2), (self.rect.centery - self.image.get_height()/2)))