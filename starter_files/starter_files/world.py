import constants

class World():
    def __init__(self):
        self.map_tiles = []

    def update(self, data, tile_list, level: int):
        for y, row in enumerate(data[level-1]):
            for x, tile in enumerate(row):
                tile = int(tile)
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                if tile >= 0:
                    self.map_tiles.append(tile_data)
    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
        