import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list,):
        super().__init__()
        self.item_type = item_type #0:coin 1: potion
        self.animation_list = animation_list
        self.frame_index = 0
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.update_time = pygame.time.get_ticks()

    def update(self, screen_scroll, player):
        # Reposition
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        
        #Handling collision
        if self.rect.colliderect(player.rect):
            # Coin
            if self.item_type == 0:
                player.score += 1
            # Potion red
            elif self.item_type == 1:
                player.health += 10
                if player.health > 100:
                    player.health = 100
                    score += 2
            self.kill()


        #Handling animation
        animation_cooldown = 200
        self.image = self.animation_list[self.frame_index]
        
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0