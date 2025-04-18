import pygame
import constants
import math

class Character():
    def __init__(self, x, y, health: int, mob_animations, char_type: int, is_boss=False):
        self.flip = False
        self.frame_index = 0
        self.action = 0   # 0:idle, 1:run
        self.update_time = pygame.time.get_ticks()
        self.char_type = char_type
        self.animation_list = mob_animations[char_type]
        self.running = False
        self.health = health
        self.score = 0
        self.alive = True

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
        elif dx < 0:
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
        
    def ai(self, screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

    def update(self):
        # Check alive
        if self.health <= 0:
            self.health = 0
            self.alive = False
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
