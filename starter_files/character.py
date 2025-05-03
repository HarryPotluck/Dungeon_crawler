import pygame
import constants
from weapon import Fireball
import math

class Character():
    def __init__(self, x, y, health: int, mob_animations, char_type: int, is_boss=False):
        self.flip = False
        self.frame_index = 0
        self.action = 0   # 0:idle, 1:run
        self.update_time = pygame.time.get_ticks()
        self.char_type = char_type
        self.is_boss = is_boss
        self.animation_list = mob_animations[char_type]
        self.running = False
        self.health = health
        self.score = 0
        self.alive = True
        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.stunned = False


        self.image = self.animation_list[self.action][self.frame_index]
        if is_boss:
            self.rect = pygame.Rect(0, 0, 40 * constants.BOSS_SCALE, 40 * constants.BOSS_SCALE)
        else:
            self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x, y)


    def move(self, dx, dy, obstacle_tiles):
        
        screen_scroll = [0, 0]
        self.running = False

        # Run check
        if dx != 0 or dy != 0:
            self.running = True

        # Flip check
        if dx > 0:
            self.flip = False
        elif dx < 20:
            self.flip = True
            
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        # Check for horizontal collision 
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if dx > 0:
                    self.rect.right = obstacle[1].left
                else:
                    self.rect.left = obstacle[1].right
        # Check for vertical collision
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                else:
                    self.rect.top = obstacle[1].bottom
            
    
        # only applied to player
        if self.char_type == 0:
            # Scroll screen
            if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
                screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.rect.right
                self.rect.right = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH)
            if self.rect.left  < constants.SCROLL_THRESH:
                screen_scroll[0] = constants.SCROLL_THRESH - self.rect.left
                self.rect.left = constants.SCROLL_THRESH
            if self.rect.top < constants.SCROLL_THRESH:
                screen_scroll[1] = constants.SCROLL_THRESH - self.rect.top
                self.rect.top = constants.SCROLL_THRESH
            if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
                screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH
            return screen_scroll
        
    def ai(self, player, obstacle_tiles, screen_scroll, fireball_image):
        clipped_line = ()
        ai_dx = 0
        ai_dy = 0
        fireball = None
        stunned_cooldown = 100

        dist = math.sqrt((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2)
        line_of_sight = ((self.rect.centerx, self.rect.centery), (player.rect.centerx, player.rect.centery))

        # Check if line of sight blocked by obstacle
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)

        # Following player if see
        if dist > constants.RANGE and not clipped_line:
            if self.rect.centerx < player.rect.centerx:
                ai_dx = constants.ENEMY_SPEED
            else:
                ai_dx = -constants.ENEMY_SPEED
            if self.rect.centery < player.rect.centery:
                ai_dy = constants.ENEMY_SPEED
            else:
                ai_dy = -constants.ENEMY_SPEED

        # Check stunned
        if self.alive:
            if not self.stunned:
                # Attack
                if dist <= constants.ATTACK_RANGE:
                    self.update_action(0)
                    if player.alive == True and player.hit == False:
                        player.hit = True
                        player.last_hit = pygame.time.get_ticks()
                        player.health -= 10
            # Boss shooting fireballs
            fireball_cooldown = 200
            if self.is_boss:
                if dist < 500:
                    if pygame.time.get_ticks() - self.last_attack > fireball_cooldown:
                        fireball = Fireball(fireball_image, self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                        self.last_attack = pygame.time.get_ticks()

        # Check if hit
        if self.hit:
            self.hit = False
            self.running = False
            self.stunned = True
            self.last_hit = pygame.time.get_ticks()

        # Reset hit
        if pygame.time.get_ticks() - self.last_hit > stunned_cooldown:
            self.stunned = False
            self.last_hit = pygame.time.get_ticks()

        # Screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # Move
        if self.alive:
            self.move(ai_dx, ai_dy, obstacle_tiles)

        return fireball

    def update(self):
        # Check alive
        if self.health <= 0:
            self.health = 0
            self.alive = False
        # Check hit cooldown
        hit_cooldown = 1000

        if self.char_type == 0:
            if pygame.time.get_ticks() - self.last_hit > hit_cooldown:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
        
        # Check current health
        if self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 70

        self.image = self.animation_list[self.action][self.frame_index]
        
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0


    def update_action(self, new_action: int):
        if new_action != self.action:
            self.action = new_action
        #update animation action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.OFFSET * constants.SCALE))
        else:
            surface.blit(flipped_image, self.rect)

        pygame.draw.rect(surface, constants.RED, self.rect, 1)
