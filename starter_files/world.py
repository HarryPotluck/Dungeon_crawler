from character import Character
from items import Item
import constants

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.level_tile = None
        self.item_list = []
        self.player = None
        self.enemy = []

    def process_data(self, data, tile_list, item_images, mob_animations):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                tile = int(tile)
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                if tile == 7:
                    self.obstacle_tiles.append(tile_data)
                if tile == 8:
                    self.level_tile = tile_data
                if tile == 9:
                    coin = Item(image_x, image_y, 0, item_images[0])
                    self.item_list.append(coin)
                    tile_data[0] = tile_list[0]
                if tile == 10:
                    red_potion = Item(image_x, image_y, 1, item_images[1])
                    self.item_list.append(red_potion)
                    tile_data[0] = tile_list[0]
                if tile == 11:
                    player = Character(image_x, image_y, 100, mob_animations, 0) 
                    self.player = player
                    tile_data[0] = tile_list[0]
                if tile >= 12 and tile <= 16:
                    enemy = Character(image_x, image_y, 90, mob_animations, tile - 11)
                    tile_data[0] = tile_list[0]
                    self.enemy.append(enemy)
                if tile == 17:
                    enemy = Character(image_x, image_y, 300, mob_animations, tile - 11, True)
                    tile_data[0] = tile_list[0]
                    self.enemy.append(enemy)
                if tile >= 0:
                    self.map_tiles.append(tile_data)

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])
    
    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
    
    def next_level(self, player):
        if self.level_tile and self.level_tile[1].colliderect(player.rect):
            return True
        return False